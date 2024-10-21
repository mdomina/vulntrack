<template>
    <v-container fluid class="down-top-padding">
        <v-row justify="center">
            <v-col cols="12" lg="9">
                <v-card>
                    <v-card-title>
                        <v-progress-linear indeterminate color="cyan" v-if="progress"></v-progress-linear>
                    </v-card-title>
                    <v-card-text>
                        <v-form v-model="valid" @submit.prevent="invia" ref="form">
                            <v-file-input label="File input" v-model="file" outlined dense counter show-size required
                                accept=".xlsx"></v-file-input>
                            
                            <v-btn type="submit" color="primary">Invia</v-btn>
                        </v-form>

                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import axios from 'axios'
import { mapActions } from 'vuex';
export default {
    name: "Upload",
    components: {
    },
    data: () => ({
        valid: false,
        file: null,
        progress: false
    }),
    methods: {
        invia() {
            // attivo la barra di caricamento
            this.progress = true

            // Create a new FormData instance
            let formData = new FormData();

            // Add the file to the form data
            formData.append("file", this.file);
            // Add other form data
            if (this.valid) {
                const urlBackend = process.env.VUE_APP_ADMIN_UPLOADFILE;
                // Use axios to send the file to the endpoint
                axios.post(urlBackend, formData, { headers: { "Content-Type": "multipart/form-data" } }).then(res => {
                    // disattivo la barra di caricamento
                    this.progress = false

                    this.$toasted.success('File caricato con successo', { duration: 3000, theme: "bubble" });
                    this.$refs.form.reset();
                    
                }).catch(err => {
                    // disattivo la barra di caricamento
                    this.progress = false
                    if (err.response.data.detail == 'File esistente'){
                        this.$toasted.error('Il file è già stato caricato', { duration: 3000, theme: "bubble" });
                    }
                    else if (err.response.data.detail == 'nome file errato'){
                        this.$toasted.error('VAPT Anno - Cliente - Codice Elettra - Nome App - Recheck (se è un recheck) -Remediation Plan', { duration: 5000, theme: "bubble" });
                    }
                    else if (err.response.data.detail == 'Errore lettura file'){
                        this.$toasted.error('Formattazione del file sbagliata', { duration: 3000, theme: "bubble" });
                    }
                    else if (err.response.data.detail == 'Errore estrazione mese'){
                        this.$toasted.error('Formattare la data in GG/MM/YYYY', { duration: 5000, theme: "bubble" });
                    }
                    else if (err.response.data.detail == 'Errore colonna Gravità'){
                        this.$toasted.error('Formattare i valori della colonna Gravità con Bassa, Media, Alta, Critica', { duration: 5000, theme: "bubble" });
                    }
                    else{
                        this.$toasted.error('Upload file fallito', { duration: 3000, theme: "bubble" });
                    }
                })
            }


        },
        ...mapActions(
             ['checkAuth']
        )
    },
    beforMount(){
        this.checkAuth();
    },
    mounted() {
    }
}
</script>