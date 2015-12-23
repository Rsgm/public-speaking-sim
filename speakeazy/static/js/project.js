(function () {
    // set up breadcrumbs
    var path = location.pathname.split('/');
    var subPath = '/';

    for (var i = 0; i < path.length; i++) {
        if (path[i] === '') {
            continue;
        }

        var p = path[i];
        subPath += p + '/';
        var $element = $('<li>');

        if (subPath === location.pathname) {
            $element.addClass('active');
            $element.text(p);
        } else {
            var $link = $('<a>');
            $link.attr('href', subPath);
            $link.text(p);

            $element.append($link);
        }

        $('.breadcrumb').append($element);
    }
})();
