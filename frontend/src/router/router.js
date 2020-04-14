import Router from 'vue-router'
import Index from '../components/Pages/Index.vue'
import SignInOrUp from '../components/Pages/SignInOrUp.vue'

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
        }
    ]
})