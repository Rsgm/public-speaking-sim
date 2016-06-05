(function () {
  'use strict';

  var selectChoice = Vue.extend({
    data: function () {
      return {
        selected: false
      }
    },

    props: ['choice', 'radio'],

    methods: {
      click: function () {
        this.selected = true;
        this.$dispatch('select', this.choice.id);
      }
    },

    events: {
      'deselect-others': function (choice) {
        this.selected = this.choice.id === choice;
      },
      'deselect': function (choice) {
        if (this.choice.id === choice) {
          this.selected = false;
        }
      }
    },

    template: '<div @click="click" :class="{selected: selected, deselected: !selected}">' +

    '<h4>{{* choice.name }}</h4>' +
    '<p>{{* choice.description }}</p>' +

    '<ul class="uk-list" v-if="choice.list">' +
    '<li v-for="li in choice.list">{{* li }}</li>' +
    '</ul>' +

    '</div>'
  });


  Vue.component('selectInput', {
    data: function () {
      return {
        selected: []
      }
    },

    props: [
      'name',
      'choices', // in json form
      'multiple', // single or multiple select
      'required',
      'end'
    ],

    events: {
      'select': function (choice) {
        if (!this.multiple) {
          this.selected = choice;
          this.$broadcast('deselect-others', choice);
        } else if (this.selected.indexOf(choice) === -1) {
          this.selected.push(choice);
        } else {
          this.selected.$remove(choice);
          this.$broadcast('deselect', choice);
        }

        if (this.end) {
          var event = this.end.id === choice ? 'end-selected' : 'end-deselected';
          this.$dispatch(event, this.name)
        }
      }
    },

    template: '<div>' +

    '<select-choice v-for="choice in choices" :choice="choice"></select-choice>' +
    '<select-choice v-if="end" class="end" :choice="end"></select-choice>' +

    '<input type="hidden" name="{{* name }}" v-model="selected" required="{{* required }}">' +
    '</div>',

    components: {
      'select-choice': selectChoice
    }
  });

})();
