<template>
    <v-container fluid class="down-top-padding">
        <v-row>
            <TableRemediation :dataRemediation="dataRemediation"></TableRemediation>
        </v-row>
    </v-container>
</template>
<script>
import TableRemediation from '../dashboard/components/TableRemediation';
import axios from 'axios';
import { mapActions } from 'vuex';
import NProgress from 'nprogress';

export default {
    components: {
        TableRemediation
    },
    data: () => ({
        dataRemediation: [],
    }),
    methods: {
        getDataRemediation() {
            NProgress.start(); // Avvia la barra di caricamento

            const urlBackend = process.env.VUE_APP_VAPT_DATA_DASHBOARD;

            axios
                .get(urlBackend)
                .then((res) => {
                this.dataRemediation = res.data; // Imposta i dati ricevuti
                })
                .catch((error) => {
                    this.$toast.error('Errore caricamento dati', { duration: 3000, theme: "bubble" });
                })
                .finally(() => {
                NProgress.done(); // Termina la barra di caricamento
                });
            },
        ...mapActions(
            ['checkAuth']
        )
    },
    beforeMount() {
        this.checkAuth();
        this.getDataRemediation();
    }
}

</script>