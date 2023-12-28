<template>
  <div id="chart">
    <apexchart type="radar" :options="chartOptions" :series="series"></apexchart>
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
      name: 'Series 1',
      data: [2, 0, 0, 0, 0, 0, 0],
    }],
    chartOptions: {
      chart: {
        //height: 350,
        type: 'radar',
        toolbar: {
          show: false
        },
      },
      dataLabels: {
        enabled: true
      },
      plotOptions: {
        radar: {
          size: 140,
          polygons: {
            strokeColors: '#e9e9e9',
            fill: {
              colors: ['#f8f8f8', '#fff']
            }
          }
        }
      },
      colors: ['#00b0f0'],
      /*  markers: {
        size: 4,
        colors: ['#fff'],
        strokeColor: '#0070c0',
        strokeWidth: 2,
      }, */
      tooltip: {
        y: {
          formatter: function (val) {
            return val
          }
        }
      },
      xaxis: {
        categories: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
      },
      yaxis: {
        tickAmount: 7,
        labels: {
          show: false,
          formatter: function (val, i) {
            return ''
            /* if (i % 2 === 0) {
              return val
            } else {
              return ''
            } */
          }
        }
      }
    },
  }),
  props: ['dataRemediation'],
  methods: {
    formatData() {
      let tipologies = {}; // Crea un oggetto vuoto per memorizzare le tipologie e i loro conteggi
      let categorie_fisse = ['Injection', 'Security Misconfiguration', 'Insecure Design', 'Broken Access Control', 'Cryptographic Failures']; // Definisci le categorie fisse

      // Itera su ogni elemento in dataRemediation
      this.dataRemediation.forEach(item => {
        // Itera su ogni elemento nella lista "data" dell'elemento corrente
        item.data.forEach(entry => {
          // Se l'elemento ha una proprietà 'categoria'
          if (entry['categoria']) {
            // Se non abbiamo ancora visto questa categoria, aggiungila all'oggetto 'tipologies' con un conteggio di 1
            if (!tipologies[entry['categoria']]) {
              tipologies[entry['categoria']] = 1;
            } else {
              // Altrimenti, abbiamo già visto questa categoria, quindi aumentiamo il conteggio di 1
              tipologies[entry['categoria']]++;
            }
          }
        });
      });

      let seriesData = []; // Crea un array vuoto per memorizzare i dati della serie
      let categories = []; // Crea un array vuoto per memorizzare le categorie

      // Itera su ogni categoria in 'tipologies'
      for (let tipology in tipologies) {
        // Aggiungi il conteggio della categoria ai dati della serie
        seriesData.push(tipologies[tipology]);
        // Aggiungi il nome della categoria alle categorie
        categories.push(tipology);
      }

      // Se ci sono meno di 5 categorie
      let index_fisse = 0;
      while (categories.length < 5 && index_fisse < categorie_fisse.length) {
        let categoria = categorie_fisse[index_fisse];
        // Evita di aggiungere categorie duplicate
        if (!categories.includes(categoria)) {
          // Aggiungi la categoria fissa alle categorie
          categories.push(categoria);
          // Aggiungi un conteggio di 0 ai dati della serie per questa categoria
          seriesData.push(0);
        }
        index_fisse++;
      }

      // Imposta 'series' e 'chartOptions' per l'utilizzo nel grafico
      this.series = [{ name: 'Series 1', data: seriesData }];
      this.chartOptions = {
        ...this.chartOptions,
        xaxis: { categories: categories }
      };

    }
  },
  watch: {
    dataRemediation: {
      deep: true,
      handler() {
        this.formatData();
      },
    },
  },


}

</script>