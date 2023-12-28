<template>
    <v-container fluid class="down-top-padding">
        <v-row justify="center">
            <v-col cols="12" lg="9">
                <v-card>
                    <v-card-title>
                        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line
                            hide-details></v-text-field>
                    </v-card-title>
                    <v-data-table :headers="headers" :items="remediations" :search="search">
                        <template v-slot:item.actions="{ item }">
                            <v-icon small @click="deleteItem(item)">
                                mdi-delete
                            </v-icon>
                        </template>
                    </v-data-table>
                </v-card>
            </v-col>
        </v-row>
        <v-dialog v-model="dialogDelete" max-width="600px">
          <v-card>
            <v-card-title class="text-h5">{{ testo }}</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-container>
</template>
<script>
import axios from 'axios';
import { mapActions } from 'vuex';
export default {
    data() {
        return {
            search: '',
            headers: [
                { text: 'Nome', align: 'start', value: 'nome' },
                { text: 'Codice Elettra', align: 'start', value: 'codice_elettra' },
                { text: 'Azienda', value: 'cliente'},
                { text: 'Tipologia', value: 'type' },
                { text: 'Anno', value: 'anno' },
                { text: 'Actions', value: 'actions', sortable: false },
            ],
            remediations:[],
            dialogDelete: false,
            testo: '',
            docDaEliminare: {}
        }
    },
    methods: {
        getListaRemediation(){
            axios.get("/remediadions/list").then(res => {
                
                this.remediations = res.data
            })
        },
        ...mapActions(
             ['checkAuth']
        ),
        deleteItem(item){
            this.dialogDelete = true;
            this.testo = 'Eliminare: ' + item.nome + '?';
            this.docDaEliminare = item
        },
        closeDelete(){
            this.dialogDelete = false
        },
        deleteItemConfirm(){
            let url = '/items/' + this.docDaEliminare.id;
            axios.delete(url).then(res => {
                this.removeItem(this.docDaEliminare)
                this.dialogDelete = false
            })
        },
        removeItem(item) {
        // Trova l'indice dell'oggetto nell'array items.
        // Il metodo indexOf restituisce -1 se l'oggetto non è presente nell'array.
        let index = this.remediations.indexOf(item);
        
        // Controlla se l'oggetto esiste nell'array verificando che l'indice sia maggiore di -1.
        if (index > -1) {
            // Se l'oggetto esiste nell'array, rimuovilo utilizzando il metodo splice.
            // Splice rimuove 1 elemento a partire dall'indice specificato.
            this.remediations.splice(index, 1);
        }
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