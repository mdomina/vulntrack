<template>
    <v-dialog v-model="dialog" persistent max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Conferma eliminazione</v-card-title>
        <v-card-text>Sei sicuro di voler eliminare questo utente?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="$emit('update:dialog', false)">Annulla</v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">Elimina</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  export default {
    props: {
      dialog: Boolean,
      userToDelete: String,
    },
    methods: {
      confirmDelete() {
        this.$emit('confirm-delete', this.userToDelete);
        this.$emit('update:dialog', false);
      }
    }
  };
  </script>
  