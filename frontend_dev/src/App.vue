<template>
  <v-app id="materialpro" :class="`${!$vuetify.breakpoint.smAndDown ? 'full-sidebar' : 'mini-sidebar'}`">
      <router-view />
  </v-app>

</template>

<script>
// Importa le variabili di configurazione
import { API_URL, IMAGES_PATH } from './vue_config';

export default {
  name: 'App',

  data() {
    return {
      apiUrl: API_URL,
      };
    },

  components: {
    
  },

  created(){
    this.$store.dispatch('userInfo');
  }

};
</script>
