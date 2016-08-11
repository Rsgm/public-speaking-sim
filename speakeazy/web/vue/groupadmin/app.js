import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './routes.js'
import SelectInput from '../components/select/SelectInput.vue'

Vue.use(VueRouter);


// register reusable components here
Vue.component('select-input', SelectInput);


// routing
var router = new VueRouter({
  history: true,
  root: '/groups/admin',
  saveScrollPosition: true
});
router.mode = 'html5';

router.map(routes);


router.start(Vue.extend({}), 'body');
