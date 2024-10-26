import Vue from 'vue'
import Router from 'vue-router'
import store from './store/index.js'


Vue.use(Router)

export default new Router({
    mode: 'hash',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            redirect: 'dashboard/dashboard',
            component: () => import('@/layouts/Layout'),
            beforeEnter: (to, from, next) => {
                if (store.state.user.auth) {
                    next();
                } else {
                    next('/login');
                }
            },
            children: [
                // Components

                {
                    name: 'Profile',
                    path: 'pages/profile',
                    component: () => import('@/views/pages/Profile'),
                },
                {
                    name: 'Dashboard',
                    path: 'dashboard/dashboard',
                    component: () => import('@/views/dashboard/Dashboard'),
                },
                {
                    name: 'Recheck',
                    path: 'dashboard/recheck/:nomeApp/:cliente',
                    props: true,
                    component: () => import('@/views/dashboard/Recheck'),
                },
                
                {
                    name: 'RecheckList',
                    path: 'list/recheck',
                    component: () => import('@/views/pages/RecheckList'),
                },
                
                {
                    name: 'ListRemediation',
                    path: 'list/remediation',
                    component: () => import('@/views/pages/AuditsList'),
                },        

            ]
        },
        {
            path: '/admin',
            component: () => import('@/layouts/Layout'),
            beforeEnter: (to, from, next) => {
                if (store.state.user.auth) {
                    if(store.state.user.role != 'admin'){
                        next('/');
                    }else{
                        next();
                    }
                } else {
                    next('/login');
                }
            },
            children: [
                {
                    name: 'Users',
                    path: 'users',
                    component: () => import('@/views/pages/Users'),
                },
                
            ],
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/pages/Login'),

        },
        {
            path: '/logout',
            name: 'logout',
            component: () => import('@/views/Logout'),
            
        }

    ],
})