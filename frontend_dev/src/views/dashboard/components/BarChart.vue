<template>
    <div id="chart">
        <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
    components: {
        apexchart: VueApexCharts,
    },
    data: () => ({

        series: [{
            name: 'Bassa',
            data: [0]
        }, {
            name: 'Media',
            data: [1]
        }, {
            name: 'Alta',
            data: [0]
        }, {
            name: 'Critica',
            data: [0]
        }],
        chartOptions: {
            colors: ['#8B0000', '#FF0000', '#ff7f0e', '#2ca02c'],
            chart: {
                type: 'bar',
                height: '100%',
                stacked: true,
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    horizontal: true,
                    dataLabels: {
                        total: {
                            enabled: true,
                            offsetX: 0,
                            style: {
                                fontSize: '13px',
                                fontWeight: 900
                            }
                        }
                    }
                },
            },
            stroke: {
                width: 1,
                colors: ['#fff']
            },
            xaxis: {
                categories: [],
            },
            yaxis: {
                title: {
                    text: undefined
                },
            },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val
                    }
                }
            },
            fill: {
                opacity: 1
            },
            legend: {
                position: 'bottom',
                horizontalAlign: 'center',
                offsetX: 40
            }
        },


    }),
    props: ['dataRemediation'],
    methods: {
        formatData() {
            let countData = {
                'Critica': {},
                'Alta': {},
                'Media': {},
                'Bassa': {},
            };

            // Calcolo dei conteggi delle vulnerabilità per mese e gravità
            this.dataRemediation.forEach(item => {
                let month = item.mese;

                item.data.forEach(entry => {
                    let gravity = entry['gravità'].charAt(0).toUpperCase() + entry['gravità'].slice(1); // Conversione della gravità in formato appropriato
                    if (!(month in countData[gravity])) {
                        countData[gravity][month] = 0;
                    }
                    countData[gravity][month]++;
                });
            });

            // Creazione di un elenco univoco di mesi (categorie asse x)
            let uniqueMonths = [...new Set([].concat(...Object.values(countData).map(Object.keys)))];

            // Ordinamento dei mesi in ordine temporale
            const monthNames = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"];
            uniqueMonths.sort((a, b) => monthNames.indexOf(a) - monthNames.indexOf(b));

            // Creazione di dati di serie
            let series = Object.entries(countData).map(([gravity, counts]) => {
                return {
                    name: gravity,
                    data: uniqueMonths.map(month => counts[month] || 0)
                };
            });

            // Assegnazione dei risultati alle variabili appropriate
            this.series = series;
            this.chartOptions = {
                ...this.chartOptions,
                xaxis: { categories: uniqueMonths }
            };
        }


    },
    watch: {
        dataRemediation: {
            immediate: true,
            handler() {
                // Quando dataRemediation cambia, chiamiamo formatData
                this.formatData();
            }
        }
    }

}

</script>