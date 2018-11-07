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
import { valid_color } from '@/const'
import { max, min, getScale, removeSvg, styleAxis } from '@/utils'

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
      // define svg element
      const parent_area = d3.select(id)
      const width = parent_area._groups[0][0].clientWidth
      const height = parent_area._groups[0][0].clientHeight
      const margin = { 'left': 60, 'top': 100, 'right': 140, 'bottom': 60, 'hist_inner': 20, 'hist_outer': 40 }
      const valid_max = max(y_valid)
      const valid_min = min(y_valid)

      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const x_scale = getScale([valid_min, valid_max], [margin.left, width - margin.right])
      const y_scale = getScale([valid_min, valid_max], [height - margin.bottom, margin.top])

      // draw x axis
      const x_axis_define = d3.axisBottom(x_scale)
        .tickSizeInner(-(height - margin.top - margin.bottom))
        .tickSizeOuter(0)
        .ticks(5)
        .tickPadding(10)
      const x_axis = svg.append('g')
        .attr('transform', 'translate(' + 0 + ',' + (height - margin.bottom) + ')')
        .call(x_axis_define)
      styleAxis(x_axis)

      // draw y axis
      const y_axis_define = d3.axisLeft(y_scale)
        .tickSizeInner(-(width - margin.left - margin.right))
        .tickSizeOuter(0)
        .ticks(5)
        .tickPadding(10)
      const y_axis = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + 0 + ')')
        .call(y_axis_define)
      styleAxis(y_axis)

      // draw scatter plot
      const dataset = this.shapeDataset(y_valid, y_pred)
      svg.append('g')
        .selectAll('circle')
        .data(dataset)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x_scale(d[0]) })
        .attr('cy', function (d) { return y_scale(d[1]) })
        .attr('fill', valid_color)
        .attr('r', 3)

      // draw diagonal line
      svg.append('line')
        .attr('x1', x_scale(valid_min))
        .attr('x2', x_scale(valid_max))
        .attr('y1', y_scale(valid_min))
        .attr('y2', y_scale(valid_max))
        .attr('stroke-width', 1)
        .attr('stroke', 'gray')
        .attr('opacity', 0.3)

      // draw sd area dummy
      const dummy_array = [...Array(46).keys()].map(function (i) { return i + 5 })
      svg.append('path')
        .datum(dummy_array)
        .attr('fill', 'green')
        .attr('opacity', 0.05)
        .attr('d', d3.area()
          .x(function (d) { return x_scale(d) })
          .y1(function (d) { return y_scale(max([valid_min, d - 5])) })
          .y0(function (d) { return y_scale(min([valid_max, d + 5])) })
          .curve(d3.curveCardinal)
        )

      // draw histogram true
      const true_histogram = this.getHistgram(x_scale, 10)
      const true_valid_bins = true_histogram(y_valid)
      const true_hist_max = this.getHistgramSizeMax(true_valid_bins)
      const histy_scale = getScale([valid_max, valid_max + true_hist_max], [margin.top - margin.hist_inner, margin.hist_outer])

      svg.append('path')
        .datum(true_valid_bins)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return histy_scale(valid_max + d.length) })
          .y0(function (d) { return histy_scale(valid_max) })
          .curve(d3.curveCardinal)
        )

      // draw histogram prediction
      const pred_histogram = this.getHistgram(y_scale, 10)
      const pred_valid_bins = pred_histogram(y_pred)
      const pred_hist_max = this.getHistgramSizeMax(pred_valid_bins)
      const histx_scale = getScale([valid_max, valid_max + pred_hist_max], [width - margin.right + margin.hist_inner, width - margin.hist_outer])

      svg.append('path')
        .datum(pred_valid_bins)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x1(function (d) { return histx_scale(valid_max + d.length) })
          .x0(function (d) { return histx_scale(valid_max) })
          .y(function (d, index) { return y_scale((d.x0 + d.x1) / 2) })
          .curve(d3.curveCardinal)
        )
    },
    drawDeployed: function () {
      if (this.$store.state.deployed_model_y_pred.length === 0) return
      const id = '#deployed-plot'
      removeSvg(id)
      const y_valid = this.$store.state.deployed_model_y_valid
      const y_pred = this.$store.state.deployed_model_y_pred
      this.drawTruePredPlot(id, y_valid, y_pred)
    },
    drawSelected: function () {
      if (!this.$store.state.selected_model) return
      const id = '#selected-plot'
      removeSvg(id)
      const y_valid = this.$store.state.selected_y_valid
      const y_pred = this.$store.state.selected_y_pred
      this.drawTruePredPlot(id, y_valid, y_pred)
    },
    getHistgram: function (scale, ticks) {
      return d3.histogram()
        .value(function (d) { return d })
        .domain(scale.domain())
        .thresholds(scale.ticks(ticks))
    },
    getHistgramSizeMax: function (hist) {
      return max(hist.map(function (d) { return d.length }))
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
        font-size: $fs-small;
        color: $light-gray;
      }
      .x-axis-name {
        bottom: 24px;
        left: 50%;
        @include prefix("transform", "translateX(-50%)");
      }
      .y-axis-name {
        top: 56px;
        left: 16px;
      }
    }
  }
}
</style>
