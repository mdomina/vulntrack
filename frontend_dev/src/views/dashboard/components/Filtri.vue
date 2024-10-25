<template>
  <v-row justify="end">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">
          Filtri
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Filtri Ricerca</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <!-- Selettore per Enti -->
                <v-select :items="companies" label="Enti" v-model="selectedCompany" item-text="name" item-value="id" :required="false"></v-select>
              </v-col>
              <v-col cols="12">
                <!-- Selettore per Nome App -->
                <v-select :items="appNames" label="Nome App" v-model="nomeApp" :required="false"></v-select>
              </v-col>
              <v-col cols="12">
                <!-- Radio per tipo app -->
                <v-radio-group v-model="typeApp" required row>
                  <v-radio label="Vapt" value="vapt"></v-radio>
                  <v-radio label="Recheck" value="recheck"></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" text @click="filteredData()">Save</v-btn>
          <v-btn color="blue darken-1" text @click="clearFilter()">Clear</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import axios from 'axios';

export default {
  name: "Filtri",
  data: () => ({
    dialog: false,
    companies: [],       // Lista per gli enti
    appNames: [],        // Lista per i nomi app
    selectedCompany: '', // Entità selezionata
    nomeApp: '',         // Nome app selezionato
    typeApp: ''          // Tipo app selezionato
  }),
  methods: {
    getCompaniesByUser() {
      const urlBackendCompanies = process.env.VUE_APP_VAPT_COMPANIES_BY_USER;
      axios.get(urlBackendCompanies)
      .then(res => {
        this.companies = res.data;
      })
      .catch(err => console.error('Errore nel recupero delle companies:', err));
    },
    getNameApps(selectedCompany) {
      if (!selectedCompany) return;  // Verifica che sia selezionato un ente /names/appbyComany
      const urlBackend = `${process.env.VUE_APP_VAPT_NAMES_APP_BY_COMP}/${selectedCompany}`; //<--- MODIFICARE CON LA NUOVA API!!!
      axios.get(urlBackend)
      .then(res => {
        this.appNames = res.data;
      })
      .catch(err => console.error('Errore nel recupero delle app:', err));
    },
    filteredData() {
      const data = { nome: this.nomeApp, type: this.typeApp, company: this.selectedCompany };
      const urlBackend = process.env.VUE_APP_VAPT_LIST_FILTERED;
      axios.post(urlBackend, data)
      .then(res => {
        if (res.data.length > 0) {
          this.dialog = false;
          this.$emit('updateDataRemediation', res.data); // Invia i dati filtrati alla dashboard
        } else {
          this.$toasted.show('Documento Non Trovato!', {
            duration: 3000,
            theme: "bubble",
            fullWidth: false,
            position: "top-center"
          });
        }
      })
      .catch(err => console.error('Errore durante il filtraggio:', err));
    },
    clearFilter() {
      this.selectedCompany = '';
      this.nomeApp = '';
      this.typeApp = '';
      this.appNames = [];  // Ripristina anche i nomi app
      this.$emit('clearFiltered'); // Notifica alla dashboard che i filtri sono stati cancellati
      this.dialog = false;
    }
  },
  watch: {
    // Watcher per eseguire getNameApps quando selectedCompany cambia
    selectedCompany(newVal) {
      this.getNameApps(newVal);
    }
  },
  mounted() {
    this.getCompaniesByUser();
  }
};
</script>

<style scoped>
/* Aggiungi eventuali stili personalizzati qui */
</style>
