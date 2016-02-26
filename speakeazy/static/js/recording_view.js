(function () {
    var $videoContainer = $('.s-evaluation-player');
    var $video = $('.s-evaluation-player video');

    // controls
    var $controls = $('.s-video-controller');
    var $controlsBackground = $('.s-video-controller-background');
    var $play = $('.s-play-pause .uk-icon-play');
    var $pause = $('.s-play-pause .uk-icon-pause');
    var $volume = $('.s-video-volume');
    var $fullscreen = $('.s-video-fullscreen');
    var $time = $('.s-time-played');
    var $group = $('.s-group-submit');

    // slider controls
    var $slider = $('.s-slider');
    var $sliderBar = $('.s-slider-bar');
    var $played = $('.s-slider-played');
    var $buffered = $('.s-slider-buffered');

    // points
    var $points = $('.s-points');
    var $evaluations = $('.s-evaluation-list');
    var $evaluation = $('.s-evaluation').not('.s-evaluation-add');
    var $evaluationAdd = $('.s-create-evaluation');
    var $evaluationAddButton = $('.s-evaluation-add');
    var $evaluationAddType = $('.s-create-evaluation .uk-icon-button');

    // normal variables
    var pointTimes = [];
    var minDistance = 0;
    var absoluteMinDistance = 1;

    //$controls.hide();
    $play.hide();
    setTimeout(startBuffer, 500);

    $video[0].load();
    $video[0].ondurationchange = createEvaluations;

    $video.on('timeupdate', function () {
        calculateSlider();
        $time.text(calculateTime($video[0].currentTime));
        showEvaluations();
    });

    $videoContainer.hover(function () {}, $.debounce(600, function () {
        hideControls();
    }));

    $videoContainer.mousemove(showControls);

    $videoContainer.mousestop(hideControls, {
        timeToStop: null,   // the amount of time the stop event has to run before it will not run at all anymore
        delayToStop: '800', // the delay for what is considered a "stop"
        onMouseout: null,   // function to run when we mouseout of our element
        onStopMove: null    // function to run when we start moving again after the stop
    });

    $controlsBackground.click(playPause);
    $play.parent().click(playPause);
    //$play.click(play);
    //$pause.click(pause);

    $sliderBar.mousedown(function (event) {
        $(this).data('mousedown', true);
        changeCurrentTime(event);
    });

    $sliderBar.mousemove(function (event) {
        if ($(this).data('mousedown')) {
            changeCurrentTime(event)
        }
    });

    $sliderBar.mouseup(function () {
        $(this).data('mousedown', false);
    });

    $sliderBar.mouseleave(function () {
        $(this).data('mousedown', false);
    });

    $slider.mousemove(function (event) {
        if (event.pageX < $slider.offset().left || event.pageX > $slider.offset().left + $slider.width()) {
            $(this).data('mousedown', false);
        }
    });

    $slider.mouseleave(function () {
        $sliderBar.data('mousedown', false);
    });

    $volume.click(function () {
        $video[0].muted = !$video[0].muted;
    });


    $fullscreen.click(function () {
        var elem = $videoContainer[0];

        //if (isFullscreen) {
        //    $(this).removeClass('s-active');
        //
        //    if (elem.exitFullscreen) {
        //        elem.exitFullscreen();
        //    } else if (elem.mozCancelFullScreen) {
        //        elem.mozCancelFullScreen();
        //    } else if (elem.webkitExitFullscreen) {
        //        elem.webkitExitFullscreen();
        //    } else if (elem.msExitFullscreen) {
        //        elem.msExitFullscreen();
        //    }
        //
        //} else {
        //$(this).addClass('s-active');

        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen();
        }
        //}
    });

    $evaluations.click(function () {
        pause();
    });

    $evaluationAddType.click(function () {
        var $type = $(this);

        var $input = $evaluationAdd.find('textarea');
        var text = $input.val();
        var type = $(this).attr('data-type');
        var time = Math.floor($video[0].currentTime);

        sendEval(type, text, time, function () {
            $input.val('');

            addPoint(time);

            addEvaluation({
                evaluator: se.user,
                text: text,
                icon: $type.attr('class').split(/\s+/)[0],
                time: time
            });
        });
    });

    $group.click(function () {
        var data = {
            action: 'request',
            group: $(this).attr('data-group'),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        };

        $.post('/projects/p/' + se.project + '/' + se.recording + '/', data, function () {
            // success notification
        });
    });


    /**
     * Updates the buffered bar in the case of the video being paused
     */
    function startBuffer() {
        var currentTime = $video[0].currentTime;
        var currentBuffer = $video[0].buffered.end(0);
        var maxDuration = $video[0].duration;
        var percentage = 100 * (currentBuffer - currentTime) / maxDuration;

        $buffered.css('width', percentage + '%');

        if (currentBuffer < maxDuration) {
            setTimeout(startBuffer, 500);
        }
    }

    /**
     * Calculates the correct width of the played and buffered time bars
     */
    function calculateSlider() {
        var currentTime = $video[0].currentTime;
        var currentBuffer = $video[0].buffered.end(0);
        var maxDuration = $video[0].duration;
        var playedPercentage = 100 * currentTime / maxDuration;
        var bufferedPercentage = 100 * (currentBuffer) / maxDuration - playedPercentage;

        $played.css('width', playedPercentage + '%');
        $buffered.css('width', bufferedPercentage + '%');
    }

    /**
     * Set the current video time from the mouse position
     * @param event jquery event
     */
    function changeCurrentTime(event) {
        var x = event.pageX - $sliderBar.offset().left;
        $video[0].currentTime = x / $sliderBar.width() * $video[0].duration;
        calculateSlider();
    }

    /**
     * Pause the video and update relevant elements
     */
    function play() {
        $pause.show();
        $play.hide();
        $video[0].play();

        setTimeout(hideControls, 1200);
    }

    /**
     * Pause the video and update relevant elements
     */
    function pause() {
        $play.show();
        $pause.hide();
        $video[0].pause();

        showControls();
    }

    /**
     * Toggles playing and pausing the video
     */
    function playPause() {
        if ($video[0].paused) {
            play();
        } else {
            pause();
        }
    }

    /**
     * Hide control overlay if not paused
     */
    function hideControls() {
        if (!$video[0].paused) {
            $controls.addClass('uk-animation-fade');
            $videoContainer.css('cursor', 'none');
        }
    }

    /**
     * Show control overlay no matter what
     */
    function showControls() {
        $controls.removeClass('uk-animation-fade');
        $videoContainer.css('cursor', 'default');
    }

    /**
     * Calculates the time and returns an [h:]m:ss representation of it
     * @param totalSeconds time in seconds
     * @returns {string} [h:]m:ss
     */
    function calculateTime(totalSeconds) {
        var hours = Math.floor(totalSeconds / (60 * 60));

        var divisor_for_minutes = totalSeconds % (60 * 60);
        var minutes = Math.floor(divisor_for_minutes / 60);
        var seconds = Math.floor(divisor_for_minutes % 60);

        if (seconds < 10) {
            seconds = '0' + seconds;
        }

        if (hours > 0) {
            return hours + ':' + minutes + ':' + seconds;
        } else {
            return minutes + ':' + seconds;
        }
    }

    function sendEval(type, text, time, sendCallback) {
        var data = {
            action: 'eval',
            type: type,
            text: text,
            seconds: time,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        };

        $.post('/projects/p/' + se.project + '/' + se.recording + '/', data, function () {
            sendCallback();
        });
    }

    function createEvaluations() {
        $video[0].ondurationchange = null;

        minDistance = 15 / $sliderBar.width() * $video[0].duration;
        minDistance = minDistance > absoluteMinDistance ? minDistance : absoluteMinDistance;

        var lastTime;

        evaluations.map(function (evaluation) {
            addPoint(evaluation.time);

            addEvaluation(evaluation).hide();
        });
    }

    function addPoint(time) {
        var createPoint = true;
        pointTimes.map(function (point) {
            if (Math.abs(time - point) < minDistance) {
                createPoint = false;
            }
        });

        if (!createPoint) {
            return;
        }

        pointTimes.push(time);

        var $point = $('<i class="uk-icon-caret-down uk-icon-small uk-icon-hover" data-uk-tooltip="{pos:\'top\'}">');
        $point.attr('title', calculateTime(time));

        var duration = $video[0].duration;

        time += 0.5;
        time = time < duration ? time : duration;

        var timeScalar = time / duration; // use the middle of the second
        var position = Math.floor($sliderBar.parent().width() * timeScalar - 6);
        $point.css('left', position + 'px');

        $points.append($point);

        $point.click(function () {
            pause();

            $video[0].currentTime = time;
            calculateSlider();
        });
    }

    function addEvaluation(evaluation) {
        var $newEvaluation = $('<div class="s-evaluation" data-uk-dropdown="{mode:\'click\', pos:\'right-top\'}">');
        $newEvaluation.attr('data-time', evaluation.time);

        var $icon = $('<i class="uk-icon-hover">');
        $icon.addClass(evaluation.icon);

        var $content = $('<div class="uk-dropdown uk-dropdown-scrollable uk-panel uk-panel-header">');

        var $user = $('<div class="uk-panel-title">');
        $user.text(evaluation.evaluator);

        var $text = $('<p>');
        $text.text(evaluation.text);

        var $date = $('<p>');

        $content.append($user);
        $content.append($text);
        $content.append($date);

        $newEvaluation.append($icon);
        $newEvaluation.append($content);

        $evaluations.append($newEvaluation);
        $evaluation.push($newEvaluation);

        return $newEvaluation;
    }

    function showEvaluations() {
        var time = Math.floor($video[0].currentTime);

        $evaluation.each(function (i, $e) {
            var pos = parseInt($e.attr('data-time'), 10) + 0.5;
            if (Math.abs(pos - time) <= minDistance) { // one of the few times to use rough equality
                $e.show();
            } else {
                $e.hide();
            }
        });
    }
})();
