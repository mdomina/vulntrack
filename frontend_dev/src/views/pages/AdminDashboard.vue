<template>
  <v-container fluid class="down-top-padding">
    <v-row>
      <v-col cols="12" sm="12">
        <v-card>
          <v-card-title>
            <h2>Admin Dashboard</h2>
            <v-spacer></v-spacer>
            <v-btn @click="showDialog = true">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card-title>
          <v-data-table :headers="headers" :items="users" item-key="email" class="elevation-1" :loading="loading">
            <!-- bottone per eliminare l'utente -->
            <template v-slot:item.actions="{ item }">
              <v-btn @click="openDeleteDialog(item.email)" color="red">
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
import AddUserDialog from '@/components/AddUserDialog.vue';

export default {
  components: {
    AddUserDialog,
  },
  data() {
    return {
      headers: [
        { text: 'Email', value: 'email', align: 'center' },
        { text: 'Name', value: 'name', align: 'center' },
        { text: 'Username', value: 'username', align: 'center' },
        { text: 'Role', value: 'role', align: 'center' },
        { text: 'Actions', value: 'actions', align: 'center', sortable: false }, // Aggiungi colonna per le azioni
      ],
      users: [], // Array per memorizzare i dati degli utenti
      showDialog: false, // Stato per mostrare il dialog 
      loading: true, // Stato di caricamento
      dialogDelete: false,
      currentUserToDelete: null,
    };
  },
  methods: {
    getUsersList() {
      this.loading = true;
      axios.get("http://127.0.0.1:8000/admin/users/list")
        .then((response) => {
          console.log("Response data:", response.data); // Log the response data
          this.users = response.data || []; // Assicurati che sia corretto in base alla tua risposta
          this.loading = false; // Imposta loading su false dopo il recupero dei dati
        })
        .catch((error) => {
          console.error("Error fetching users:", error); // Log dell'errore per il debug
          this.$toast.error('Errore:', error);
          this.loading = false; // Assicurati che loading sia false anche in caso di errore
        });
    },
    deleteUser(userEmail) {
      this.dialogDelete = false; // Chiudi il dialogo
      // Esegui la richiesta di eliminazione
      axios.delete('/admin/users/delete', {
        data: { email: userEmail } // Passa l'email nel body della richiesta
      })
        .then((response) => {
          if (response.status === 200) {
            this.$toast.success("Utente eliminato");
            this.users = this.users.filter(user => user.email !== userEmail);
          }
        })
        .catch((error) => {
          this.$toast.error('Errore durante l\'eliminazione dell\'utente');
          console.error("Errore durante l'eliminazione:", error); // Log per il debug
        });
    },
    openDeleteDialog(userEmail) {
      this.currentUserToDelete = userEmail;
      this.dialogDelete = true;
    },
    addUser(user) {
      this.$toast.success("Utente aggiunto");
      this.users.push(user); // Aggiungi il nuovo utente alla lista
      setTimeout(() => {
        this.getUsersList(); // Ricarica gli utenti
      }, 1500);
    },
  },
  mounted() {
    this.getUsersList(); // Carica i dati al momento del montaggio del componente
  },
};
</script>

<style scoped>
/* Aggiungi stili personalizzati se necessario */
</style>
