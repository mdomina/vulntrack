<template>
  <v-container fluid class="down-top-padding">
    <v-row>
      <v-col cols="12" sm="12">
        <v-card>
          <v-card-title>
            <h2>Dati Utente</h2>
            <v-spacer></v-spacer>
            <v-btn @click="showDialog = true">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card-title>
          <v-data-table :headers="headers" :items="users" item-key="id" class="elevation-1" :loading="loading">
            <template v-slot:item.actions="{ item }">
              <v-btn @click="openDeleteDialog(item.id)" color="red">
                <v-icon color="white">mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    <add-user-dialog :dialog.sync="showDialog" @add-user="addUser" />
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
import axios from 'axios';
import AddUserDialog from '@/components/AddUserDialog.vue'; 

export default {
  components: {
    AddUserDialog
  },
  data() {
    return {
      headers: [
        { text: 'Email', value: 'email', align: 'center' },
        { text: 'Name', value: 'name', align: 'center' },
        { text: 'Username', value: 'username', align: 'center' },
        { text: 'Role', value: 'role', align: 'center' },
        { text: 'Actions', value: 'actions', align: 'center', sortable: false }
      ],
      users: [],
      showDialog: false,
      loading: true,
      dialogDelete: false,
      currentUserToDelete: null,
    };
  },
  methods: {
    async getUsersList() {
      this.loading = true;
      try {
        const response = await axios.get('/admin/user/list');
        this.users = response.data.users || [];
      } catch (error) {
        // Sostituzione console.log con toast per l'errore di caricamento
        this.$toast.error('Errore nel caricamento degli utenti. Riprova più tardi.'); 
      } finally {
        this.loading = false;
      }
    },
    async deleteUser(userId) {
      this.dialogDelete = false; // Chiudi il dialogo
      try {
        const response = await axios.delete(`/gui/user/delete/${userId}`);
        if (response.status === 200) {
          this.$toast.success("Utente eliminato"); // Notifica di successo
          this.users = this.users.filter(user => user.id !== userId);
        }
      } catch (error) {
        // Sostituzione console.log con toast per l'errore di eliminazione
        if (error.response) {
          switch (error.response.status) {
            case 403:
              this.$toast.error('Non hai i permessi necessari per eliminare questo utente.');
              break;
            case 404:
              this.$toast.error('Utente non trovato.');
              break;
            case 500:
              this.$toast.error('Si è verificato un errore interno del server. Riprova più tardi.');
              break;
            default:
              this.$toast.error('Si è verificato un errore durante l\'eliminazione dell\'utente.');
              break;
          }
        } else {
          this.$toast.error('Errore di rete. Si prega di riprovare più tardi.'); // Gestisci errore di rete
        }
      }
    },
    openDeleteDialog(userId) {
      this.currentUserToDelete = userId;
      this.dialogDelete = true;
    },
    async addUser(user) {
      this.$toast.success("Utente aggiunto");
      this.users.push(user); 
      setTimeout(() => {
        this.getUsersList(); // Ricarica utenti
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
