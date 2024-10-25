<template>
  <v-data-table :headers="headers" :items="users" item-key="email" class="elevation-1">
    <!-- Azioni: Bottone per eliminare l'utente -->
    <template v-slot:item.actions="{ item }">
      <v-btn @click="$emit('delete-user', item.email)" color="red">
        <v-icon color="white">mdi-delete</v-icon>
      </v-btn>
    </template>

    <!-- Mostra la lista degli enti in una tendina a comparsa -->
    <template v-slot:item.companies="{ item }">
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <!-- Icona o pulsante per aprire la tendina -->
          <v-btn v-bind="attrs" v-on="on" icon>
            <v-icon>mdi-menu-down</v-icon>
          </v-btn>
        </template>

        <!-- Contenuto della tendina: elenco degli enti dell'utente -->
        <v-list>
          <v-list-item
            v-for="(company, index) in item.companies"
            :key="index"
          >
            <v-list-item-content>
              <v-list-item-title>{{ company }}</v-list-item-title> <!-- Mostra il nome dell'ente -->
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: {
    users: {
      type: Array,
      required: true // Validazione per la prop users
    },
  },
  data() {
    return {
      // Definizione delle intestazioni della tabella
      headers: [
        { text: 'Email', value: 'email', align: 'center' },
        { text: 'Username', value: 'username', align: 'center' },
        { text: 'Ruolo', value: 'role', align: 'center' },
        { text: 'Enti', value: 'companies', align: 'center' },
        { text: 'Azioni', value: 'actions', align: 'center', sortable: false },
      ],
    };
  },
};
</script>

<style scoped>
/* Aggiungi eventuali stili personalizzati qui */
</style>
