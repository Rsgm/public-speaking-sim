// thumbnail hover effect
$('#recent-recordings .uk-flex > div').hover(function () {
    $(this).find('video').get(0).play();
}, function () {
    var video = $(this).find('video').get(0);
    video.pause();
    video.currentTime = 0
});
