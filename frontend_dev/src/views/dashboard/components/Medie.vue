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
            dataLabels:{
                enabled: false,
            },
            tooltip:{
                enabled: false
            },
            plotOptions: {
                pie: {
                    donut: {
                        size:'80%',
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
                                    return 'Medie'
                                }
                            }
                        }
                    }
                }
            },
            //labels: ['Bassa', 'Media', 'Alta', 'Critica'],
            colors: ['#ff7f0e'],
           /*  responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }], */
            legend: {
                show: false
            }
        },
    }),
    props: ['dataRemediation'],
    methods: {
        countVulnerabilities() {
            const severities = ['media'];
            let counts = [];

            severities.forEach(severity => {
                let count = 1;

                this.dataRemediation.forEach(item => {
                    count += item.data.filter(entry => entry['gravità'].toLowerCase() === severity).length;
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