<template>
    <v-col cols="12">
        <v-card :elevation="1">
            <v-card-title>
                <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line
                    hide-details></v-text-field>
            </v-card-title>
            <v-data-table :headers="headers" :items="remediations" :search="search">
                <template v-slot:item.gravita="{ item }">
                    <v-chip :color="colorChips(item.gravita)" dark> 
                        {{ item.gravita }}
                    </v-chip>
                </template>
            </v-data-table>
        </v-card>
    </v-col>
</template>
<script>

export default {
    data() {
        return {
            search: '',
            headers: [
                { text: 'Nome', value: 'nome', align:'center' },
                { text: 'Codice Elettra', value: 'codice_elettra', align:'center' },
                { text: 'Tipologia', value: 'type', align:'center' },
                { text: 'Anno', value: 'anno', align:'center' },
                //{ text: 'Mese', value: 'mese', align:'center' },
                { text: 'Azienda', value: 'cliente', align:'center' },
                { text: 'Vulnerabilità', value: 'vulnerabilita', align:'center' },
                { text: 'Gravità', value: 'gravita', align:'center'}
                //{ text: 'Descrizione', value: 'descrizione', sortable: false},
                //{ text: 'Owner', value: 'owner' },
            ],
            remediations: []

        }
    },
    props: ['dataRemediation'],
    methods: {
        formatRemediationData() {
            let remediationsData = [];
            this.dataRemediation.forEach(item => {
                item.data.forEach(entry => {
                    let remediation = {
                        nome: item.nome,
                        type: item.type,
                        codice_elettra: item.codice_elettra,
                        vulnerabilita: entry['vulnerabilità'],
                        anno: item.anno,
                        mese: item.mese,
                        descrizione: entry.descrizione,
                        owner: entry.owner,
                        gravita: entry['gravità'],
                        cliente: item.cliente
                    };
                    remediationsData.push(remediation);
                });
            });
            this.remediations = remediationsData;
        },
        colorChips(gravita){
            if (gravita == 'critica'){
                return '#8B0000'
            }
            else if (gravita == 'alta'){
                return '#FF0000'
            }
            else if (gravita == 'media'){
                return '#ff7f0e'
            }
            else {
                return '#2ca02c'
            }
        }
    },
    watch: {
        dataRemediation: {
            handler() {
                this.formatRemediationData();
            },
            deep: true,
        },
    },
    mounted() {

    }
}
</script>