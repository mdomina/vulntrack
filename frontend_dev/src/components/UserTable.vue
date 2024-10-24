<template>
    <v-data-table :headers="headers" :items="users" item-key="email" class="elevation-1">
      <template v-slot:item.actions="{ item }">
        <v-btn @click="$emit('delete-user', item.email)" color="red">
          <v-icon color="white">mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </template>
  
  <script>
  export default {
    props: {
      users: Array,
    },
    data() {
      return {
        headers: [
          { text: 'Email', value: 'email', align: 'center' },
          { text: 'Name', value: 'name', align: 'center' },
          { text: 'Username', value: 'username', align: 'center' },
          { text: 'Role', value: 'role', align: 'center' },
          { text: 'Actions', value: 'actions', align: 'center', sortable: false },
        ],
      };
    },
  };
  </script>
  