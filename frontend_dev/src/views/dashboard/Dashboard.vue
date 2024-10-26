<template>
    <v-container fluid class="down-top-padding">
        <v-row>
            <v-col cols="12">
                <v-card>
                    <v-card-title>
                        {{ nomeAppFiltrata }}
                    
                    <!--filtro ricerca-->
                    <filtri :dataRemediation="dataRemediation" @updateDataRemediation="handleUpdateDataRemediation"
                        @clearFiltered="getDataRemediation">
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
        nomeAppFiltrata: ''
    }),
    methods: {
        ...mapActions(
            ['checkAuth']
        ),
        handleUpdateDataRemediation(newData) {
            this.dataRemediation = newData
            let nomeApp = newData[0].nome
            let typeApp = newData[0].type.toUpperCase()
            this.nomeAppFiltrata = nomeApp + ' - ' + typeApp
        },
        getDataRemediation() {
            const urlBackend = process.env.VUE_APP_VAPT_DATA_DASHBOARD;
            axios.get(urlBackend).then(res => {
                this.dataRemediation = res.data
            })
        }
    },
    beforeMount() {
        this.checkAuth();
        this.getDataRemediation();
    }
}
</script>