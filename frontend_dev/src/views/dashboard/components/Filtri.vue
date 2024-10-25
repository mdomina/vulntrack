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
          <span class="text-h5">filtri ricerca</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-select :items="items" label="Nome App" v-model="nomeApp" required></v-select>
              </v-col>
              <v-col cols="12">
                <v-radio-group v-model="typeApp" required row >
                  <v-radio label="Vapt" value="vapt"></v-radio>
                  <v-radio label="Recheck" value="recheck"></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Close
          </v-btn>
          <v-btn color="blue darken-1" text @click="filteredData()">
            Save
          </v-btn>
          <v-btn color="blue darken-1" text @click="clearFilter()">
            Clear
          </v-btn>
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
    items: [],
    nomeApp: '',
    typeApp: ''
  }),
  methods: {
    getNameApps() {
      const urlBackend = process.env.VUE_APP_VAPT_NAMES_APP;
      //urlcomposta = urlBackend+nometente
      axios.get(urlBackend).then(res => {
        this.items = res.data
      })
    },
    filteredData() {
      let data = { nome: this.nomeApp, type: this.typeApp }
      const urlBackend = process.env.VUE_APP_VAPT_LIST_FILTERED;
      axios.post(urlBackend, data).then(res => {
        if (res.data.length > 0 ){
          this.dialog = false;
          this.$emit('updateDataRemediation', res.data); // invio i dati alla pagina dashboard
        }
        else{
          this.$toasted.show('Documento Non Trovato!', { duration: 3000, theme: "bubble", fullWidth: false, position: "top-center" });
        }
      }).catch(err => {
        console.log(err)
      })
    },
    clearFilter() {
      this.dialog = false;
      this.$emit('clearFilterd');
    }
  },
  mounted() {
    this.getNameApps();
  }

}
</script>