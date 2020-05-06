import Vue from 'vue'
import App from './App.vue'
import router from './utils/router.js'
import apolloProvider from './utils/apolloClient.js'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import vuescroll from 'vuescroll';
import axios from 'axios'

Vue.use(vuescroll);

router.beforeEach((to, from, next) => {
  if(to.meta.title) {
    document.title = to.meta.title
  }
  next();
});

Vue.use(ElementUI);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.prototype.$axios = axios;
Vue.config.productionTip = false;

new Vue({
    router,
    apolloProvider,
    render: h => h(App)
}).$mount('#app');

