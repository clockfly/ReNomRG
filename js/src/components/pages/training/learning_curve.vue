<template>
  <div id="learning-curve">
    <div class="panel">
      <div class="panel-title">
        Learning Curve
      </div>
      <div id="curve-canvas" class="panel-content">
        <div class="x-axis-name">Epoch</div>
        <div class="y-axis-name">Loss [-]</div>
        <div class="bar-legends">
          <div class="legend">
            <div class="legend-color train"></div>
            <div class="legend-name">Train</div>
          </div>

          <div class="legend">
            <div class="legend-color validation"></div>
            <div class="legend-name">Validation</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
const train_color = '#0762ad'
const valid_color = '#ef8200'

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

      const parent_area = d3.select('#curve-canvas')
      const width = parent_area._groups[0][0].clientWidth
      const height = parent_area._groups[0][0].clientHeight
      const margin = { 'left': 60, 'top': 40, 'right': 60, 'bottom': 40 }

      const svg = d3.select('#curve-canvas')
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const xScale = d3.scaleLinear()
        .domain([0, this.trainList.length])
        .range([margin.left, width - margin.right])
      const yScale = d3.scaleLinear()
        .domain([0, d3.max(this.trainList, function (d) { return d })])
        .range([height - margin.bottom, margin.top])

      // get axes
      const axisx = d3.axisBottom(xScale)
        .tickSizeInner(-(height - margin.top - margin.bottom))
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)
      const axisy = d3.axisLeft(yScale)
        .ticks(10)
        .tickSizeInner(-(width - margin.left - margin.right))
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)

      // draw x axis
      let gX = svg.append('g')
        .attr('transform', 'translate(' + 0 + ',' + (height - margin.bottom) + ')')
        .call(axisx)
      // draw y axis
      let gY = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + 0 + ')')
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
      d3.select('#curve-canvas').selectAll('svg').remove()
    }
  }
}
</script>

<style lang="scss" scoped>
#learning-curve {
  width: 100%;
  height: $learning-curve-height;

  #curve-canvas {
    position: relative;

    .x-axis-name, .y-axis-name, .bar-legends {
      position: absolute;
      font-size: 0.5rem;
      color: $gray;
    }
    .x-axis-name {
      bottom: 12px;
      right: 40px;
    }
    .y-axis-name {
      top: 16px;
      left: 32px;
    }
    .bar-legends {
      @include prefix("display", "flex");
      top: 16px;
      right: 16px;

      .legend {
        @include prefix("display", "flex");
        justify-content: center;
        align-items: center;
        margin-right: 16px;

        .legend-color {
          width: 8px;
          height: 8px;
          margin-right: 4px;
        }
      }
    }
  }
}
</style>
