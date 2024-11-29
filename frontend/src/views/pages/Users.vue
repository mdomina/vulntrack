<template>
  <v-container fluid class="down-top-padding">
    <v-row>
      <v-col cols="12" sm="12">
        <v-card>
          <v-card-title>
            <h2>Users</h2>
            <v-spacer></v-spacer>
            <v-btn @click="showDialog = true">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card-title>
          <user-table :users="users" @delete-user="openDeleteDialog" />
        </v-card>
      </v-col>
    </v-row>
    <add-user-dialog :dialog.sync="showDialog" @add-user="addUser" />
    <delete-confirmation-dialog
      :dialog.sync="dialogDelete"
      :user-to-delete="currentUserToDelete"
      @confirm-delete="deleteUser"
    />
  </v-container>
</template>

<script>
import axios from 'axios';
import AddUserDialog from '@/components/AddUserDialog.vue';
import UserTable from '@/components/UserTable.vue';
import DeleteConfirmationDialog from '@/components/DeleteConfirmationDialog.vue';
import NProgress from 'nprogress';

export default {
  components: {
    AddUserDialog,
    UserTable,
    DeleteConfirmationDialog,
  },
  data() {
    return {
      users: [],
      showDialog: false,
      dialogDelete: false,
      currentUserToDelete: null,
    };
  },
  methods: {
    getUsersList() {
      NProgress.start(); // Avvia la barra di caricamento

      const urlApiUserList = process.env.VUE_APP_ADMIN_USERS_LIST;
      axios.get(urlApiUserList)
        .then((response) => {
          this.users = response.data || [];
        })
        .catch(() => {
          this.$toast.error('Errore nel recupero degli utenti', { duration: 3000, theme: "bubble" });
        })
        .finally(() => {
          NProgress.done(); // Termina la barra di caricamento
        });
    },

    deleteUser(userEmail) {
      NProgress.start(); // Avvia la barra di caricamento

      const urlApiUserDelete = process.env.VUE_APP_ADMIN_USERS_DELETE;
      axios.delete(urlApiUserDelete, {
        data: { email: userEmail }
      })
        .then(() => {
          this.$toast.success("Utente eliminato con successo", { duration: 3000, theme: "bubble" });
          this.users = this.users.filter(user => user.email !== userEmail);
        })
        .catch(() => {
          this.$toast.error("Errore durante l'eliminazione dell'utente", { duration: 3000, theme: "bubble" });
        })
        .finally(() => {
          NProgress.done(); // Termina la barra di caricamento
        });
    },

    openDeleteDialog(userEmail) {
      this.currentUserToDelete = userEmail;
      this.dialogDelete = true;
    },
    addUser() {
      this.getUsersList(); // Aggiorna la lista degli utenti
    }

  },
  mounted() {
    this.getUsersList();
  },
};
</script>
