(function () {
    var $videoContainer = $('.s-video');
    var $video = $('.s-video-element');

    // controls
    var $controls = $('.s-video-controls'); // play and pause
    var $play = $('.s-video-play .fa-play'); // play and pause
    var $pause = $('.s-video-play .fa-pause'); // play and pause
    var $volume = $('.s-video-volume');
    var $fullscreen = $('.s-video-fullscreen');

    // slider controls
    var $position = $('.s-video-slider-position');
    var $played = $('.s-video-slider-played');
    var $buffered = $('.s-video-slider-buffered');

    $controls.hide();
    $play.hide();
    $video[0].play();

    $videoContainer.hover(function () {
        $controls.show();
    }, function () {
        $controls.hide();
    });

    $play.click(play);
    $pause.click(pause);

    $volume.click(function () {
        $video[0].muted = !$video[0].muted;
    });

    $video.click(function () {
        if ($video[0].paused) {
            play();
        } else {
            pause();
        }
    });

    $video.on('timeupdate', function () {
        var currentPos = $video[0].currentTime; //Get currenttime
        var maxDuration = $video[0].duration; //Get video duration
        var percentage = 100 * currentPos / maxDuration; //in %
        $position.css('left', (percentage - $position.width / 2) + '%');
        $played.css('width', percentage + '%');
    });

    var startBuffer = function () {
        var currentBuffer = $video[0].buffered.end(0); //Get currenttime
        var maxDuration = $video[0].duration; //Get video duration
        var percentage = 100 * currentBuffer / maxDuration; //in %
        $buffered.css('left', percentage + '%');

        if (currentBuffer < maxDuration) {
            setTimeout(startBuffer, 500);
        }
    };

    setTimeout(startBuffer, 500);

    function play() {
        $pause.show();
        $play.hide();
        $video[0].play()
    }

    function pause() {
        $play.show();
        $pause.hide();
        $video[0].pause();
    }
})();
