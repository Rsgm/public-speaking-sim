(function () {
    var uploadQueue = [];
    var uploadTotal;
    var stopped;
    var progress;

    var mediaStream;
    var setupVideo;
    var audienceVideo;
    var stopAudioAnalyzer;

    var mediaRecorder;
    var started;

    var uploadInterval = 3000;
    var crsf = $('input[name=csrfmiddlewaretoken]').val();

    navigator.getUserMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);

    $('#start-recording').click(startRecording);
    $('#stop-recording').click(stopRecording);
    $('#preview').hide();
    $('#recording').hide();
    $('#finished').hide();

    initializeMediaStream();


    /**
     * Sets up webcam stream object.
     * This will ask the user for permission to access the webcam (unless using tls, iirc)
     */
    function initializeMediaStream() {
        var mediaConstraints = {
            audio: true,
            video: true
        };

        navigator.getUserMedia(mediaConstraints, onMediaSuccess, onMediaError);


        function onMediaSuccess(stream) {
            mediaStream = stream;
            url = window.URL.createObjectURL(mediaStream);

            console.log(mediaStream);

            setupVideo = $('#setup-video').get(0);
            setupVideo.src = url;
            setupVideo.muted = true;
            setupVideo.play();

            audienceVideo = $('#audience-video').get(0);
            audienceVideo.requestFullscreen = ( audienceVideo.requestFullscreen || audienceVideo.mozRequestFullScreen || audienceVideo.webkitRequestFullscreen);
            audienceVideo.pause();

            $('#preview').show();


            var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            var source = audioCtx.createMediaStreamSource(stream);
            var analyser = audioCtx.createAnalyser();
            source.connect(analyser);

            var $volume = $('#volume-slider');
            var totalHeight = $volume.parent().height();

            var lastVolumes = [0, 0, 0, 0, 0, 0];
            var volumeInterval = setInterval(function () {
                var data = new Uint8Array(analyser.fftSize);
                analyser.getByteTimeDomainData(data);
                var sum = 0;

                data.forEach(function (e) {
                    sum += (e - 127) * (e - 127);
                });

                var v = Math.sqrt(sum / data.length) / 127;
                var baseTen = Math.log(Math.pow(10, v)) / Math.LN2;
                console.log([v, baseTen]);

                lastVolumes.push(v);
                lastVolumes.shift();

                sum = 0;
                lastVolumes.forEach(function (e) {
                    sum += e;
                });

                var volume = sum / 2;

                var height = totalHeight - volume * totalHeight;
                $volume.css('height', height + 'px')
            }, 200);

            stopAudioAnalyzer = function () {
                clearInterval(volumeInterval);

                analyser.disconnect();
                source.disconnect();
                audioCtx.close();
            };
        }

        function onMediaError(e) {
            //console.error('media error', e);
        }
    }

    function startRecording() {
        $('#preview').hide();
        $('#recording').show();

        stopAudioAnalyzer();

        setupVideo.muted = true;
        audienceVideo.play();
        //audienceVideo.requestFullscreen();

        $.post('/record/' + se.project + '/', {request: 'start', csrfmiddlewaretoken: crsf}, function (result) {
            id = result.id;

            // setup recorder and start recording

            mediaRecorder = new MultiStreamRecorder(mediaStream);
            mediaRecorder.video = setupVideo;

            mediaRecorder.ondataavailable = function (blobs) {
                upload(id, blobs.video, blobs.audio);
                if (!started) {
                    started = true;
                }
            };

            mediaRecorder.start(uploadInterval);
        });
    }

    function stopRecording() {
        $('#recording').hide();
        $('#finished').show();

        audienceVideo.pause();
        mediaRecorder.stop();

        finish(id, function progress(size, uploadTotal) {
            progress = Math.floor((uploadTotal - size) * 100 / uploadTotal);
        });
    }


    function upload(id, video, audio) {
        var result = {
            recordingUuid: id
        };

        var hasVideo = video.type.startsWith("video");
        var hasAudio = audio.type.startsWith("audio");

        console.log({
            id: id,
            video: video,
            audio: audio
        });

        function uploadBlob(result) {
            uploadQueue.push(result);
            if (uploadQueue.length == 1) {
                uploadPiece();
            }

            function uploadPiece() { // recursively finish uploading
                if (uploadQueue.length > 0) {
                    var data = uploadQueue[0];
                    data.csrfmiddlewaretoken = crsf;
                    data.recording = id;
                    data.request = 'upload';

                    $.post('/record/' + se.project + '/', data, function () {
                        uploadQueue.shift();
                        if (stopped) {
                            progress(uploadQueue.length, uploadTotal);
                        }
                        uploadPiece();
                    });
                } else if (stopped) {
                    $.post('/record/' + se.project + '/', {
                        recording: id,
                        request: 'finish',
                        csrfmiddlewaretoken: crsf
                    }, function (response) {
                        window.location.href = response;
                    });
                }
            }
        }


        if (video && hasVideo) {
            var videoReader = new FileReader();
            videoReader.readAsDataURL(video);

            // encode video into base64
            videoReader.onload = function () {
                result.v = videoReader.result.match(/,(.*)$/)[1]; // move this to the resource

                if (!audio || !hasAudio || result.audioData) { // upload when both are ready
                    uploadBlob(result);
                }
            };
        }

        if (audio && hasAudio) {
            var audioReader = new FileReader();
            audioReader.readAsDataURL(audio);

            // encode audio into base64
            audioReader.onload = function () {
                result.a = audioReader.result.match(/,(.*)$/)[1]; // move this to the resource

                if (!video || !hasVideo || result.videoData) { // upload when both are ready, or there is no video
                    uploadBlob(result);
                }
            };
        }
    }

    function finish(record, progressFn) {
        progress = progressFn;
        uploadTotal = uploadQueue.length;
        stopped = record;
    }
})();
