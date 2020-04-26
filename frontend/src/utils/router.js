import Vue from 'vue'
import Router from 'vue-router'
import Personal from '../components/Pages/PersonalPage.vue'
import InfoChange from '../components/Pages/InfoChangePage.vue'
import PasswordChange from '../components/Pages/PasswordChangePage.vue'
import PasswordFind from '../components/Pages/PasswordFindPage.vue'
import Index from '../components/Pages/Index'
import Login from '../components/Pages/SignInOrUp'
import MemoryInfo from '../components/Pages/MemoryInfoPage.vue'
import MyMemories from '../components/Pages/MyMemoriesPage.vue'

Vue.use(Router);


const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'index',
            component: Index,
            meta: {
                title: '记忆森林'
            }
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: {
                title: '登录'
            }
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
        },
        {
            path: '/memoryinfo',
            name: 'memoryinfo',
            component: MemoryInfo,
            meta: {
                title: '记忆详情'
            }
        },
        {
            path: '/mymemories',
            name: 'mymemories',
            component: MyMemories,
            meta: {
                title: '我的记忆'
            }
        }
    ]
});


router.beforeEach((to, meta, next) => {
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    next();
});


export default router;