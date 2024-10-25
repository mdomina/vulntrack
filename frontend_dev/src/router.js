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
                    name: 'Alerts',
                    path: 'pages/alerts',
                    component: () => import('@/views/pages/Alerts'),
                },

                {
                    name: 'Profile',
                    path: 'pages/profile',
                    component: () => import('@/views/pages/Profile'),
                },

                {
                    name: 'Icons',
                    path: 'pages/icons',
                    component: () => import('@/views/pages/Icons'),
                },

                {
                    name: 'TableSimple',
                    path: 'pages/tables-simple',
                    component: () => import('@/views/pages/TableSimple'),
                },

                {
                    name: 'BasciDashboard',
                    path: 'dashboard/basic-dashboard',
                    component: () => import('@/views/dashboard/BasicDashboard'),
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
                    name: 'Upload',
                    path: 'upload/remediation',
                    component: () => import('@/views/pages/Upload'),
                },
                {
                    name: 'RemediationUploaded',
                    path: 'uploaded/remediation',
                    component: () => import('@/views/pages/RemediationUploaded'),
                },
                {
                    name: 'ListRemediation',
                    path: 'list/remediation',
                    component: () => import('@/views/pages/RemediationList'),
                },

                {
                    name: 'AdminDashboard',
                    path: 'dashboard/AdminDashboard',
                    component: () => import('@/views/pages/AdminDashboard'),
                },

            ]
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