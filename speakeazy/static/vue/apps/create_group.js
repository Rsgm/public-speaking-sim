(function () {
  'use strict';

  new Vue({
    el: '#group-form',

    data: {
      showRoles: false
    },

    events: {
      'end-selected': function (name) {
        this.showRoles = true;
        console.log(this.show)
      },
      'end-deselected': function (name) {
        if ('default-roles')
          this.showRoles = false;
      }
    }
  });

})();
