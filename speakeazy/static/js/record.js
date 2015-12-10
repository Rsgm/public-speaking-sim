(function () {
    var rec = {};

    var uploadQueue = [];
    var uploadTotal;
    var stopped;
    var progress;

    var uploadInterval = 5000;
    var crsf = document.getElementsByName('csrfmiddlewaretoken')[0].value; // $('csrfmiddlewaretoken').get(0);

    rec.project = window.location.pathname.split('/')[2];


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
            rec.mediaStream = stream;
            rec.url = window.URL.createObjectURL(rec.mediaStream);

            //$log.log(rec.mediaStream);

            rec.setupVideo = $('#setup-video').get(0);
            rec.setupVideo.src = rec.url;
            rec.setupVideo.muted = true;
            rec.setupVideo.play();

            rec.audienceVideo = $('#audience-video').get(0);
            rec.audienceVideo.requestFullscreen = ( rec.audienceVideo.requestFullscreen || rec.audienceVideo.mozRequestFullScreen || rec.audienceVideo.webkitRequestFullscreen);
            rec.audienceVideo.pause();

            $('#preview').show();


            var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            var source = audioCtx.createMediaStreamSource(stream);
            var analyser = audioCtx.createAnalyser();
            source.connect(analyser);

            var lastVolumes = [0, 0, 0, 0, 0, 0];
            rec.volumeInterval = setInterval(function () {
                var data = new Uint8Array(analyser.fftSize);
                analyser.getByteTimeDomainData(data);
                var sum = 0;

                data.forEach(function (e) {
                    sum += (e - 127) * (e - 127);
                });

                lastVolumes.push(Math.log(Math.pow(10, (Math.sqrt(sum / data.length)) / 127)) / Math.LN2);
                lastVolumes.shift();

                sum = 0;
                lastVolumes.forEach(function (e) {
                    sum += e;
                });

                rec.volume = sum / 2;

                rec.slider = {"margin-top": (200 - rec.volume * 200) + "px"};
            }, 200);

            rec.stopAudioAnalyzer = function stopAudioAnalyzer() {
                clearInterval(rec.volumeInterval);

                analyser.disconnect();
                source.disconnect();
                audioCtx.close();
            };
        }

        function onMediaError(e) {
            //$log.error('media error', e);
        }
    }

    function startRecording() {
        $('#preview').hide();
        $('#recording').show();

        rec.stopAudioAnalyzer();

        rec.setupVideo.muted = true;
        rec.audienceVideo.play();
        //rec.audienceVideo.requestFullscreen();

        $.get('/projects/' + rec.project + '/record/start/', function (result) {
            rec.id = result.id;

            // setup recorder and start recording

            rec.mediaRecorder = new MultiStreamRecorder(rec.mediaStream);
            rec.mediaRecorder.video = rec.setupVideo;

            rec.mediaRecorder.ondataavailable = function (blobs) {
                upload(rec.id, blobs.video, blobs.audio);
                if (!rec.started) {
                    rec.started = true;
                }
            };

            rec.mediaRecorder.start(uploadInterval);
        });
    }

    function stopRecording() {
        $('#recording').hide();
        $('#finished').show();

        rec.audienceVideo.pause();
        rec.mediaRecorder.stop();

        finish(rec.id, function progress(size, uploadTotal) {
            rec.progress = Math.floor((uploadTotal - size) * 100 / uploadTotal);
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

                    $.post('/projects/' + rec.project + '/record/' + rec.id + '/upload/', data, function () {
                        uploadQueue.shift();
                        if (stopped) {
                            progress(uploadQueue.length, uploadTotal);
                        }
                        uploadPiece();
                    });
                } else if (stopped) {
                    $.get('/projects/' + rec.project + '/record/' + rec.id + '/finish/');
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