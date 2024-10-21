<template>
  <v-app id="materialpro" :class="`${!$vuetify.breakpoint.smAndDown ? 'full-sidebar' : 'mini-sidebar'}`">
      <router-view />
  </v-app>

</template>

<script>

export default {
  name: 'App',

  data() {
    return {
      };
    },

  components: {
    
  },

  created(){
    this.$store.dispatch('userInfo');
  }

};
</script>
