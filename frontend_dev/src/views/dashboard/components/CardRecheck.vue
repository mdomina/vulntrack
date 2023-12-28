<template>
    <div>
        <v-row class="justify-center">
            <v-col cols="4">
                <v-card :elevation="0" dark color="#8B0000">
                    <v-card-title class="justify-center">
                        {{ vulns.critica }}
                    </v-card-title>
                    <v-card-text class="text-center">
                        Critiche
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card :elevation="0" dark color="#FF0000">
                    <v-card-title class="justify-center">
                        {{ vulns.alta }}
                    </v-card-title>
                    <v-card-text class="text-center">
                        Alte
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-row class="justify-center">
            <v-col cols="4">
                <v-card :elevation="0" dark color="#ff7f0e">
                    <v-card-title class="justify-center">
                        {{ vulns.media }}
                    </v-card-title>
                    <v-card-text class="text-center">
                        Medie
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card :elevation="0" dark color="#2ca02c">
                    <v-card-title class="justify-center">
                        {{ vulns.bassa }}
                    </v-card-title>
                    <v-card-text class="text-center">
                        Basse
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>
<script>
export default {
    data: () => ({
        vulns: {}
    }),
    props: ['data'],
    methods:{
        formatData(){
            let vulnerabilitaCount = {
                'critica': 0,
                'alta': 0,
                'media': 0,
                'bassa': 0,
            };

            for (let item of this.data) {
                for (let vulnerabilita of item.data) {
                    if (vulnerabilita.gravità in vulnerabilitaCount) {
                        vulnerabilitaCount[vulnerabilita.gravità]++;
                    }
                }
            }

            this.vulns = vulnerabilitaCount;
        }
    },
    watch: {
        data: {
            deep: true,
            handler() {
                this.formatData();
            },
        },
    }
}
</script>