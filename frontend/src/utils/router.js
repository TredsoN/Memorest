import Vue from 'vue'
import Router from 'vue-router'
import Index from '../components/Pages/Index'

Vue.use(Router);


const router = new Router({
    mode: 'hash',
    routes: [
        {
            path: '/',
            name: 'index',
            component: Index,
            meta: {
                title: '记忆森林',
            }
        },
        {
            path: '/login',
            name: 'login',
            component: resolve=>(require(["../components/Pages/SignInOrUp"],resolve)),
            meta: {
                title: '登录'
            }
        },
        {
            path: '/select-subject',
            name: 'selectSubject',
            component: resolve=>(require(["../components/Pages/SelectSubject"],resolve)),
            meta: {
                title: '选择主题'
            }
        },
        {
            path: '/create-memory',
            name: 'createMemory',
            component: resolve=>(require(["../components/Pages/CreateMemory"],resolve)),
            meta: {
                title: '发布记忆'
            }
        },
        {
            path: '/personal',
            name: 'personal',
            component: resolve=>(require(["../components/Pages/PersonalPage"],resolve)),
            meta: {
                title: '个人中心'
            }
        },
        {
            path: '/infochange',
            name: 'infochange',
            component: resolve=>(require(["../components/Pages/InfoChangePage"],resolve)),
            meta: {
                title: '修改信息'
            }
        },
        {
            path: '/passwordchange',
            name: 'passwordchange',
            component: resolve=>(require(["../components/Pages/PasswordChangePage"],resolve)),
            meta: {
                title: '修改密码'
            }
        },
        {
            path: '/passwordfind',
            name: 'passwordfind',
            component: resolve=>(require(["../components/Pages/PasswordFindPage"],resolve)),
            meta: {
                title: '找回密码'
            }
        },
        {
            path: '/memoryinfo',
            name: 'memoryinfo',
            component: resolve=>(require(["../components/Pages/MemoryInfoPage"],resolve)),
            meta: {
                title: '记忆详情',
            }
        },
        {
            path: '/indexmemoryinfo',
            name: 'indexmemoryinfo',
            component: resolve=>(require(["../components/Pages/MemoryInfoPage2"],resolve)),
            meta: {
                title: '记忆详情',
            }
        },
        {
            path: '/mymemories',
            name: 'mymemories',
            component: resolve=>(require(["../components/Pages/MyMemoriesPage"],resolve)),
            meta: {
                title: '我的记忆'
            }
        },
        {
            path: '/myforgottenmemories',
            name: 'myforgottenmemories',
            component: resolve=>(require(["../components/Pages/MyDeadMemoriesPage"],resolve)),
            meta: {
                title: '遗忘记忆'
            }
        },
        {
            path: '/memorygrave',
            name: 'memorygrave',
            component: resolve=>(require(["../components/Pages/MemoryGravePage"],resolve)),
            meta: {
                title: '记忆公墓'
            }
        },
        {
            path: '/newsintro',
            name: 'newsintro',
            component: resolve=>(require(["../components/Pages/NewsIntroPage"],resolve)),
            meta: {
                title: '关于阿兹海默'
            }
        },
        {
            path: '/newsindex',
            name: 'newsindex',
            component: resolve=>(require(["../components/Pages/NewsIndexPage"],resolve)),
            meta: {
                title: '资讯列表'
            }
        },
        {
            path: '/newsinfo',
            name: 'newsinfo',
            component: resolve=>(require(["../components/Pages/NewsInfoPage"],resolve)),
            meta: {
                title: '资讯详情'
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