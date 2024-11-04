<template>
    <div>
        <v-row class="justify-center">
            <v-col cols="4">
                <v-card :elevation="0" dark color="#8B0000">
                    <v-card-title class="justify-center">
                        {{ vulns.critical }}
                    </v-card-title>
                    <v-card-text class="text-center">
                        Critiche
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card :elevation="0" dark color="#FF0000">
                    <v-card-title class="justify-center">
                        {{ vulns.high }}
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
                        {{ vulns.medium }}
                    </v-card-title>
                    <v-card-text class="text-center">
                        Medie
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="4">
                <v-card :elevation="0" dark color="#2ca02c">
                    <v-card-title class="justify-center">
                        {{ vulns.low }}
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
        vulns: {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
        }
    }),
    props: {
        data: {
            type: Object,
            default: () => ({})
        }
    },
    methods: {
        formatData() {
            // Inizializza le vulnerabilità a zero
            let vulnerabilitaCount = {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
            };
            if (this.data.findings && Array.isArray(this.data.findings)) {
                for (let vulnerabilita of this.data.findings) {
                    const severity = vulnerabilita.severity.toLowerCase();
                    if (severity in vulnerabilitaCount) {
                        vulnerabilitaCount[severity]++;
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
    },
    mounted() {
        this.formatData();
    }
}
</script>
