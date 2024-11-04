<template>
  <div id="chart">
    <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
<script>
import VueApexCharts from 'vue-apexcharts'
import axios from 'axios';

export default {
  name: "ColumsChart",
  components: {
    apexchart: VueApexCharts,
  },
  data: () => ({
    series: [],
    chartOptions: {
      colors: ['#8B0000', '#FF0000', '#ff7f0e', '#2ca02c'],
      chart: {
        type: 'bar',
        height: 350,
        width: "100%",
        stacked: true,
        toolbar: {
          show: true,
          tools: {
            download: false,
            pan: false,
          }
        },
        zoom: {
          enabled: true
        }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '80%',
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
        type: 'datetime',
        categories: [],
        tickPlacement: 'between',
        labels: {
          formatter: (val, timestamp, opts) => {
            let date = new Date(val);
            let formattedDate = date.toLocaleDateString('it-IT', { day: 'numeric', month: 'short' });
            return formattedDate
          }
        }
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
            let date = new Date(val);
            let formattedDate = date.toLocaleDateString();
            return formattedDate
          }
        }
      }
    },
  }),
  props: ['data'],
  methods: {
    formatData() {
    let dataFromMongoDB = this.data; // Inserisci qui i tuoi dati
    
    // Mappatura per ottenere le informazioni chiave dei progetti
    let projects = dataFromMongoDB.map(item => ({ date: item.date, name: item.name, cliente: item.company }));

    let dateCounts = {}; // Oggetto per tenere traccia delle date e dei conteggi

    projects.forEach(project => {
        if (!dateCounts[project.date]) {
            dateCounts[project.date] = dataFromMongoDB.find(item => item.name === project.name && item.company === project.cliente).findings;
        } else {
            dateCounts[project.date] = dateCounts[project.date].concat(dataFromMongoDB.find(item => item.name === project.name && item.company === project.cliente).findings);
        }
    });
    
    // Categorie di severità da usare nel grafico
    let severities = ['Critical', 'High', 'Medium', 'Low'];

    let chartData = severities.map(severity => {
        let data = [];
        for (let date in dateCounts) {
            let count = dateCounts[date].filter(entry => entry['severity'].toLowerCase() === severity.toLowerCase()).length;
            data.push(count);
        }
        return { name: severity, data: data };
    });

    // Creazione delle categorie (date) per l'asse x
    let categories = Object.keys(dateCounts).map(date => date + ' GMT');

    let finalChartObject = {
        chartData: chartData,
        xaxis: { type: 'datetime', categories: categories },
    };

    this.series = finalChartObject.chartData;

    // Configurazione delle opzioni del grafico
    this.chartOptions = {
        ...this.chartOptions,
        chart: {
            ...this.chartOptions.chart,
            stacked: categories.length > 1,
        },
        xaxis: finalChartObject.xaxis
    };
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
}
</script>
