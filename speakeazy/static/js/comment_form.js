(function () {
  $('.comment-form button').click(function () {
    var text = $('.comment-form textarea').val();
    $.post(Urls['recordings:recording:comments:create'](se.project, se.recording), {
      text: text,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }, function () {
      var $list = $('.uk-comment-list');
      var $comment = $('<li class="uk-comment">' +
          '<header class="uk-comment-header">' +
          '<h4 class="uk-comment-title">' + se.user + '</h4>' +
          '<div class="uk-comment-meta">' + moment().format('MMMM D, YYYY, h:mm a') + '</div>' +
          '</header>' +
          '<div class="uk-comment-body">' + text + '</div>' +
          '</li>');
      $list.append($comment);
    });
  });
})();