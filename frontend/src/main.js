import Vue from 'vue'
import router from './router/router.js'
import Router from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import ApolloClient from 'apollo-boost'
import VueApollo from 'vue-apollo'
import App from './App.vue'

Vue.use(VueApollo);
Vue.use(Router);
Vue.use(ElementUI);
Vue.config.productionTip = false;

const apolloClient = new ApolloClient({
    uri: 'http://localhost:3000/graphql'
});

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
});

new Vue({
    router,
    apolloProvider,
    render: h => h(App)
}).$mount('#app');

