(function () {
  'use strict';

  new Vue({
    el: '#group-form',

    data: {
      showRoles: false
    },

    props: [
      'hide'
    ],

    events: {
      'end-selected': function (name) {
        if (name === this.hide) {
          this.showRoles = true;
        }
      },
      'end-deselected': function (name) {
        if (name === this.hide) {
          this.showRoles = false;
        }
      }
    }
  });

})();
