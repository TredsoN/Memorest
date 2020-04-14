import Vue from 'vue'
import Router from 'vue-router'
import Test from '../components/TredsonPage/Test.vue'

Vue.use(Router)

export default new Router({
    routes: [
      {
        path: '/test',
        name: 'test',
        component: Test,
      }
    ]
  })