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
    let tipologies = {}; // Oggetto per memorizzare le tipologie e i loro conteggi
    let categorie_fisse = ['Injection', 'Security Misconfiguration', 'Insecure Design', 'Broken Access Control', 'Cryptographic Failures']; // Categorie fisse

    // Itera su ogni elemento in dataRemediation.findings
    this.dataRemediation.findings.forEach(entry => {
        // Se l'elemento ha una proprietà 'vulnType'
        if (entry['vulnType']) {
            // Se non abbiamo ancora visto questa vulnType, aggiungila all'oggetto 'tipologies' con un conteggio di 1
            if (!tipologies[entry['vulnType']]) {
                tipologies[entry['vulnType']] = 1;
            } else {
                // Altrimenti, aumenta il conteggio di 1
                tipologies[entry['vulnType']]++;
            }
        }
    });

    let seriesData = []; // Array per i dati della serie
    let categories = []; // Array per le categorie

    // Itera su ogni vulnType in 'tipologies'
    for (let tipology in tipologies) {
        // Aggiungi il conteggio della vulnType ai dati della serie
        seriesData.push(tipologies[tipology]);
        // Aggiungi il nome della vulnType alle categorie
        categories.push(tipology);
    }

    // Se ci sono meno di 5 categorie
    let index_fisse = 0;
    while (categories.length < 5 && index_fisse < categorie_fisse.length) {
        let vulnType = categorie_fisse[index_fisse];
        // Evita di aggiungere categorie duplicate
        if (!categories.includes(vulnType)) {
            // Aggiungi la vulnType fissa alle categorie
            categories.push(vulnType);
            // Aggiungi un conteggio di 0 ai dati della serie per questa vulnType
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