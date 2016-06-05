(function () {
  $('.s-selected').each(function () {
    var $input = $(this).find('input');

    $(this).find('a').click(function () {
      var $last = $('#_form > .s-selected')
      $last.removeClass('s-selected');

      if (this !== $last) {
        $(this).addClass('s-selected');
        $input.val($(this).attr('data-value'));
      } else {
        $input.val(-1);
      }
    });
  });
})();
