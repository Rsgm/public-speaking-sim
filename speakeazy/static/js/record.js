(function () {
  var stopped;

  var mediaStream;
  var recording;
  var setupVideo;
  var audienceVideo;
  var stopAudioAnalyzer;

  var mediaRecorder;

  var uploadInterval = 9900; // ms
  var uploadQueue = [];
  var uploadTotal;

  var crsf = $('input[name=csrfmiddlewaretoken]').val();

  // navigator.getUserMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);

  $('#start-recording').click(startRecording);
  $('#stop-recording').click(stopRecording);
  $('#preview').hide();
  $('#recording').hide();
  $('#finished').hide();

  initializeMediaStream();


  /**
   * Sets up webcam stream object.
   */
  function initializeMediaStream() {
    var mediaConstraints = {
      audio: true,
      video: true
    };

    navigator.getUserMedia(mediaConstraints, onMediaSuccess, onMediaError);


    function onMediaSuccess(stream) {
      mediaStream = stream;
      console.log(mediaStream);


      setupVideo = $('#setup-video').get(0);
      setupVideo.src = window.URL.createObjectURL(mediaStream);
      setupVideo.muted = true;
      setupVideo.play();

      audienceVideo = $('#audience-video').get(0);
      audienceVideo.pause();

      $('#preview').show();


      // var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      // var source = audioCtx.createMediaStreamSource(stream);
      // var analyser = audioCtx.createAnalyser();
      // source.connect(analyser);
      //
      // var $volume = $('#volume-slider');
      // var totalHeight = $volume.parent().height();
      //
      //var lastVolumes = [0, 0, 0, 0, 0, 0];
      //var volumeInterval = setInterval(function () {
      //  var data = new Uint8Array(analyser.fftSize);
      //  analyser.getByteTimeDomainData(data);
      //  var sum = 0;
      //
      //  data.forEach(function (e) {
      //    sum += (e - 127) * (e - 127);
      //  });
      //
      //  var v = Math.sqrt(sum / data.length) / 127;
      //  var baseTen = Math.log(Math.pow(10, v)) / Math.LN2;
      //  //console.log([v, baseTen]);
      //
      //  lastVolumes.push(v);
      //  lastVolumes.shift();
      //
      //  sum = 0;
      //  lastVolumes.forEach(function (e) {
      //    sum += e;
      //  });
      //
      //  var volume = sum / 2;
      //
      //  var height = totalHeight - volume * totalHeight;
      //  $volume.css('height', height + 'px')
      //}, 200);
      //
      //stopAudioAnalyzer = function () {
      //  clearInterval(volumeInterval);
      //
      //  analyser.disconnect();
      //  source.disconnect();
      //  audioCtx.close();
      //};
    }

    function onMediaError(e) {
      console.error('media error', e);
    }
  }


  function startRecording() {
    $('#preview').hide();
    $('#recording').show();
    fullscreen();

    //stopAudioAnalyzer();

    // setup recorder
    mediaRecorder = new MultiStreamRecorder(mediaStream);
    mediaRecorder.video = setupVideo;
    mediaRecorder.mimeType = 'video/webm';

    setupVideo.muted = true;
    audienceVideo.play();

    $.post(Urls['recordings:record'](se.project), {csrfmiddlewaretoken: crsf}).then(function (result) {
      console.log('recording: ' + result.id);

      mediaRecorder.ondataavailable = function (blobs) {
        console.log('data available');
        upload(result.id, blobs);
      };

      mediaRecorder.start(uploadInterval);
    });
  }


  function upload(id, blobs) {
    var video = blobs.video;
    var audio = blobs.audio;
    var formData = new FormData();

    console.log(blobs);

    formData.append('csrfmiddlewaretoken', crsf);
    if (audio && video.type.startsWith('video')) {
      formData.append('video', video);
    }
    if (audio && audio.type.startsWith('audio')) {
      formData.append('audio', audio);
    }

    uploadBlob(formData);

    function uploadBlob(data) {
      uploadQueue.push(data);

      if (uploadQueue.length == 1) {
        uploadPiece(); // upload when not waiting on other uploads
      }

      // this recursively goes through the queue and
      function uploadPiece() {
        if (uploadQueue.length > 0) {
          var data = uploadQueue[0];

          console.log('uploading', data);

          $.ajax({
            url: Urls['recordings:piece_upload'](se.project, id + ''),
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false
          }).then(function () {
            uploadQueue.shift(); // needs to be done after upload
            if (stopped) {
              progress(uploadQueue.length, uploadTotal);
            }

            uploadPiece();
          });

        } else if (stopped) { // send finish request
          $.ajax({
            url: Urls['recordings:record'](se.project),
            type: 'PUT',
            data: {
              recording: id,
              csrfmiddlewaretoken: crsf
            }
          }).then(function (response) {
            window.location.href = response;
          });
        }
      }
    }
  }


  function stopRecording() {
    exitFullscreen();

    $('#recording').hide();
    $('#finished').show();

    audienceVideo.pause();
    mediaRecorder.stop();
    mediaRecorder.stream.stop(); // recorder will stop the stream before the end of the current recording piece

    uploadTotal = uploadQueue.length;
    stopped = true;

    var progress = function progress(size, uploadTotal) {
      var $progressBar = $('#finished .uk-progress-bar');
      var progress = Math.floor((uploadTotal - size) * 100 / uploadTotal);

      $progressBar.css('width', progress + '%');
      $progressBar.text(progress + '%');
    };
  }


  function fullscreen() {
    var elem = $('#recording .s-recording-player')[0];

    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen();
    }
  }


  function exitFullscreen() {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }
})();
