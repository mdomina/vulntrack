<template>
    <v-app id="inspire" style="background-color: #EEF5F9">
        <v-main>
            <v-container class="fill-height" fluid style="height: 100%;">
                <v-row justify="center">
                    <v-col cols="5">
                        <v-card elevation="2">
                            <v-card-text>
                                <v-form ref="form" v-model="valid" @submit.prevent="login">
                                    <v-text-field :rules="rules1" v-model="dataUser.username" label="Username"
                                        required></v-text-field>
                                    <v-text-field :rules="rules2" v-model="dataUser.password" label="Password"
                                        type="password" required></v-text-field>
                                    <v-btn type="submit" color="primary">Login</v-btn>
                                </v-form>
                            </v-card-text>

                        </v-card>
                    </v-col>
                </v-row>


            </v-container>
            <Footer></Footer>
        </v-main>
    </v-app>
</template>
  
<script>
import Footer from "@/layouts/footer/Footer";
import axios from 'axios';

export default {
    components: { Footer },
    data: () => ({
        valid: false,
        dataUser: {
            username: '',
            password: ''
        },
        rules1: [value => !!value || 'Required.'],
        rules2: [value => !!value || 'Required.'],
    }),
    methods: {
        login() {
            axios.post('/token', this.dataUser).then((response) => {
                localStorage.setItem('token', response.data.access_token);
                this.$store.dispatch('actSetAuth');
                this.$store.dispatch('userInfo').then(()=>{
                    this.$router.push('/')
                })
            }).catch((error) => {
                if(error.response.status == 401){
                this.$toasted.error('Username o Password Sbagliate', {duration: 3000, theme: "bubble"});

                }

            });
        }
    }
};
</script>
  