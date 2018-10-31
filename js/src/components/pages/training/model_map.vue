<template>
  <div id="model-map">
    <div class="panel">
      <div class="panel-title">
        Model Map
      </div>

      <div id="value-map" class="panel-content"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
const width = 300
const height = 300

export default {
  name: 'ModelMap',
  computed: {
    modelList: function () {
      return this.$store.state.model_list
    }
  },
  watch: {
    modelList: function () {
      this.drawMap()
    }
  },
  methods: {
    drawMap: function () {
      if (!this.$store.state.model_list) return
      this.removeMap()

      const [rmse_list, max_abs_error_list, dataset] = this.shapeDataset()

      const svg = d3.select('#value-map')
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const xScale = d3.scaleLinear()
        .domain([0, d3.max(rmse_list, function (d) { return d })])
        .range([0, width])
      const yScale = d3.scaleLinear()
        .domain([0, d3.max(max_abs_error_list, function (d) { return d })])
        .range([height, 0])

      // get axes
      const axisx = d3.axisBottom(xScale)
        .tickSizeInner(-height)
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)
      const axisy = d3.axisLeft(yScale)
        .ticks(10)
        .tickSizeInner(-width)
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)

      // draw x axis
      let gX = svg.append('g')
        .attr('transform', 'translate(' + 0 + ',' + height + ')')
        .call(axisx)
      // draw y axis
      let gY = svg.append('g')
        .attr('transform', 'translate(' + 0 + ',' + 0 + ')')
        .call(axisy)

      stylingAxes()

      svg.append('g')
        .selectAll('circle')
        .data(dataset)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return xScale(d[0]) })
        .attr('cy', function (d) { return yScale(d[1]) })
        .attr('fill', 'blue')
        .attr('r', 4)

      function stylingAxes () {
        gX.selectAll('path')
          .style('stroke', d3.rgb(128, 128, 128, 0.5))
        gX.selectAll('line')
          .style('stroke', d3.rgb(0, 0, 0, 0.2))
          .style('stroke-dasharray', '2,2')
        gX.selectAll('.tick').selectAll('text')
          .style('fill', d3.rgb(0, 0, 0, 0.5))
          .style('font-size', '0.60em')

        gY.selectAll('path')
          .style('stroke', d3.rgb(128, 128, 128, 0.5))
        gY.selectAll('line')
          .style('stroke', d3.rgb(0, 0, 0, 0.2))
          .style('stroke-dasharray', '2,2')
        gY.selectAll('.tick').selectAll('text')
          .style('fill', d3.rgb(0, 0, 0, 0.5))
          .style('font-size', '0.60em')
      }
    },
    removeMap: function () {
      d3.select('#value-map').selectAll('*').remove()
    },
    shapeDataset: function () {
      let rmse_list = []
      let max_abs_error_list = []
      let dataset = []
      for (let m of this.$store.state.model_list) {
        let d = [m['best_epoch_rmse'], m['best_epoch_max_abs_error']]
        rmse_list.push(m['best_epoch_rmse'])
        max_abs_error_list.push(m['best_epoch_max_abs_error'])
        dataset.push(d)
      }
      return [rmse_list, max_abs_error_list, dataset]
    }
  }
}
</script>

<style lang="scss" scoped>
#model-map {
}
</style>
