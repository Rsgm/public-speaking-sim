// thumbnail hover effect
$('a.s-list-item').not('.s-list-add').each(function () {
    $(this).hover(function () {
        $(this).find('video').get(0).play();
    }, function () {
        var video = $(this).find('video').get(0);
        video.pause();
        video.currentTime = 0
    });
});
