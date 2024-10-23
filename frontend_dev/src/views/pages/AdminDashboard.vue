<template>
  <v-container fluid class="down-top-padding">
    <v-row>
      <v-col cols="12" sm="12">
        <v-card>
          <v-card-title>
            <h2>Admin Dashboard</h2>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-btn @click="showDialog = true">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card-title>
          <v-data-table :headers="headers" :items="users" item-key="id" class="elevation-1" :loading="loading">
            <!-- bottone per eliminare l'utente -->
            <template v-slot:item.actions="{ item }">
              <v-btn @click="openDeleteDialog(item.id)" color="red">
                <v-icon color="white">mdi-delete</v-icon>
              </v-btn>
            </template>

          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    <!-- aggiungi utente -->
    <add-user-dialog :dialog.sync="showDialog" @add-user="addUser" />
    <!-- elimina utente dialog -->
    <v-dialog v-model="dialogDelete" persistent max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Conferma eliminazione</v-card-title>
        <v-card-text>Sei sicuro di voler eliminare questo utente?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialogDelete = false">Annulla</v-btn>
          <v-btn color="red darken-1" text @click="deleteUser(currentUserToDelete)">Elimina</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import axios from 'axios'; // Importa Axios
import AddUserDialog from '@/components/AddUserDialog.vue'; // Assicurati che il percorso sia corretto

export default {
  components: {
    AddUserDialog
  },
  data() {
    return {
      headers: [
        { text: 'Email', value: 'email', align: 'center' },
        { text: 'Name', value: 'name', align: 'center' },
        { text: 'Surname', value: 'surname', align: 'center' },
        { text: 'Username', value: 'username', align: 'center' },
        { text: 'Role', value: 'role', align: 'center' },
        { text: 'Actions', value: 'actions', align: 'center', sortable: false } // Aggiungi colonna per le azioni
      ],
      users: [], // Array per memorizzare i dati degli utenti
      showDialog: false, // Stato per mostrare il dialog 
      loading: true, // Stato di caricamento
      dialogDelete: false,
      currentUserToDelete: null,
    };
  },
  methods: {
    getUsersList(userId) {
      this.loading = true;
      axios.get('http://localhost:8000/admin/users/list')
        .then((response) => {
          console.log("Response data:", response.data); // Log the response data
          this.users = response.data.users || []; // Ensure this is correct based on your response
          this.loading = false; // Set loading to false after fetching data
        })
        .catch((error) => {
          console.error("Error fetching users:", error); // Log the error for debugging
          this.$toast.error('Errore:', error);
          this.loading = false; // Ensure loading is false even on error
    });
    },
    deleteUser(userId) {
      this.dialogDelete = false; // Chiudi il dialogo
      try {
        const response = axios.delete(`/gui/user/delete/${userId}`);
        if (response.status === 200) {
          this.$toast.success("Utente eliminato");
          this.users = this.users.filter(user => user.id !== userId);
        }
      } catch (error) {
        this.$toast.error('Errore durante l\'eliminazione dell\'utente');
      }
    },
    openDeleteDialog(userId) {
      this.currentUserToDelete = userId;
      this.dialogDelete = true;
    },

    addUser(user) {
      this.$toast.success("Utente aggiunto");
      this.users.push(user); // Aggiungi il nuovo utente alla lista
      setTimeout(() => {
        // Qui puoi inserire il codice che vuoi eseguire dopo il ritardo
        this.getUsersList(); // ricarica gli utenti
      }, 1500);
      
    }
  },
  mounted() {
    this.getUsersList(); // Carica i dati al momento del montaggio del componente
  }
};
</script>

<style scoped>
/* Aggiungi stili personalizzati se necessario */
</style>