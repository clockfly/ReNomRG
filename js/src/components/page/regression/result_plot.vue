<template>
  <div id="result-plot">
    <canvas id="prediction-plot"></canvas>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Chart from 'chart.js'

export default {
  name: 'ResultPlot',
  computed: mapState(['selected_model', 'valid_true']),
  watch: {
    selected_model () {
      if (this.selected_model) {
        this.drawScatter()
      }
    }
  },
  mounted: function () {
    if (this.selected_model) {
      this.drawScatter()
    }
  },
  methods: {
    drawScatter: function () {
      const self = this
      const color = '#0762ad'

      const a = this.valid_true.concat(this.selected_model.valid_pred)
      const min = Math.min.apply(null, a)
      const max = Math.max.apply(null, a)

      let plot_data = this.valid_true.map(function (e, i) {
        return {'x': e, 'y': self.selected_model.valid_pred[i]}
      })

      let datasets = [{
        data: plot_data,
        backgroundColor: color
      }]

      // canvas
      let parent = document.getElementById('result-plot')
      let parent_width = parent.style.width
      let parent_height = parent.style.height
      let canvas = document.getElementById('prediction-plot')
      let ctx = canvas.getContext('2d')

      canvas.width = parent_width
      canvas.height = parent_height

      // set chart data
      let chart_data = {
        datasets: datasets
      }

      // set chart options
      var options = {
        animation: {
          duration: 0
        },
        scales: {
          xAxes: [{
            position: 'bottom',
            ticks: {
              min: min,
              max: max
            },
            scaleLabel: {
              display: true,
              labelString: 'True'
            }
          }],
          yAxes: [{
            position: 'left',
            ticks: {
              min: min,
              max: max
            },
            scaleLabel: {
              display: true,
              labelString: 'Predict'
            }
          }]
        },
        layout: {
          padding: {
            top: 24,
            bottom: 0,
            left: 24,
            right: 24
          }
        },
        legend: false
      }

      if (this.chart) this.chart.destroy()
      this.chart = new Chart(ctx, {
        type: 'scatter',
        data: chart_data,
        options: options })
    }
  }
}
</script>

<style lang="scss" scoped>
#result-plot {
  width: 100%;
  height: 100%;
}
</style>
