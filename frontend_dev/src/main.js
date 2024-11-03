import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store/index.js'
import './plugins/base'
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css'; //importa i css

// AXIOS
import axios from 'axios';
import https from 'https';

// Configura axios per ignorare i certificati autofirmati
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;
axios.defaults.httpsAgent = new https.Agent({ rejectUnauthorized: false });

// Intercettore delle richieste
axios.interceptors.request.use((config) => {
   let token = localStorage.getItem('token');
   if (token) {
     config.headers['Authorization'] = `Bearer ${token}`;
   }
   return config;
}, (error) => {
   return Promise.reject(error);
});

axios.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response.status === 401) {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    }

    return Promise.reject(error);
})

// NOTIFICHE
// import Toasted from 'vue-toasted';
// Vue.use(Toasted);

// Configurazione delle opzioni di Toastification
const options = {
    position: "top-right",
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    closeButton: "button",
    icon: true,
    rtl: false
 };

 Vue.use(Toast, options);

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
