<template>
    <v-container fluid class="down-top-padding">
        <v-row>
            <v-col cols="12">
                <v-btn color="primary" dark @click="stampaReport">
                    Stampa Report
                </v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card>
                    <v-card-title>
                        <template  v-if="auditFiltered.company != ''">
                            {{ auditFiltered.company }} - {{  auditFiltered.name }} -  {{ auditFiltered.type }}
                        </template>
                    <!--filtro ricerca-->
                    <filtri :dataRemediation="dataRemediation" @updateDataRemediation="handleUpdateDataRemediation"
                        @clearFiltered="clearFilter">
                    </filtri>
                </v-card-title>
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
                            <v-col cols="3">
                                <critiche :dataRemediation="dataRemediation"></critiche>
                            </v-col>
                            <v-col cols="3">
                                <alte :dataRemediation="dataRemediation"></alte>
                            </v-col>

                            <v-col cols="3">
                                <medie :dataRemediation="dataRemediation"></medie>
                            </v-col>
                            <v-col cols="3">
                                <basse :dataRemediation="dataRemediation"></basse>
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
                        Timeline Vulnerabilità
                    </v-card-title>
                    <v-card-text>
                        <timeline :data="dataRemediation"></timeline>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="6">
                <v-card :elevation="1">
                    <v-card-title>
                        Percentuale Vulnerabilità Complessive
                    </v-card-title>
                    <v-card-text>
                        <piechart :dataRemediation="dataRemediation"></piechart>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="6">
                <v-card :elevation="1">
                    <v-card-title>
                        Vulnerabilità Complessive Mensili
                    </v-card-title>
                    <v-card-text>
                        <mesi :dataRemediation="dataRemediation"></mesi>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="6">
                <v-card :elevation="1">
                    <v-card-title>
                        Vulnerabilità per Categoria
                    </v-card-title>
                    <v-card-text>
                        <radarchart :dataRemediation="dataRemediation"></radarchart>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="6">
                <v-card :elevation="1">
                    <v-card-title>
                        Vulnerabilità per Nome
                    </v-card-title>
                    <v-card-text>
                        <nomiVulnerabilita :dataRemediation="dataRemediation"></nomiVulnerabilita>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <!-- <v-row>
            <tableRem :dataRemediation="dataRemediation"></tableRem>
        </v-row> -->
    </v-container>
</template>
<script>
import ColumsChart from './components/ColumnsChart.vue'
import Filtri from './components/Filtri.vue'
import PieChart from './components/PieChart.vue'
import RadarChart from './components/RadarChart.vue'
import Basse from './components/Basse.vue'
import Medie from './components/Medie.vue'
import Alte from './components/Alte.vue'
import Critiche from './components/Critiche.vue'
import TableRemediation from './components/TableRemediation.vue'
import BarChart from './components/BarChart.vue'
import TreemapChart from './components/TreemapChart.vue'
import { mapActions } from 'vuex';
import axios from 'axios';

export default {
    name: "Dashboard",
    components: {
        timeline: ColumsChart,
        filtri: Filtri,
        piechart: PieChart,
        radarchart: RadarChart,
        basse: Basse,
        medie: Medie,
        alte: Alte,
        critiche: Critiche,
        //tableRem: TableRemediation,
        mesi: BarChart,
        nomiVulnerabilita: TreemapChart
    },
    data: () => ({
        dataRemediation: [],
        auditFiltered: {
            "company": "",
            "name":"",
            "type":""
        }
    }),
    methods: {
        ...mapActions(
            ['checkAuth']
        ),
        handleUpdateDataRemediation(newData) {
            this.dataRemediation = newData
            this.auditFiltered.name = newData[0].name
            this.auditFiltered.company = newData[0].company
            this.auditFiltered.type = newData[0].auditType
            
        },
        getDataRemediation() {
            const urlBackend = process.env.VUE_APP_VAPT_DATA_DASHBOARD;
            axios.get(urlBackend).then(res => {
                this.dataRemediation = res.data
            })
        },
        clearFilter(){
            this.auditFiltered.name = "";
            this.auditFiltered.company = "";
            this.auditFiltered.type = "";
            this.getDataRemediation();
        },
        stampaReport() {
            const urlBackend = process.env.VUE_APP_VAPT_PRINT_DASHBOARD;

            axios.post(urlBackend, this.auditFiltered, { responseType: 'blob' })
                .then((response) => {
                    // Crea un URL temporaneo per il blob
                    const url = window.URL.createObjectURL(new Blob([response.data]));

                    // Crea un elemento <a> per scaricare il file
                    const link = document.createElement('a');
                    link.href = url;

                    // Costruisci il nome del file dinamicamente
                    const dateStr = new Date().toISOString().split('T')[0];
                    const filename = `Report-${this.auditFiltered.type}-${this.auditFiltered.company}-${this.auditFiltered.name}-${dateStr}.docx`;

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


},
    beforeMount() {
        this.checkAuth();
        this.getDataRemediation();
    }
}
</script>