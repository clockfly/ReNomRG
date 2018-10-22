<template>
  <div id="dashboard-count-bar">
    <div class='title'>Total Models: {{model_list.length}}</div>
    <canvas id="horizontal-stack-bar"></canvas>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Chart from 'chart.js'

export default {
  name: 'DashboardCountBar',
  computed: mapState(['model_list']),
  mounted: function () {
    this.drawBar()
  },
  updated: function () {
    this.drawBar()
  },
  methods: {
    drawBar: function () {
      // crate chart dataset
      let datasets = [{
        label: 'RandomForest',
        data: [this.model_list.length],
        backgroundColor: '#000068'
      }]

      // init canvas
      let parent = document.getElementById('dashboard-count-bar')
      let canvas = document.getElementById('horizontal-stack-bar')
      let ctx = canvas.getContext('2d')
      ctx.canvas.width = parent.clientWidth
      ctx.canvas.height = 100

      // set chart data
      let chart_data = {
        labels: [''],
        datasets: datasets
      }

      // set char options
      var options = {
        animation: {
          duration: 0
        },
        scales: {
          xAxes: [{
            display: false,
            stacked: true
          }],
          yAxes: [{
            display: false,
            stacked: true,
            barParcentage: 0.5,
            categoryPercentage: 0.5
          }]
        },
        responsive: false,
        maintainAspectRatio: false,
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            boxWidth: 10,
            fontSize: 10
          }
        },
        tooltips: {
          bodyFontSize: 10
        }
      }

      // remove chart for redraw.
      if (this.chart) this.chart.destroy()

      // draw chart
      this.chart = new Chart(ctx, {
        type: 'horizontalBar',
        data: chart_data,
        options: options })
    }
  }
}
</script>

<style lang="scss" scoped>
#dashboard-count-bar {
  $title-height: 24px;
  $title-font-size: 16px;
  $font-weight-medium: 500;

  overflow: visible;

  .title {
    line-height: $title-height;
    font-size: $title-font-size;
    font-weight: $font-weight-medium;
  }
}
</style>
