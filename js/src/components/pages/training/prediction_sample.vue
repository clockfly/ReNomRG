<template>
  <div id="prediction-result">
    <div class="panel">
      <div class="panel-title">
        Prediction Sample
      </div>

      <div class="panel-content plots-area">
        <div id="deployed-plot" class="column"></div>
        <div id="selected-plot" class="column"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
const width = 300
const height = 300

export default {
  name: 'PreictionResult',
  computed: {
    selectedModel: function () {
      return this.$store.state.selected_model
    }
  },
  watch: {
    selectedModel: function () {
      this.drawSelected()
    }
  },
  mounted: function () {
    this.drawSelected()
    // this.drawDeployed()
  },
  methods: {
    drawDeployed: function () {
      console.log('deployed')
    },
    drawSelected: function () {
      if (!this.$store.state.selected_model) return
      this.removeSelected()

      const y_valid = this.$store.state.selected_y_valid
      const y_pred = this.$store.state.selected_y_pred
      const dataset = this.shapeDataset()

      const svg = d3.select('#selected-plot')
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const xScale = d3.scaleLinear()
        .domain([d3.min(y_valid, function (d) { return d }), d3.max(y_valid, function (d) { return d })])
        .range([0, width])
      const yScale = d3.scaleLinear()
        .domain([d3.min(y_pred, function (d) { return d }), d3.max(y_pred, function (d) { return d })])
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

      // draw diagonal line
      svg.append('line')
        .attr('x1', d3.min(y_valid, function (d) { return xScale(d) }))
        .attr('x2', d3.max(y_valid, function (d) { return xScale(d) }))
        .attr('y1', height - d3.min(y_valid, function (d) { return xScale(d) }))
        .attr('y2', height - d3.max(y_valid, function (d) { return xScale(d) }))
        .attr('stroke-width', 1)
        .attr('stroke', 'gray')

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
    removeDeployed: function () {
      d3.select('#deployed-plot').selectAll('*').remove()
    },
    removeSelected: function () {
      d3.select('#selected-plot').selectAll('*').remove()
    },
    shapeDataset: function () {
      let dataset = []
      for (let i in this.$store.state.selected_y_valid) {
        let d = [this.$store.state.selected_y_valid[i], this.$store.state.selected_y_pred[i]]
        dataset.push(d)
      }
      return dataset
    }
  }
}
</script>

<style lang="scss" scoped>
#prediction-result {
  width: 100%;

  .plots-area {
    @include prefix("display", "flex");
    .column {
      width: 50%;
    }
  }
}
</style>
