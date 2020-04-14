import Vue from 'vue'
import router from './router/router.js'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import apolloProvider from './graphql/apollo'
import App from './App.vue'


Vue.use(ElementUI);
Vue.config.productionTip = false;


new Vue({
    router,
    apolloProvider,
    render: h => h(App)
}).$mount('#app');

