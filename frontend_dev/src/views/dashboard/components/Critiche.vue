<template>
    <div id="chart">
        <apexchart type="donut" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
    components: {
        apexchart: VueApexCharts,
    },
    data: () => ({
        series: [],
        chartOptions: {
            chart: {
                type: 'donut',
                height: "100%",
                width: "100%",
            },
            dataLabels: {
                enabled: false,
            },
            tooltip:{
                enabled: false
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '80%',
                        labels: {
                            show: true,
                            value: {
                                show: true,
                                formatter: function (val) {
                                    return val - 1;
                                }
                            },
                            name: {
                                show: true,
                                formatter: function (val) {
                                    return 'Critiche'
                                }
                            }
                        }
                    }
                }
            },
            //labels: ['Bassa', 'Media', 'Alta', 'Critica'],
            colors: ['#8B0000'],
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }],
            legend: {
                show: false
            }
        },
    }),
    props: ['dataRemediation'],
    methods: {
        countVulnerabilities() {
            const severities = ['Critical'];  // Modifica la severità come desiderato
            let counts = [];

            severities.forEach(severity => {
                let count = 0;

                this.dataRemediation.forEach(item => {
                    count += item.findings.filter(entry => entry['severity'].toLowerCase() === severity.toLowerCase()).length;
                });

                counts.push(count);
            });

            this.series = counts;
        },
    },
    watch: {
        dataRemediation: {
            deep: true,
            handler() {
                this.countVulnerabilities();
            },
        },
    },
}


</script>