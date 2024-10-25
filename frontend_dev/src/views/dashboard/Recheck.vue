<template>
    <v-container fluid class="down-top-padding">
        <v-row>
            <v-col cols="12">
                <v-card :elevation="1">
                    <v-card-title class="d-flex justify-space-between align-center">
                        <span>App:{{ nomeApp }} | Ente:{{ cliente }}</span>
                        <v-btn color="primary" @click="fetchAdditionalData">Scarica Documento</v-btn>
                    </v-card-title>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card :elevation="1">
                    <v-card-title>
                        Recheck Summary
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>
                                        VAPT
                                    </v-card-title>
                                    <v-card-text>
                                        <cardrecheck :data="dataRemediation.vapt"></cardrecheck>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>
                                        Recheck
                                    </v-card-title>
                                    <v-card-text>
                                        <cardrecheck :data="dataRemediation.recheck"></cardrecheck>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card :elevation="1">
                    <v-card-title>
                        Vulnerabilità Totali
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>VAPT</v-card-title>
                                    <v-card-text>
                                        <columnsrecheck :data="dataRemediation.vapt"></columnsrecheck>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>Recheck</v-card-title>
                                    <v-card-text v-show="recheckData.length > 0">
                                        <columnsrecheck :data="dataRemediation.recheck"></columnsrecheck>
                                    </v-card-text>
                                    <v-card-text v-show="recheckData.length == 0">
                                        <p class="text-center">
                                            <v-icon x-large color="green darken-2">
                                                mdi-check-all
                                            </v-icon>
                                            <br>
                                            Nessuna Vulnerabilità
                                        </p>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card :elevation="1">
                    <v-card-title>
                        Percentuale Vulnerabilità Complessive
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>VAPT</v-card-title>
                                    <v-card-text>
                                        <donutchart :dataRemediation="dataRemediation.vapt"></donutchart>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>
                                        Recheck
                                    </v-card-title>
                                    <v-card-text v-show="recheckData.length > 0">
                                        <donutchart :dataRemediation="dataRemediation.recheck"></donutchart>
                                    </v-card-text>
                                    <v-card-text v-show="recheckData.length == 0">
                                        <p class="text-center">
                                            <v-icon x-large color="green darken-2">
                                                mdi-check-all
                                            </v-icon>
                                            <br>
                                            Nessuna Vulnerabilità
                                        </p>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card :elevation="1">
                    <v-card-title>
                        Vulnerabilità per Tipologia
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>VAPT</v-card-title>
                                    <v-card-text>
                                        <radarchart :dataRemediation="dataRemediation.vapt"></radarchart>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>
                                        Recheck
                                    </v-card-title>
                                    <v-card-text v-show="recheckData.length > 0">
                                        <radarchart :dataRemediation="dataRemediation.recheck"></radarchart>
                                    </v-card-text>
                                    <v-card-text v-show="recheckData.length == 0">
                                        <p class="text-center">
                                            <v-icon x-large color="green darken-2">
                                                mdi-check-all
                                            </v-icon>
                                            <br>
                                            Nessuna Vulnerabilità
                                        </p>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card :elevation="1">
                    <v-card-title>
                        Vulnerabilità per Nome
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>VAPT</v-card-title>
                                    <v-card-text>
                                        <treemapchart :dataRemediation="dataRemediation.vapt"></treemapchart>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="6">
                                <v-card :elevation="0">
                                    <v-card-title>
                                        Recheck
                                    </v-card-title>
                                    <v-card-text v-show="recheckData.length > 0">
                                        <treemapchart :dataRemediation="dataRemediation.recheck"></treemapchart>
                                    </v-card-text>
                                    <v-card-text v-show="recheckData.length == 0">
                                        <p class="text-center">
                                            <v-icon x-large color="green darken-2">
                                                mdi-check-all
                                            </v-icon>
                                            <br>
                                            Nessuna Vulnerabilità
                                        </p>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import axios from 'axios';
import DonutChart from './components/DonutChart.vue';
import RadarChart from './components/RadarChart.vue';
import TreemapChart from './components/TreemapChart.vue';
import ColumnsRecheck from './components/ColumnsRecheck.vue';
import CardRecheck from './components/CardRecheck.vue';

export default {
    components: {
        donutchart: DonutChart,
        radarchart: RadarChart,
        treemapchart: TreemapChart,
        columnsrecheck: ColumnsRecheck,
        cardrecheck: CardRecheck
    },
    data: () => ({
        dataRemediation: { recheck: {}, vapt: {} },
        recheckData: []
    }),
    props: ['nomeApp', 'cliente'],
    methods: {
        getData() {
            let data = { nome: this.nomeApp, type: '' };
            axios.post("/recheck/data", data).then(res => {
                this.dataRemediation = res.data;
                this.recheckData = res.data.recheck[0]?.data || [];
            });
        },
        fetchAdditionalData() { //metodo per recuperare dati per il documento tramite App ed Ente
            // Passaggio di `nomeApp` e `cliente` al componente
            const payload = { nome: this.nomeApp, cliente: this.$route.params.cliente };

            axios.post("/recheck/additionalData", payload) //<--MODIFICARE API
                .then(res => {
                    console.log("Dati aggiuntivi caricati:", res.data);
                    // Aggiungi i dati ricevuti come necessario
                })
                .catch(error => {
                    console.error("Errore nel caricamento dei dati aggiuntivi:", error);
                });
        }
    }
,
    watch: {
        nomeApp() {
            this.getData();
        }
    },
    mounted() {
        this.getData();
    }
}
</script>