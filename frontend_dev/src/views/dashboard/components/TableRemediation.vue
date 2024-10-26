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
                //{ text: 'Codice Elettra', value: 'codice_elettra', align:'center' },
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
                item.findings.forEach(entry => {
                    let remediation = {
                        nome: item.name,  // Cambiato da 'nome' a 'name'
                        type: item.auditType,  // Cambiato da 'type' a 'auditType'
                        codice_elettra: "-",  // Codice elettra non esiste in new_data, puoi mantenerlo se necessario
                        vulnerabilita: entry.title,  // Cambiato da 'vulnerabilità' a 'title'
                        anno: new Date(item.date).getFullYear(),  // Estrai l'anno dalla data
                        mese: new Date(item.date).toLocaleString('it-IT', { month: 'long' }),  // Estrai il mese dalla data
                        descrizione: entry.vulnType,  // Non c'è 'descrizione' diretta, uso 'vulnType'
                        owner: item.company,  // 'owner' è il cliente, quindi usa 'company'
                        gravita: entry.severity,  // Cambiato da 'gravità' a 'severity'
                        cliente: item.company  // 'cliente' è 'company'
                    };
                    remediationsData.push(remediation);
                });
            });

            this.remediations = remediationsData;
        },
        colorChips(gravita) {
            gravita = gravita.toLowerCase();  // Trasforma 'gravita' in minuscolo

            if (gravita === 'critical') {
                return '#8B0000';  // Rosso scuro per 'critica'
            } 
            else if (gravita === 'high') {
                return '#FF0000';  // Rosso per 'alta'
            } 
            else if (gravita === 'medium') {
                return '#ff7f0e';  // Arancione per 'media'
            } 
            else {
                return '#2ca02c';  // Verde per altre gravità (presumibilmente 'bassa')
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