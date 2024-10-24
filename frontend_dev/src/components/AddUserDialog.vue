<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">Aggiungi Utente</span>
      </v-card-title>
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
          
          <!-- Selettore per l'ente dell'utente -->
          <!-- <v-select v-model="user.ente" :items="enti" label="Ente" required
            :rules="[v => !!v || 'Seleziona un ente']" item-text="name" item-value="id" /> -->
        </v-form>
      </v-card-subtitle>
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
        email: '',
        name: '',
        surname: '',
        password: '',
        role: ''
        //ente: '' // Campo per memorizzare l'ente selezionato
      },
      roles: [ // Opzioni per il selettore dei ruoli
        { value: 'admin', name: 'Admin' },
        { value: 'user', name: 'User' }
      ],
      // enti: [ // Elenco degli enti (città lombarde)
      //   { id: 1, name: 'Milano' },
      //   { id: 2, name: 'Bergamo' },
      //   { id: 3, name: 'Brescia' },
      //   { id: 4, name: 'Como' }
      // ],
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
    // Qui non è necessario chiamare getEnti poiché gli enti sono già definiti staticamente.
  },
  methods: {
    close() {
      this.$emit('update:dialog', false); // Chiudi il dialog e aggiorna lo stato nel componente genitore
    },
    submit() {
      // Controlla se il modulo è valido
      if (this.$refs.form.validate()) {
        const urlApiUserAdd = process.env.VUE_APP_ADMIN_USERS_ADD //variabile da .env
        axios.post(urlApiUserAdd, {
          email: this.user.email,
          name: this.user.name,
          surname: this.user.surname,
          password: this.user.password,
          role: this.user.role,
          //ente: this.user.ente // Includi l'ente nella richiesta se necessario
        })
        .then((response) => {
          if (response.status === 200) {
            this.$emit('add-user', this.user); // Passa i dati dell'utente al componente genitore
            this.close(); // Chiudi il dialog
            this.resetForm(); // Resetta il modulo
            this.$toast.success("Utente aggiunto con successo!"); // Notifica di successo
          } else {
            throw new Error(`Errore nel server: ${response.statusText}`);
          }
        })
        .catch((error) => {
          // Gestione degli errori basata sul codice di stato
          if (error.response && error.response.status === 403) {
            this.$toast.error("Non hai i permessi per aggiungere utenti!");
          } else if (error.response && error.response.status === 400) {
            this.$toast.error("Email già in uso. Scegli un'altra email.");
          } else {
            this.$toast.error("Errore interno del server. Riprova più tardi.");
          }
        });
      } else {
        this.$toast.error("Per favore, completa il modulo correttamente."); // Messaggio di errore per validazione fallita
      }
    },
    toggleShowPassword() {
      this.showPassword = !this.showPassword; // Alterna la visibilità della password
    },
    resetForm() {
      // Resetta i campi del modulo
      this.user = {
        email: '',
        name: '',
        surname: '',
        password: '',
        role: '',
        //ente: '' // Resetta il campo ente
      };
    }
  }
};
</script>
