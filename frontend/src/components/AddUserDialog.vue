<template>
  <!-- Dialog per aggiungere un nuovo utente -->
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <!-- Titolo del dialog -->
      <v-card-title>
        <span class="headline">Aggiungi Utente</span>
      </v-card-title>
      
      <!-- Sottotitolo con il form -->
      <v-card-subtitle>
        <v-form ref="form" v-model="valid">
          <!-- Campo per l'email dell'utente -->
          <v-text-field v-model="user.email" label="Email" required :rules="emailRules" />
          
          <!-- Campo per il nome dell'utente -->
          <v-text-field v-model="user.name" label="Nome" required :rules="[v => !!v || 'Nome è richiesto']" />
          
          <!-- Campo per il cognome dell'utente -->
          <v-text-field v-model="user.surname" label="Cognome" required :rules="[v => !!v || 'Cognome è richiesto']" />
          
          <!-- Campo per la password dell'utente -->
          <v-text-field v-model="user.password" label="Password" required :rules="passwordRules"
            append-icon="mdi-eye-off" @click:append="toggleShowPassword" :type="showPassword ? 'text' : 'password'" />
          
          <!-- Selettore per il ruolo dell'utente -->
          <v-select v-model="user.role" :items="roles" label="Ruolo" required :rules="[roleRule]" item-text="name"
            item-value="value" />
          
          <!-- Selettore per l'ente dell'utente (con supporto per selezione multipla) -->
          <v-select v-model="user.ente" :items="enti" label="Ente" required
            :rules="[v => !!v || 'Seleziona almeno un ente']" item-text="name" item-value="id" multiple />
          <!-- `multiple` permette all'utente di selezionare più enti -->
        </v-form>
      </v-card-subtitle>

      <!-- Azioni del dialog -->
      <v-card-actions>
        <v-spacer></v-spacer>
        <!-- Pulsante per annullare l'operazione -->
        <v-btn text @click="close">Annulla</v-btn>
        <!-- Pulsante per inviare i dati -->
        <v-btn color="primary" @click="submit">Aggiungi</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios'; // Importa Axios per effettuare chiamate API

export default {
  props: {
    dialog: { // Proprietà per controllare la visibilità del dialog
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      valid: false, // Stato di validazione del modulo
      showPassword: false, // Stato per mostrare/nascondere la password
      user: {
        email: '',   // Email dell'utente
        name: '',    // Nome dell'utente
        surname: '', // Cognome dell'utente
        password: '',// Password dell'utente
        role: '',    // Ruolo dell'utente (admin/user)
        ente: []     // Lista di enti selezionati dall'utente (inizialmente vuota)
      },
      roles: [ // Opzioni per il selettore dei ruoli
        { value: 'admin', name: 'Admin' },
        { value: 'user', name: 'User' }
      ],
      enti: [], // Elenco degli enti ottenuti dall'API
      // Regole per la validazione dei campi
      emailRules: [
        v => !!v || 'Email è richiesta',
        v => /.+@.+\..+/.test(v) || 'Email deve essere valida'
      ],
      roleRule: [
        v => !!v || 'Ruolo è richiesto',
        v => ['admin', 'user'].includes(v) || 'Ruolo deve essere "Admin" o "User"'
      ],
      passwordRules: [
        v => !!v || 'Campo obbligatorio',
        v => v.length >= 12 || 'Minimo 12 caratteri',
        v => /\d/.test(v) || 'La password deve contenere almeno un numero',
        v => /[!@#$%^&*(),.?":{}|<>]/.test(v) || 'La password deve contenere almeno un carattere speciale',
        v => /[A-Z]/.test(v) || 'La password deve contenere almeno una lettera maiuscola',
      ]
    };
  },
  mounted() {
    this.getEnti(); // Recupera l'elenco degli enti al montaggio del componente
  },
  methods: {
    // Funzione per recuperare l'elenco degli enti dall'API
    getEnti() {
      const urlApiEnti = '/admin/companies/list'; // URL API per ottenere la lista degli enti
      axios.get(urlApiEnti)
        .then((response) => {
          this.enti = response.data; // Salva la lista degli enti nella variabile enti
        })
        .catch(() => {
          this.$toast.error('Errore nel recupero degli enti'); // Notifica errore in caso di fallimento
        });
    },
    
    // Funzione per chiudere il dialog
    close() {
      this.$emit('update:dialog', false); // Chiudi il dialog e aggiorna lo stato nel componente genitore
    },

    // Funzione per inviare i dati dell'utente tramite API
    submit() {
      if (this.$refs.form.validate()) {
        const urlApiUserAdd = process.env.VUE_APP_ADMIN_USERS_ADD;
        const newUser = {
          email: this.user.email,
          name: this.user.name,
          surname: this.user.surname,
          password: this.user.password,
          role: this.user.role,
          companies: Array.isArray(this.user.ente) ? this.user.ente : [this.user.ente]
        };
        
        axios.post(urlApiUserAdd, newUser)
          .then((response) => {
            if (response.status === 200) {
              this.$emit('add-user', response.data); // Passa l'utente appena creato
              this.close();
              this.resetForm();
              this.$toast.success("Utente aggiunto con successo!");
            } else {
              throw new Error(`Errore nel server: ${response.statusText}`);
            }
          })
          .catch((error) => {
            if (error.response && error.response.status === 403) {
              this.$toast.error("Non hai i permessi per aggiungere utenti!");
            } else if (error.response && error.response.status === 400) {
              this.$toast.error("Email già in uso. Scegli un'altra email.");
            } else {
              this.$toast.error("Errore interno del server. Riprova più tardi.");
            }
          });
      } else {
        this.$toast.error("Per favore, completa il modulo correttamente.");
      }
    },    
    // Funzione per alternare la visibilità della password
    toggleShowPassword() {
      this.showPassword = !this.showPassword; // Alterna la visibilità della password
    },

    // Funzione per resettare i campi del modulo
    resetForm() {
      // Resetta i campi del modulo dopo che l'utente è stato aggiunto
      this.user = {
        email: '',
        name: '',
        surname: '',
        password: '',
        role: '',
        companies: [] // Assicurati che ente venga resettato come array vuoto
      };
    }
  }
};
</script>
