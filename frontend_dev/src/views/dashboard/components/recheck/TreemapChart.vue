<template>
    <div id="chart">
        <apexchart type="treemap" :options="chartOptions" :series="series"></apexchart>
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
            legend: {
                show: false
            },
            chart: {
                height: '100%',
                width: '100%',
                type: 'treemap',
                toolbar: {
                    show: false
                }
            },
            dataLabels: {
                style: {
                    fontSize: '14px',
                    fontFamily: 'Helvetica, Arial, sans-serif',  // Cambia il nome del font qui
                }
            },
        },
    }),
    props: ['dataRemediation'],
    methods: {
        formatData() {
            let vulnerabilityCount = {};

            // Verifica che findings esista come array in dataRemediation
                this.dataRemediation.findings.forEach((vulnerability) => {
                    let vulnerabilityName = vulnerability['title'];
                    if (vulnerabilityCount[vulnerabilityName]) {
                        vulnerabilityCount[vulnerabilityName]++;
                    } else {
                        vulnerabilityCount[vulnerabilityName] = 1;
                    }
                });

            let vulnerabilityCountArray = [];
            for (const vulnerability in vulnerabilityCount) {
                vulnerabilityCountArray.push({ x: vulnerability.replace(' ', "\n"), y: vulnerabilityCount[vulnerability] });
            }

            this.series = [{ data: vulnerabilityCountArray }];
        }


    },
    watch: {
        dataRemediation: {
            deep: true,
            handler() {
                this.formatData();
            },
        },
    }

}

</script>