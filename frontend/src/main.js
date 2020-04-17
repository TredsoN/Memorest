import Vue from 'vue'
import App from './App.vue'
import router from './utils/router.js'
import apolloProvider from './utils/apolloClient.js'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';


router.beforeEach((to, from, next) => {
  if(to.meta.title) {
    document.title = to.meta.title
  }
  next();
});

Vue.use(ElementUI);
Vue.config.productionTip = false;


new Vue({
    router,
    apolloProvider,
    render: h => h(App)
}).$mount('#app');

