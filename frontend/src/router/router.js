import Vue from 'vue'
import Router from 'vue-router'
import Test from '../components/Pages/Test.vue'
import ChangeInformation from '../components/Pages/ChangeInformation.vue'

Vue.use(Router)

export default new Router({
    routes: [
      {
        path: '/',
        name: 'test',
        component: Test,
      },
      {
        path: '/page1',
        name: 'page1',
        component: ChangeInformation,
      }
    ]
  })