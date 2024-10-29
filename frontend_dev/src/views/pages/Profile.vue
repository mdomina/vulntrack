<template>
  <v-container fluid class="down-top-padding">
      <v-row>
          <v-col cols="12" sm="12">
              <v-card>
                  <v-toolbar flat>
                      <v-toolbar-title>Account</v-toolbar-title>
                      <v-spacer></v-spacer>
                      <v-card-actions>
                          <ChangePassword></ChangePassword>
                      </v-card-actions>
                  </v-toolbar>
                  <v-divider></v-divider>
                  <div>
                      <!-- <v-list-item-subtitle class="text-wrap">
                          You can show a dense version of the table by using the <code>dense</code> prop.
                      </v-list-item-subtitle> -->
                      <div class="mt-4">
                          <v-simple-table>
                              <template v-slot:default>
                                  <tbody>
                                      <tr>
                                          <th>
                                              Name
                                          </th>
                                          <td>
                                              {{ getUser.name }}
                                          </td>
                                      </tr>
                                      <tr>
                                          <th>
                                              Surname
                                          </th>
                                          <td>
                                              {{ getUser.surname }}
                                          </td>
                                      </tr>
                                      <tr>
                                          <th>
                                              Username
                                          </th>
                                          <td>
                                              {{ getUser.username }}
                                          </td>
                                      </tr>
                                      <tr>
                                          <th>
                                              Email
                                          </th>
                                          <td>
                                              {{ getUser.email }}
                                          </td>
                                      </tr>
                                      <tr>
                                          <th>
                                              Api Key
                                          </th>
                                          <td>
                                              {{ getUser.apikey }}
                                          </td>
                                      </tr>
                                      <tr>
                                          <th>
                                              Role
                                          </th>
                                          <td>
                                              {{ getUser.role }}
                                          </td>
                                      </tr>
                                  </tbody>
                              </template>
                          </v-simple-table>
                      </div>
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
  components:{
      ChangePassword
  },
  data(){
      return {
          dialog: false,
      }
  },
  computed: {
      ...mapGetters([
          'getUser'
      ])
  },
  watch: {
     
  },
  mounted() {
  }
}
</script>