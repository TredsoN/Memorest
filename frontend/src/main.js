import Vue from 'vue'
import router from './router/router.js'
import Router from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'

Vue.use(Router);
Vue.use(ElementUI);
Vue.config.productionTip = false;

new Vue({
    render: h => h(App),
    router
}).$mount('#app');

