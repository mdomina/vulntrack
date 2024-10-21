import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store/index.js'
import './plugins/base'

// AXIOS
import axios from 'axios';
//dev
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;
//prod
axios.interceptors.request.use((config) => {
   let token = localStorage.getItem('token');
   if (token) {
     config.headers['Authorization'] = `Bearer ${token}`;
   }
   return config;
}, (error) => {
   return Promise.reject(error);
});

/*axios.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response.status === 401) {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    }

    return Promise.reject(error);
});*/


// NOTIFICHE
import Toasted from 'vue-toasted';
Vue.use(Toasted);


//GRAFICI
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)


Vue.config.productionTip = false

new Vue({
    vuetify,
    store,
    router,
    render: h => h(App)
}).$mount('#app')
