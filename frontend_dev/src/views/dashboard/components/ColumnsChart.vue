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

      let projects = dataFromMongoDB.map(item => ({ date: item.data[0]['ultimo aggiornamento'], name: item.nome }));

      let dateCounts = {}; // Un oggetto per tenere traccia delle date e dei conteggi

      projects.forEach(project => {
        if (!dateCounts[project.date]) {
          dateCounts[project.date] = dataFromMongoDB.find(item => item.nome === project.name && item.cliente === project.cliente).data;
        } else {
          dateCounts[project.date] = dateCounts[project.date].concat(dataFromMongoDB.find(item => item.nome === project.name && item.cliente === project.cliente).data);
        }
      });

      let severities = ['Critica', 'Alta', 'Media', 'Bassa'];

      let chartData = severities.map(severity => {
        let data = [];
        for (let date in dateCounts) {
          let count = dateCounts[date].filter(entry => entry['gravità'].toLowerCase() === severity.toLowerCase()).length;
          data.push(count);
        }
        return { name: severity, data: data };
      });

      let categories = Object.keys(dateCounts).map(date => date + ' GMT');

      /*let xaxis = categories.length > 0
        ? { type: 'datetime', categories: categories }
        : { categories: categories };*/



      let finalChartObject = {
        chartData: chartData,
        xaxis: { type: 'datetime', categories: categories },
      };


      this.series = finalChartObject.chartData;

      // Creiamo un nuovo oggetto chartOptions. 
      // L'operatore di spread (...) per creare una copia di chartOptions, quindi sostituisce:
      // se categories.length > 1 allora stacked è true altrimenti è false
      // la proprietà xaxis
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
