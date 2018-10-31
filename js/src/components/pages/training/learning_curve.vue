<template>
  <div id="learning-curve">
    <div class="panel">
      <div class="panel-title">
        Learning Curve
      </div>
      <div id="curve-canvas" class="panel-content"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
const train_color = '#0762ad'
const valid_color = '#ef8200'
const width = 300
const height = 300

export default {
  name: 'LerningCurve',
  computed: {
    trainList: function () {
      return this.$store.state.train_loss_list
    },
    validList: function () {
      return this.$store.state.valid_loss_list
    }
  },
  watch: {
    trainList: function () {
      this.drawCurve()
    },
    validList: function () {
      this.drawCurve()
    }
  },
  mounted: function () {
    this.drawCurve()
  },
  methods: {
    drawCurve: function () {
      this.removeData()
      const svg = d3.select('#curve-canvas')
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const xScale = d3.scaleLinear()
        .domain([0, this.trainList.length])
        .range([0, width])
      const yScale = d3.scaleLinear()
        .domain([0, d3.max(this.trainList, function (d) { return d })])
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

      let LineLayer = svg.append('g').attr('clip-path', 'url(#clip)')
      // draw line chart
      LineLayer.append('path')
        .datum(this.trainList)
        .attr('fill', 'none')
        .attr('stroke', train_color)
        .attr('stroke-width', 1.5)
        .attr('d', d3.line()
          .x(function (d, index) { return xScale(index) })
          .y(function (d) { return yScale(d) })
          .curve(d3.curveLinear)
        )

      // draw line chart
      LineLayer.append('path')
        .datum(this.validList)
        .attr('fill', 'none')
        .attr('stroke', valid_color)
        .attr('stroke-width', 1.5)
        .attr('d', d3.line()
          .x(function (d, index) { return xScale(index) })
          .y(function (d) { return yScale(d) })
          .curve(d3.curveLinear)
        )

      const axis_color = d3.rgb(128, 128, 128, 0.5)
      function stylingAxes () {
        gX.selectAll('path')
          .style('stroke', axis_color)
        gX.selectAll('line')
          .style('stroke', d3.rgb(0, 0, 0, 0.2))
          .style('stroke-dasharray', '2,2')
        gX.selectAll('.tick').selectAll('text')
          .style('fill', axis_color)
          .style('font-size', '0.60em')

        gY.selectAll('path')
          .style('stroke', axis_color)
        gY.selectAll('line')
          .style('stroke', d3.rgb(0, 0, 0, 0.2))
          .style('stroke-dasharray', '2,2')
        gY.selectAll('.tick').selectAll('text')
          .style('fill', axis_color)
          .style('font-size', '0.60em')
      }
    },
    removeData: function () {
      d3.select('#curve-canvas').selectAll('*').remove()
    }
  }
}
</script>

<style lang="scss" scoped>
#learning-curve {
}
</style>
