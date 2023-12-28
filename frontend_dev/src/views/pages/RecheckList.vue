<template>
    <v-container fluid class="down-top-padding">
        <v-row justify="center">
            <v-col cols="12">
                <v-card>
                    <v-card-title>
                        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line
                            hide-details></v-text-field>
                    </v-card-title>
                    <v-data-table :headers="headers" :items="remediations" :search="search">
                        <template v-slot:item.vapt="{ item }">
                            <v-icon color="success" small v-if="item.vapt">
                                mdi-checkbox-marked-circle-outline
                            </v-icon>
                            <v-icon color="error" small v-else>
                                mdi-close-circle-outline
                            </v-icon>
                        </template>
                        <template v-slot:item.recheck="{ item }">
                            <v-icon color="success" small v-if="item.recheck">
                                mdi-checkbox-marked-circle-outline
                            </v-icon>
                            <v-icon color="error" small v-else>
                                mdi-close-circle-outline
                            </v-icon>
                        </template>
                        <template v-slot:item.actions="{ item }">
                            <v-icon color="success" small @click="showDoc(item)" v-if="item.recheck && item.vapt">
                                mdi-file-find
                            </v-icon>
                        </template>
                    </v-data-table>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import axios from 'axios';
import { mapActions } from 'vuex';
import router from '../../router';
export default {
    data() {
        return {
            search: '',
            headers: [
                { text: 'Nome', align: 'start', value: 'nome' },
                { text: 'Codice Elettra', align: 'start', value: 'codice_elettra' },
                { text: 'Azienda', value: 'cliente'},
                { text: 'Anno', value: 'anno' },
                { text: 'VAPT', value: 'vapt', align: 'center' },
                { text: 'Recheck', value: 'recheck', align: 'center' },
                { text: 'Actions', value: 'actions', align: 'center', sortable: false },
            ],
            remediations:[],
        }
    },
    methods: {
        getListaRemediation(){
            axios.get("/recheck/list").then(res => {
                
                this.remediations = res.data
            })
        },
        ...mapActions(
             ['checkAuth']
        ),
        showDoc(item){
            let url = '/dashboard/recheck/' + item.nome
            this.$router.push(url)
        }
    },
    beforMount(){
        this.checkAuth();
    },
    mounted(){
        this.getListaRemediation();
    }
}
</script>