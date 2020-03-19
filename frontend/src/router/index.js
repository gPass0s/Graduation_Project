import Vue from 'vue';
import Router from 'vue-router';
import PrevisaoComponent from '@/components/PrevisaoComponent';

Vue.use(Router);

export default new Router({
	routes: [
    	{
	      path: '/',
	      name: 'PrevisaoComponent',
	      component: PrevisaoComponent,
    	},
 	],
});
