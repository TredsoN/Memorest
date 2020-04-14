import Router from 'vue-router'
import Index from '../components/Pages/Index.vue'
import SignInOrUp from '../components/Pages/SignInOrUp.vue'
import ChangeInformation from '../components/Pages/ChangeInformation.vue'
import Vue from "vue";


Vue.use(Router);


export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'index',
            component: Index,
        },
        {
            path: '/login',
            name: 'login',
            component: SignInOrUp,
        },
        {
            path: '/page1',
            name: 'page1',
            component: ChangeInformation,
        }
    ]
})