// src/store/modules/user.js

import axios from 'axios';
import router from '@/router';

const state = {
    auth: !!localStorage.getItem('token'),
    role: '',
    username: '',
    email: '', // Aggiungi `email` allo stato
    user: null,
};

const getters = {
    getAuth: (state) => state.auth,
    getLevel: (state) => state.role,
    getUsername: (state) => state.username,
    getEmail: (state) => state.email, // Getter per l'email
    getUser: (state) => state.user,
};

const mutations = {
    setAuth: (state, authValue) => (state.auth = authValue),
    setLevel: (state, role) => (state.role = role),
    setUsername: (state, username) => (state.username = username),
    setEmail: (state, email) => (state.email = email), // Mutazione per l'email
    setUser: (state, user) => (state.user = user),
};

const actions = {
    userInfo: (ctx) => {
        axios.get('/users/me')
            .then((res) => {
                ctx.commit('setLevel', res.data.role);
                ctx.commit('setUsername', res.data.username);
                ctx.commit('setEmail', res.data.email); // Imposta l'email
                ctx.commit('setUser', res.data);
            })
            .catch((error) => {
                console.error("Errore nel recupero dei dati utente:", error);
            });
    },
    checkAuth(ctx) {
        axios.get('/auth/check')
            .then(() => {
                ctx.commit('setAuth', true);
            })
            .catch(() => {
                ctx.commit('setAuth', false);
                router.push('/logout');
            });
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
};
