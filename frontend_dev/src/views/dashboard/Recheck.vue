<template>
    <v-container fluid class="down-top-padding">
        <v-row>
            <v-col cols="12">
                <v-card :elevation="1">
                    <v-card-title class="d-flex justify-space-between align-center">
                        <span>{{ company }} - {{ nameApp }}</span>
                        <v-btn color="primary" @click="printReport">Stampa Report</v-btn>
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
import DonutChartRecheck from './components/recheck/DonutChartRecheck.vue';
import RadarChart from './components/recheck/RadarChartRecheck.vue';
import TreemapChart from './components/recheck/TreemapChart.vue';
import ColumnsRecheck from './components/recheck/ColumnsRecheck.vue';
import CardRecheck from './components/recheck/CardRecheck.vue';
import { mapActions } from 'vuex';
export default {
    components: {
        donutchart: DonutChartRecheck,
        radarchart: RadarChart,
        treemapchart: TreemapChart,
        columnsrecheck: ColumnsRecheck,
        cardrecheck: CardRecheck
    },
    data: () => ({
        dataRemediation: { recheck: {}, vapt: {} },
        recheckData: [],
        auditFiltered: {
            "company": "",
            "name":"",
        },
    }),
    props: ['nameApp', 'company'],
    methods: {
        ...mapActions(
            ['checkAuth']
        ),
        getData() { //metodo per recuperare dati per il documento tramite App ed Ente
            // Passaggio di `nomeApp` e `cliente` al componente
            const payload = { name: this.$route.params.nameApp, company: this.$route.params.company };
            const urlBackend = process.env.VUE_APP_RECHECK_DASHBOARD;
            axios.post(urlBackend, payload)
                .then(res => {
                    this.dataRemediation = res.data;
                    this.recheckData = res.data.recheck.findings
                    // Aggiungi i dati ricevuti come necessario
                })
                .catch(error => {
                    console.error("Errore nel caricamento dei dati aggiuntivi:", error);
                });
        },
        printReport(){
            const urlBackend = process.env.VUE_APP_VAPT_PRINT_DASHBOARD_RECHECK;
            this.auditFiltered.name = this.$route.params.nameApp;
            this.auditFiltered.company = this.$route.params.company;

            axios.post(urlBackend, this.auditFiltered, { responseType: 'blob' })
                .then((response) => {
                    // Crea un URL temporaneo per il blob
                    const url = window.URL.createObjectURL(new Blob([response.data]));

                    // Crea un elemento <a> per scaricare il file
                    const link = document.createElement('a');
                    link.href = url;

                    // Costruisci il nome del file dinamicamente
                    const dateStr = new Date().toISOString().split('T')[0];
                    const filename = `Rechek-${this.auditFiltered.company}-${this.auditFiltered.name}-${dateStr}.pdf`;

                    // Imposta il nome del file per il download
                    link.setAttribute('download', filename);

                    // Aggiungi l'elemento <a> al DOM e attiva il click
                    document.body.appendChild(link);
                    link.click();

                    // Rimuovi l'elemento <a> e libera l'URL temporaneo
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(url);
                })
                .catch((error) => {
                    console.error("Errore nel download del report:", error);
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
        this.checkAuth();
        this.getData();
    }
}
</script>