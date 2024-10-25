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
        'critical': {},
        'high': {},
        'medium': {},
        'low': {},
    };

    // Calcolo dei conteggi delle vulnerabilità per mese e severità
    this.dataRemediation.forEach(item => {
        if (!item.findings) return;  // Salta se findings è undefined

        // Estrai il mese dal campo 'date'
        let month = new Date(item.date).toLocaleString('it-IT', { month: 'long' });

        item.findings.forEach(entry => {
            let severity = entry['severity'] ? entry['severity'].toLowerCase() : null; // Verifica che severity esista
            if (!severity || !(severity in countData)) return; // Salta se severity è undefined o non è una chiave valida

            if (!(month in countData[severity])) {
                countData[severity][month] = 0;
            }
            countData[severity][month]++;
        });
    });

    // Creazione di un elenco univoco di mesi (categorie asse x)
    let uniqueMonths = [...new Set([].concat(...Object.values(countData).map(Object.keys)))];

    // Ordinamento dei mesi in ordine temporale
    const monthNames = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"];
    uniqueMonths.sort((a, b) => monthNames.indexOf(a) - monthNames.indexOf(b));

    // Creazione di dati di serie
    let series = Object.entries(countData).map(([severity, counts]) => {
        return {
            name: severity.charAt(0).toUpperCase() + severity.slice(1), // Capitalizza la severità per la leggibilità
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