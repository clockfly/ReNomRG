<template>
  <div id="model-plot">
    <canvas id="accuracy-plot"></canvas>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Chart from 'chart.js'

export default {
  name: 'ModelPlot',
  computed: mapState(['selected_model_id', 'model_list']),
  watch: {
    model_list () {
      this.drawScatter()
    },
    selected_model_id () {
      this.drawScatter()
    }
  },
  mounted: function () {
    this.drawScatter()
  },
  methods: {
    plotData: function (model_id, algorithm, rmse, r2) {
      return {
        'model_id': model_id,
        'algorithm': algorithm,
        'algorithm_name': 'Random Forest',
        'rmse': this.round(rmse),
        'r2': this.round(r2),
        'x': rmse,
        'y': r2
      }
    },
    round: function (v) {
      return Math.round(v * 1000) / 1000
    },
    drawScatter: function () {
      const self = this

      // calc plot dataset
      const selected_color = '#999999'
      let tooltip_colors = [selected_color, '#000068']

      // init coordinate data
      let coordinate_data = {
        'Selected': {
          data: [],
          backgroundColor: selected_color,
          pointRadius: 10,
          pointHoverRadius: 12,
          pointStyle: 'rectRot'
        },
        'RandomForest': {
          data: [],
          backgroundColor: '#000068',
          pointRadius: 4,
          pointHoverRadius: 6,
          pointStyle: 'circle'
        }
      }

      // add model coordinate to coordinate_data
      for (let model of this.model_list) {
        if (model.model_id === this.$store.state.selected_model_id) {
          coordinate_data['Selected'].data.push(this.plotData(model.model_id, model.algorithm, model.rmse, model.r2_score))
        } else {
          coordinate_data['RandomForest'].data.push(this.plotData(model.model_id, model.algorithm, model.rmse, model.r2_score))
        }
      }

      // create datasets from coordinate data
      let datasets = [coordinate_data['Selected'], coordinate_data['RandomForest']]

      // canvas
      let parent = document.getElementById('model-plot')
      let parent_width = parent.style.width
      let parent_height = parent.style.height
      let canvas = document.getElementById('accuracy-plot')
      let ctx = canvas.getContext('2d')

      canvas.width = parent_width
      canvas.height = parent_height

      // set chart data
      let chart_data = {
        datasets: datasets
      }

      // set chart options
      var options = {
        events: ['click', 'mousemove'],
        'onClick': function (evt, item) {
          if (item.length > 0) {
            const index = item[0]._index
            const datasetIndex = item[0]._datasetIndex
            const selectedModel = datasets[datasetIndex].data[index]
            const model_id = selectedModel.model_id
            self.$store.commit('setSelectedModel', {
              'model_id': model_id
            })
          }
        },
        animation: {
          duration: 0
        },
        scales: {
          xAxes: [{
            position: 'bottom',
            // ticks: {
            //   min: 0,
            //   max: 100
            // },
            scaleLabel: {
              display: true,
              labelString: 'RMSE'
            }
          }],
          yAxes: [{
            position: 'left',
            // ticks: {
            //   min: 0,
            //   max: 100
            // },
            scaleLabel: {
              display: true,
              labelString: 'R2'
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
        legend: false,
        tooltips: {
          // set custom tooltips
          enable: true,
          intersect: true,
          custom: function (tooltip) {
            if (!tooltip) return
            tooltip.displayColors = false
          },
          titleFontSize: 16,
          titleSpacing: 4,
          bodyFontSize: 14,
          xPadding: 12,
          yPadding: 12,
          callbacks: {
            // set custom tooltips
            title: function (item, data) {
              const model_id = datasets[item[0].datasetIndex].data[item[0].index].model_id
              return 'Model ID: ' + model_id
            },
            label: function (item, data) {
              const model = datasets[item.datasetIndex].data[item.index]
              const algorithm = model.algorithm_name
              const rmse = model.rmse
              const r2 = model.r2
              return ['Algorithm: ' + algorithm, 'RMSE: ' + rmse, 'R2: ' + r2]
            },
            labelColor: function (item, chart) {
              chart.tooltip._model.backgroundColor = tooltip_colors[item.datasetIndex]
            }
          }
        }
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

#model-plot {
  width: 100%;
  height: 100%;
}
</style>
