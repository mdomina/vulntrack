<template>
    <v-container>
        <v-btn @click="dialog = true">Cambia Password</v-btn>

        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    Cambio Password
                </v-card-title>
                <v-card-text>
                    <v-form ref="form">
                        <v-text-field v-model="currentPassword" label="Password Attuale" autocomplete="new-password"
                            append-icon="mdi-eye-off" @click:append="toggleShowPassword"
                            :type="showPassword ? 'text' : 'password'"></v-text-field>
                        <v-text-field v-model="password"
                            :rules="[rules.required, rules.min, rules.hasNumber, rules.hasSpecialChar, rules.hasUpperCase]"
                            label="Nuova Password" autocomplete="new-password"
                            :type="showPassword ? 'text' : 'password'"></v-text-field>
                        <v-text-field v-model="confirmPassword"
                            :rules="[rules.required, rules.min, rules.hasNumber, rules.hasSpecialChar,rules.hasUpperCase, matchPassword]"
                            label="Ripeti Nuova Password" autocomplete="new-password"
                            :type="showPassword ? 'text' : 'password'"></v-text-field>

                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="dialog = false">Annulla</v-btn>
                    <v-btn color="blue darken-1" text @click="changePassword">Conferma</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>
<script>
import axios from 'axios';
export default {
    name: 'ChangePassword',
    data: () => ({
        dialog: false,
        password: '',
        confirmPassword: '',
        currentPassword: '',
        showPassword: false,
        rules: {
            required: value => !!value || 'Campo obbligatorio',
            min: v => v.length >= 12 || 'Minimo 12 caratteri',
            hasNumber: v => /\d/.test(v) || 'La password deve contenere almeno un numero',
            hasSpecialChar: v => /[!@#$%^&*(),.?":{}|<>]/.test(v) || 'La password deve contenere almeno un carattere speciale',
            hasUpperCase: v => /[A-Z]/.test(v) || 'La password deve contenere almeno una lettera maiuscola',
        }

    }),
    methods: {
        changePassword() {
            if (this.$refs.form.validate()) {
                const payload = {
                    old_password: this.currentPassword,
                    new_password: this.confirmPassword
                };
                const urlBackEnd=process.env.VUE_APP_USERS_CHANGE_PASSWORD;
                axios.post(urlBackEnd, payload)
                    .then((response) => {
                        this.$refs.form.reset();
                        this.dialog = false; // chiudi il dialog dopo il cambio
                        this.$emit('password-changed', response.data);
                        this.$toast.success("Password cambiata con successo!");
                    })
                    .catch((error) => {
                        if (error.response) {
                            switch (error.response.status) {
                                case 422:
                                    this.$toast.error("La nuova password non soddisfa i criteri di sicurezza.");
                                    break;
                                case 400:
                                    this.$toast.error("La password attuale non è corretta.");
                                    break;
                                default:
                                    this.$toast.error("Si è verificato un errore durante il cambio della password.");
                                    break;
                            }
                        } else {
                            // Gestisci gli errori che non sono dovuti a risposte HTTP
                            this.$toast.error("Errore di rete o risposta non disponibile.");
                        }
                    });
            }
        },
        toggleShowPassword() {
            this.showPassword = !this.showPassword;
        },
        matchPassword() {
            return this.password === this.confirmPassword || 'Le password non coincidono';
        }
    }
};

</script>