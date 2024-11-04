<template>
  <v-container fluid class="down-top-padding">
    <v-row>
      <v-col cols="12" sm="12">
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title>Account</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-card-actions>
              <ChangePassword />
            </v-card-actions>
          </v-toolbar>
          <v-divider></v-divider>
          <div class="mt-4">
            <v-simple-table>
              <template v-slot:default>
                <tbody>
                  <tr>
                    <th>Username</th>
                    <td>{{ getUser.username || 'Non disponibile' }}</td>
                  </tr>
                  <tr>
                    <th>Email</th>
                    <td>{{ getUser.email || 'Non disponibile' }}</td>
                  </tr>
                  <tr>
                    <th>Name</th>
                    <td>{{ getUser.name || 'Non disponibile' }}</td>
                  </tr>
                  <tr>
                    <th>Surname</th>
                    <td>{{ getUser.surname || 'Non disponibile' }}</td>
                  </tr>
                  <tr>
                    <th>Role</th>
                    <td>{{ getUser.role || 'Non disponibile' }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import ChangePassword from '@/components/ChangePassword';

export default {
  components: {
    ChangePassword,
  },
  computed: {
    ...mapGetters(['getUser']),
  },
  mounted() {
    if (!this.getUser) {
      this.$store.dispatch('userInfo');
    }
  },
};
</script>
