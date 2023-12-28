<template>
    <div id="chart">
        <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>
<script>
import VueApexCharts from 'vue-apexcharts'

export default {
    name: "ColumsChart",
    components: {
        apexchart: VueApexCharts,
    },
    data: () => ({
        series: [
            {
                name: 'Vulnerabilità',
                data: [0, 1, 2, 3]
            }
        ],
        chartOptions: {
            colors: ['#8B0000', '#FF0000', '#ff7f0e', '#2ca02c'],
            chart: {
                type: 'bar',
                height: 350,
                width: "100%",
                stacked: false,
                toolbar: {
                    show: false,
                    tools: {
                        download: false,
                        pan: false,
                    }
                },
            },
            plotOptions: {
                bar: {
                    horizontal: true,
                    columnWidth: '80%',
                    distributed: true,
                    dataLabels: {
                        total: {
                            enabled: true,
                            distributed: true,
                            /*style: {
                              fontSize: '13px',
                              fontWeight: 900
                            }*/
                        }
                    }
                },
            },
            xaxis: {
                categories: ['Critica', 'Alta', 'Media', 'Bassa'],
                tickPlacement: 'on',
                tickAmount: 1,
                labels: {
                    formatter: function (value) {
                        // Arrotonda il valore al numero intero più vicino
                        return Math.round(value);
                    }
                },
            },
            yaxis: {
            },
            legend: {
                position: 'bottom',
            },
            fill: {
                opacity: 1
            },
            tooltip: {
                x: {
                    formatter: (val, { series, seriesIndex, dataPointIndex, w }) => {
                        return val
                    }
                },
                y: {
                    formatter: (val, { series, seriesIndex, dataPointIndex, w }) => {
                        return val
                    }
                }
            }
        },
    }),
    props: ['data'],
    methods: {
        formatData() {
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

            let series = [{
                name: 'Vulnerabilità',
                data: Object.values(vulnerabilitaCount) // questo ti darà un array [0, 3, 0, 1] (o qualunque sia il conteggio)
            }];

            this.series = series
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