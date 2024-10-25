<template>
    <div id="chart">
        <apexchart type="pie" :options="chartOptions" :series="series"></apexchart>
    </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
    components: {
        apexchart: VueApexCharts,
    },
    data: () => ({
        series: [44, 55, 41, 17, 15],
        chartOptions: {
            chart: {
                type: 'pie',
                height: "100%",
                width: "100%",
            },
            plotOptions: {
              pie: {
                donut: {
                  labels: {
                    show: true,
                    total: {
                      showAlways: true,
                      show: false
                    }
                  }
                }
              }
            },
            labels: ['Critica', 'Alta', 'Media', 'Bassa'],
            colors: ['#8B0000', '#FF0000', '#ff7f0e', '#2ca02c' ],
            /* responsive: [{
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
                position: 'bottom'
            }
        },
    }),
    props: ['dataRemediation'],
    methods: {
        countVulnerabilities() {
            const severities = ['critical', 'high', 'medium', 'low'];
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