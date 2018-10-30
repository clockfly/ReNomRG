<template>
  <div id="learning-curve">
    <Panel
      :banner_text="'Learning Curve'">
      <div id="curve-canvas" slot="pannel_content"></div>
    </Panel>
  </div>
</template>

<script>
import * as d3 from 'd3'
import { CURVE_COLORS } from '@/const'
import Panel from '@/components/organisms/panel'

export default {
  name: 'LerningCurve',
  components: {
    Panel
  },
  data: function () {
    return {
      'w': 300,
      'h': 300,
      'curve_colors': CURVE_COLORS
    }
  },
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
        .attr('width', this.w)
        .attr('height', this.h)

      const xScale = d3.scaleLinear()
        .domain([0, this.trainList.length])
        .range([0, this.w])
      const yScale = d3.scaleLinear()
        .domain([0, d3.max(this.trainList, function (d) { return d })])
        .range([this.h, 0])

      // get axes
      const axisx = d3.axisBottom(xScale)
        .tickSizeInner(-this.h)
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)
      const axisy = d3.axisLeft(yScale)
        .ticks(10)
        .tickSizeInner(-this.w)
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)

      // draw x axis
      let gX = svg.append('g')
        .attr('transform', 'translate(' + 0 + ',' + this.h + ')')
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
        .attr('stroke', CURVE_COLORS.train)
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
        .attr('stroke', CURVE_COLORS.validation)
        .attr('stroke-width', 1.5)
        .attr('d', d3.line()
          .x(function (d, index) { return xScale(index) })
          .y(function (d) { return yScale(d) })
          .curve(d3.curveLinear)
        )

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
