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
    async login(ctx, credentials) {
        const urlBackend = process.env.VUE_APP_AUTH_TOKEN;
        try {
            // Effettua il login e ottieni il token
            const response = await axios.post(urlBackend, credentials);
            const token = response.data.access_token;

            // Salva il token nel localStorage e aggiorna lo stato auth
            localStorage.setItem('token', token);
            ctx.commit('setAuth', true);

            // Recupera le informazioni dell'utente
            const userResponse = await axios.get('/users/me');
            ctx.commit('setLevel', userResponse.data.role);
            ctx.commit('setUsername', userResponse.data.username);
            ctx.commit('setEmail', userResponse.data.email);
            ctx.commit('setUser', userResponse.data);

            // Effettua il redirect alla dashboard
            router.push('/dashboard/dashboard');
        } catch (error) {
            console.error("Errore durante il login:", error);
            throw error; // Rilancia l'errore per permettere al componente di gestirlo
        }
    },
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
