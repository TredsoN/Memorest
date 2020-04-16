import Vue from 'vue'
import Router from 'vue-router'
import Personal from '../components/Pages/PersonalPage.vue'
import InfoChange from '../components/Pages/InfoChangePage.vue'
import PasswordChange from '../components/Pages/PasswordChangePage.vue'
import PasswordFind from '../components/Pages/PasswordFindPage.vue'
import Index from '../components/Pages/Index'
import Login from '../components/Pages/SignInOrUp'

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
            component: Login,
        },
        {
            path: '/personal',
            name: 'personal',
            component: Personal,
            meta: {
                title: '个人中心'
            }
        },
        {
            path: '/infochange',
            name: 'infochange',
            component: InfoChange,
            meta: {
                title: '修改信息'
            }
        },
        {
            path: '/passwordchange',
            name: 'passwordchange',
            component: PasswordChange,
            meta: {
                title: '修改密码'
            }
        },
        {
            path: '/passwordfind',
            name: 'passwordfind',
            component: PasswordFind,
            meta: {
                title: '找回密码'
            }
        }
    ]
});