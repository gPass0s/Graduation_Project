// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable */
import Vue from 'vue';
import App from './App';
import router from './router';
import money from 'v-money';
import axios from 'axios';

Vue.use(money, {
	decimal: ',',
	thousands: '.',
	precision: 2,
	masked: false /* doesn't work with directive */
});

Vue.config.productionTip = false;

Vue.prototype.$axios = axios;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
