import axios from 'axios'
import router from '@/router'

const state = {
    auth: !!localStorage.getItem('token'), //controlla che sia presente il token, ritorna true o false
    level: '',
    username: ''
};
const getters = {
    getAuth: state =>{
        return state.auth
    },
    getLevel: state =>{
        return state.level
    },
    getUsername: state => {
        return state.username
    }
};
const mutations = {
    setAtuh: (state, authValue) =>{
        return state.auth = authValue
    },
    setLevel: (state, level) =>{
        return state.level = level
    },
    setUsername: (state, username) =>{
        return state.username = username
    },
};
const actions = {
    userInfo: (ctx) => {
        axios.get('/users/me').then((res) => {
            ctx.commit('setLevel', res.data.level);
            ctx.commit('setUsername', res.data.username);
        })
    },
    actSetAuth(ctx){
        ctx.commit('setAtuh', true);
    },
    checkAuth(ctx) {
        axios.get('/auth/check') // sostituisci con la tua API di verifica dell'autenticazione
          .then(response => {
            ctx.commit('setAtuh', true); // supponendo che l'API restituisca { authenticated: true }
          })
          .catch(error => {
            ctx.commit('setAtuh', false); // se la chiamata API fallisce, presumiamo che l'utente non sia autenticato
            router.push('/logout')
          });
      },
};

export default {
state,
getters,
mutations,
actions
}
