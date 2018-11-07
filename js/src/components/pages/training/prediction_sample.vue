<template>
  <div id="prediction-result">
    <div class="panel">
      <div class="panel-title">
        Prediction Sample
      </div>

      <div class="panel-content plots-area">
        <div id="deployed-plot" class="column">
          <div class="x-axis-name">True</div>
          <div class="y-axis-name">Prediction</div>
        </div>

        <div id="selected-plot" class="column">
          <div class="x-axis-name">True</div>
          <div class="y-axis-name">Prediction</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: 'PreictionResult',
  computed: {
    selectedModel: function () {
      return this.$store.state.selected_model
    },
    deployedModelPred: function () {
      return this.$store.state.deployed_model_y_pred
    }
  },
  watch: {
    selectedModel: function () {
      this.drawSelected()
    },
    deployedModelPred: function () {
      this.drawDeployed()
    }
  },
  mounted: function () {
    this.drawSelected()
    this.drawDeployed()
  },
  methods: {
    drawTruePredPlot: function (id, y_valid, y_pred) {
      const dataset = this.shapeDataset(y_valid, y_pred)

      const parent_area = d3.select(id)
      const width = parent_area._groups[0][0].clientWidth
      const height = parent_area._groups[0][0].clientHeight
      const margin = { 'left': 60, 'top': 40, 'right': 40, 'bottom': 60 }

      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const xScale = d3.scaleLinear()
        .domain([d3.min(y_valid, function (d) { return d }), d3.max(y_valid, function (d) { return d })])
        .range([margin.left, width - margin.right])
      const yScale = d3.scaleLinear()
        .domain([d3.min(y_valid, function (d) { return d }), d3.max(y_valid, function (d) { return d })])
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
        .attr('x1', xScale(d3.min(y_valid, function (d) { return d })))
        .attr('x2', xScale(d3.max(y_valid, function (d) { return d })))
        .attr('y1', yScale(d3.min(y_valid, function (d) { return d })))
        .attr('y2', yScale(d3.max(y_valid, function (d) { return d })))
        .attr('stroke-width', 1)
        .attr('stroke', 'gray')

      // draw sd line dummy
      const dummyArray = [...Array(46).keys()].map(function (i) { return i + 5 })
      svg.append('path')
        .datum(dummyArray)
        .attr('fill', 'green')
        .attr('opacity', 0.1)
        .attr('d', d3.area()
          .x(function (d) { return xScale(d) })
          .y1(function (d) { return yScale(d - 5) })
          .y0(function (d) { return yScale(d + 5) })
          .curve(d3.curveCardinal)
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
    drawDeployed: function () {
      if (this.$store.state.deployed_model_y_pred.length === 0) return
      this.removeDeployed()
      const y_valid = this.$store.state.deployed_model_y_valid
      const y_pred = this.$store.state.deployed_model_y_pred
      this.drawTruePredPlot('#deployed-plot', y_valid, y_pred)
    },
    drawSelected: function () {
      if (!this.$store.state.selected_model) return
      this.removeSelected()
      const y_valid = this.$store.state.selected_y_valid
      const y_pred = this.$store.state.selected_y_pred
      this.drawTruePredPlot('#selected-plot', y_valid, y_pred)
    },
    removeDeployed: function () {
      d3.select('#deployed-plot').selectAll('svg').remove()
    },
    removeSelected: function () {
      d3.select('#selected-plot').selectAll('svg').remove()
    },
    shapeDataset: function (valid, pred) {
      let dataset = []
      for (let i in valid) {
        let d = [valid[i], pred[i]]
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
  height: $prediction-sample-height;

  .plots-area {
    @include prefix("display", "flex");
    .column {
      position: relative;
      width: 50%;

      .x-axis-name, .y-axis-name {
        position: absolute;
        font-size: 0.8rem;
        color: $gray;
      }
      .x-axis-name {
        bottom: 24px;
        left: 50%;
        @include prefix("transform", "translateX(-50%)");
      }
      .y-axis-name {
        top: 16px;
        left: 16px;
      }
    }
  }
}
</style>
