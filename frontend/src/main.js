import Vue from 'vue'
import App from './App.vue'
import router from './utils/router.js'
import apolloProvider from './utils/apolloClient.js'

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  if(to.meta.title) {
    document.title = to.meta.title
  }
  next();
})

new Vue({
  router,
  apolloProvider,
  render: h => h(App),
}).$mount('#app')
