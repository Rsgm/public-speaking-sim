(function () {
  var stopped;

  var mediaStream;
  var setupVideo;
  var audienceVideo;
  var stopAudioAnalyzer;

  var mediaRecorder;

  var uploadInterval = 3000;
  var crsf = $('input[name=csrfmiddlewaretoken]').val();

  var ws = new WebSocket('ws://0.0.0.0:1500', 'sync');
  // var ws2 = new WebSocket('ws://0.0.0.0:1500', 'async');

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
      url = window.URL.createObjectURL(mediaStream);

      console.log(mediaStream);

      setupVideo = $('#setup-video').get(0);
      setupVideo.src = url;
      setupVideo.muted = true;
      setupVideo.play();

      audienceVideo = $('#audience-video').get(0);
      audienceVideo.pause();

      $('#preview').show();


      var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      var source = audioCtx.createMediaStreamSource(stream);
      var analyser = audioCtx.createAnalyser();
      source.connect(analyser);

      var $volume = $('#volume-slider');
      var totalHeight = $volume.parent().height();

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

    setupVideo.muted = true;
    audienceVideo.play();

    $.post('/recordings/record/' + se.project + '/', {request: 'start', csrfmiddlewaretoken: crsf}, function (result) {
      ws.send(result);

      // setup recorder and start recording
      mediaRecorder = new MultiStreamRecorder(mediaStream);
      mediaRecorder.video = setupVideo;

      mediaRecorder.ondataavailable = function (blobs) {
        upload(blobs.video, blobs.audio);
      };

      mediaRecorder.start(uploadInterval);
    });
  }

  function stopRecording() {
    exitFullscreen();

    $('#recording').hide();
    $('#finished').show();

    audienceVideo.pause();
    mediaRecorder.stop();

    stopped = true;

    ws.onmessage = function (event) {
      var data = JSON.parse(event.data);
      
    };

    var progress = function progress(size, uploadTotal) {
      var $progressBar = $('#finished .uk-progress-bar');
      var progress = Math.floor((uploadTotal - size) * 100 / uploadTotal);

      $progressBar.css('width', progress + '%');
      $progressBar.text(progress + '%');
    };
  }


  function upload(video, audio) {
    console.log({
      video: video,
      audio: audio
    });

    if (video.type.startsWith("video")) {
      ws.send(video);
    }

    if (audio.type.startsWith("audio")) {
      ws.send(audio);
    }

    if (stopped) {
      ws.send(JSON.stringify({finished: true}));
    }
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
