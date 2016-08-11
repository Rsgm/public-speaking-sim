import Vue from 'vue'

import CreateGroup from './apps/CreateGroup.vue'
import SelectInput from './components/select/SelectInput.vue'


// register reusable components here
Vue.component('select-input', SelectInput);


new Vue({
  el: 'body',

  // register apps here
  components: {
    createGroup: CreateGroup
  }
});
