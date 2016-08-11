import Vue from 'vue'



// register reusable components here
Vue.component('select-input', SelectInput);


new Vue({
  el: 'body',

  // register apps here
  components: {
    createGroup: CreateGroup
  }
});
