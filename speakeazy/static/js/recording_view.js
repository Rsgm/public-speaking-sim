(function () {
    var $videoContainer = $('.s-video');
    var $video = $('.s-video-element');

    // controls
    var $controls = $('.s-video-controls'); // play and pause
    var $play = $('.s-video-play .fa-play'); // play and pause
    var $pause = $('.s-video-play .fa-pause'); // play and pause
    var $volume = $('.s-video-volume');
    var $fullscreen = $('.s-video-fullscreen');
    var $position = $('.s-video-position');
    var $duration = $('.s-video-duration');

    // slider controls
    var $slider = $('.s-video-slider');
    var $sliderBar = $('.s-video-slider-bar');
    var $played = $('.s-video-slider-played');
    var $buffered = $('.s-video-slider-buffered');

    // points
    var $points = $('.s-video-points');
    var $pointer = $('.s-video-pointer');
    var $marker = $('.s-video-marker');
    var $markerContainer = $('.s-video-marker-container');
    var $eval = $('.s-video-eval, .s-video-eval-add');
    var $evalMenu = $('.s-video-eval-menu');
    var $evalAddTypes = $('.s-video-eval-add-types');

    var project = window.location.pathname.split('/')[2];
    var recording = window.location.pathname.split('/')[3];

    $duration.text(calculateTime($video[0].duration));
    //$controls.hide();
    $play.hide();
    $pointer.hide();
    //$video[0].play();
    setTimeout(startBuffer, 500);
    $markerContainer.hide();
    $evalMenu.hide();

    $marker.each(function () {
        updateMarker($(this));
        addEvalAddTypes($(this));
        addMarkerHandlers($(this));
    });

    //$videoContainer.hover(function () {
    //    $controls.show();
    //}, function () {
    //    $controls.hide();
    //});
    $play.click(play);
    $pause.click(pause);

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
            $pointer.hide();
            $(this).data('mousedown', false);
        } else {
            $pointer.offset({left: event.pageX - $pointer.width() / 2});
        }
    });

    $slider.mouseleave(function () {
        $(this).find('.s-video-slider-bar').data('mousedown', false);
        $pointer.hide();
    });

    $slider.mouseenter(function () {
        $pointer.show()
    });

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
        calculateSlider();
        $position.text(calculateTime($video[0].currentTime));
    });

    $fullscreen.click(function () {
        var elem = $videoContainer[0];
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen();
        }
    });

    $pointer.click(function (event) {
        $(this).hide();
        changeCurrentTime(event);
        createMarker();
    });

    $pointer.mouseleave(function () {
        $(this).find('.s-video-marker-container').hide();
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
        var bufferedPercentage = 100 * (currentBuffer - currentTime) / maxDuration;

        $played.css('width', playedPercentage + '%');
        $buffered.css('width', bufferedPercentage + '%');
    }

    /**
     * Set the current video time from the mouse position
     * @param event jquery event
     */
    function changeCurrentTime(event) {
        var x = event.pageX - $slider.offset().left;
        $video[0].currentTime = x / $slider.width() * $video[0].duration;
        calculateSlider();
    }

    /**
     * Pause the video and update relevant elements
     */
    function play() {
        $pause.show();
        $play.hide();
        $video[0].play()
    }

    /**
     * Pause the video and update relevant elements
     */
    function pause() {
        $play.show();
        $pause.hide();
        $video[0].pause();
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
        var seconds = Math.ceil(divisor_for_minutes % 60);

        if (seconds < 10) {
            seconds = '0' + seconds;
        }

        if (hours > 0) {
            return hours + ':' + minutes + ':' + seconds;
        } else {
            return minutes + ':' + seconds;
        }
    }

    /**
     * Updates the position of the marker
     * @param $m the marker in which to update the position
     */
    function updateMarker($m) {
        var played = $m.attr('data-position') / $video[0].duration;
        var position = Math.floor($m.parent().width() * played - $m.width() / 2);

        $m.css('left', position + 'px');
    }

    /**
     * Creates a new marker at the current video time
     */
    function createMarker() {
        // check for another marker at this position

        var $newMarker = $('<div class="s-video-marker">');
        $newMarker.attr('data-position', Math.floor($video[0].currentTime));

        $newMarker.append($('<div class="fa fa-caret-down fa-lg">'));
        $newMarker.append($('<div class="fa fa-caret-up fa-lg">'));

        var $newMarkerConainer = $('<div class="s-video-marker-container">');
        var $newMarkerAdd = $('<div class="s-video-eval-add fa fa-plus-square-o">');
        var $newMarkerMenu = $('<div class="s-video-eval-menu">');
        $newMarkerMenu.append('<div class="fa fa-caret-left">');
        $newMarkerMenu.append('<div class="fa fa-caret-right">');
        $newMarkerMenu.append('<div class="s-video-eval-add-types">');

        var $newMarkerContent = $('<div class="s-video-eval-content">');
        $newMarkerContent.append('<input type="text" title="Add evaluation">');
        $newMarkerContent.append('<i class="fa fa-share-square">');

        $points.append($newMarker);
        $newMarker.append($newMarkerConainer);
        $newMarkerConainer.append($newMarkerAdd);
        $newMarkerAdd.append($newMarkerMenu);
        $newMarkerMenu.append($newMarkerContent);

        $newMarkerMenu.hide();
        $newMarkerContent.hide();

        updateMarker($newMarker);
        addEvalAddTypes($newMarker);
        addEvalAddHandlers($newMarker);

        addMarkerSendHandlers($newMarker, function () {
            $newMarker.off();
            addMarkerHandlers($newMarker);
        });

        $newMarker.mouseleave(function () {
            $newMarker.remove();
        });
    }

    /**
     * Add jquery handlers to marker events
     * @param $m marker in which to add events
     * @param sendCallback function to run after sending
     */
    function addMarkerHandlers($m, sendCallback) {
        $m.hover(function () {
            $(this).find('.s-video-marker-container').show();
            updateMarker($(this));
            $pointer.hide();
        }, function () {
            $(this).find('.s-video-marker-container').hide();
            updateMarker($(this));
            $pointer.show();
        });

        $m.find('.s-video-eval').hover(function () {
            $(this).find('.s-video-eval-menu').show();
        }, function () {
            $(this).find('.s-video-eval-menu').hide();
        });

        addEvalAddHandlers($m);
        addMarkerSendHandlers($m, sendCallback);
    }

    function addMarkerSendHandlers($m, sendCallback) {
        $m.find('.s-video-eval-add .fa-share-square').click(function () {
            sendEval($m, sendCallback);
        });

        $m.find('.s-video-eval-add input').keypress(function (event) {
            if (event.which == '13') {
                sendEval($m, sendCallback);
            }
        });
    }

    function sendEval($m, sendCallback) {
        var data = {
            type: $m.find('.s-video-eval-add').data('type'),
            text: $m.find('.s-video-eval-content > input').val(),
            seconds: $m.attr('data-position'),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        };

        $.post('/projects/' + project + '/' + recording + '/evaluate/', data, function () {
            sendCallback();
        });
    }

    function addEvalAddHandlers($m) {
        $m.find('.s-video-eval-add').hover(function () {
            $(this).find('.s-video-eval-menu').show();
            $(this).find('.s-video-eval-add-types').show();
        }, function () {
            $(this).find('.s-video-eval-menu').hide();
            $(this).find('.s-video-eval-add-types').hide();
            $(this).find('.s-video-eval-content').hide();
            $m.find('.s-video-eval-add').data('type', undefined);
        });

        $m.find('.s-video-eval-add-types > a').click(function () {
            $m.find('.s-video-eval-add').data('type', $(this).data('type'));
            $m.find('.s-video-eval-add-types').hide();
            $m.find('.s-video-eval-content').show();
        });
    }

    function addEvalAddTypes($m) {
        var $types = $m.find('.s-video-eval-add-types');

        for (var i = 0; i < evaluationTypes.length; i++) {
            var t = evaluationTypes[i];
            var $type = $('<a class="fa">');
            $type.addClass(t.fa_class);
            $type.css('background', '#' + t.color);
            $type.data('type', t.name);
            $types.append($type);
        }

        $types.hide();
    }
})();
