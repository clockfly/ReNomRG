<template>
  <div id="prediction-result">
    <div class="panel">
      <div class="panel-title">
        Prediction Sample
      </div>

      <div class="panel-content prediction-result-content flex">
        <div class="column">
          <div class="label-value flex">
            <div class="model-type">Deploy Model</div>
            <div class="label">Model ID</div>
            <div class="value" v-if="deployedModel">{{deployedModel.model_id}}</div>
          </div>
          <div v-if="deployedModel">
            <div v-for="(d, index) in deployedModel.valid_true">
              <div class="label-value flex">
                <div class="label">Target</div>
                <div class="value">{{selectedDataset.labels[selectedDataset.target_column_ids[index]]}}</div>
              </div>
              <div :id="'deployed-plot'+index" class="plot-area">
                <div class="x-axis-name">True</div>
                <div class="y-axis-name">Prediction</div>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="label-value flex">
            <div class="model-type">Select Model</div>
            <div class="label">Model ID</div>
            <div class="value" v-if="selectedModel">{{selectedModel.model_id}}</div>
          </div>
          <div v-if="selectedModel">
            <div v-for="(d, index) in selectedModel.valid_true">
              <div class="label-value flex">
                <div class="label">Target</div>
                <div class="value">{{selectedDataset.labels[selectedDataset.target_column_ids[index]]}}</div>
              </div>
              <div :id="'selected-plot'+index" class="plot-area">
                <div class="x-axis-name">True</div>
                <div class="y-axis-name">Prediction</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import { mapState, mapGetters } from 'vuex'
import { train_color, valid_color } from '@/const'
import { max, min, getScale, removeSvg, styleAxis } from '@/utils'

export default {
  name: 'PreictionResult',
  computed: {
    ...mapState(['dataset_list']),
    ...mapGetters(['deployedModel', 'selectedModel', 'selectedDataset'])
  },
  watch: {
    selectedModel: function () {
      // wait dom rendering
      this.$nextTick(function () {
        this.drawSelected()
      })
    },
    deployedModel: function () {
      this.$nextTick(function () {
        this.drawDeployed()
      })
    }
  },
  mounted: function () {
    this.drawSelected()
    this.drawDeployed()
  },
  methods: {
    drawTruePredPlot: function (id, train_true, train_pred, valid_true, valid_pred, confidence_data) {
      if (!train_true || !train_pred || !valid_true || !valid_pred) return
      // define svg element
      const width = 400
      const height = 420
      const margin = { 'left': 60, 'top': 80, 'right': 80, 'bottom': 60, 'hist_inner': 20, 'hist_outer': 20 }
      const plot_max = max([max(train_true), max(valid_true)])
      const plot_min = min([min(train_true), min(valid_true)])
      const y_max = max([plot_max, max(train_pred), max(valid_pred)])
      const y_min = min([plot_min, min(train_pred), min(valid_pred)])
      const chunk = (plot_max - plot_min) / 10
      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const x_scale = getScale([plot_min, plot_max], [margin.left, width - margin.right])
      const y_scale = getScale([y_min, y_max], [height - margin.bottom, margin.top])

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

      // draw train scatter plot
      const train_dataset = this.shapeDataset(train_true, train_pred)
      svg.append('g')
        .selectAll('circle')
        .data(train_dataset)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x_scale(d[0]) })
        .attr('cy', function (d) { return y_scale(d[1]) })
        .attr('fill', train_color)
        .attr('r', 3)
      // draw valid scatter plot
      const valid_dataset = this.shapeDataset(valid_true, valid_pred)
      svg.append('g')
        .selectAll('circle')
        .data(valid_dataset)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x_scale(d[0]) })
        .attr('cy', function (d) { return y_scale(d[1]) })
        .attr('fill', valid_color)
        .attr('r', 3)

      // draw diagonal line
      svg.append('line')
        .attr('x1', x_scale(plot_min))
        .attr('x2', x_scale(plot_max))
        .attr('y1', y_scale(plot_min))
        .attr('y2', y_scale(plot_max))
        .attr('stroke-width', 1)
        .attr('stroke', 'gray')
        .attr('opacity', 0.3)

      // draw sd area
      svg.append('path')
        .datum(confidence_data)
        .attr('fill', train_color)
        .attr('opacity', 0.1)
        .attr('d', d3.area()
          .x(function (d, index) {
            if (index === 0) return x_scale(plot_min)
            if (index === confidence_data.length - 1) return x_scale(plot_max)
            return x_scale(plot_min + (chunk * (index - 1)) + (chunk * 0.5))
          })
          .y1(function (d, index) { return y_scale(min([plot_max, d[4]])) })
          .y0(function (d, index) { return y_scale(max([plot_min, d[0]])) })
          .curve(d3.curveCardinal)
        )
      svg.append('path')
        .datum(confidence_data)
        .attr('fill', train_color)
        .attr('opacity', 0.3)
        .attr('d', d3.area()
          .x(function (d, index) {
            if (index === 0) return x_scale(plot_min)
            if (index === confidence_data.length - 1) return x_scale(plot_max)
            return x_scale(plot_min + (chunk * (index - 1)) + (chunk * 0.5))
          })
          .y1(function (d, index) { return y_scale(min([plot_max, d[3]])) })
          .y0(function (d, index) { return y_scale(max([plot_min, d[1]])) })
          .curve(d3.curveCardinal)
        )

      // draw histogram train true
      const true_histogram = this.getHistgram(x_scale, 10)
      const train_true_bins = true_histogram(train_true)
      const true_hist_max = this.getHistgramSizeMax(train_true_bins)
      const histy_scale = getScale([plot_max, plot_max + true_hist_max], [margin.top - margin.hist_inner, margin.hist_outer])

      svg.append('path')
        .datum(train_true_bins)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return histy_scale(plot_max + d.length) })
          .y0(function (d) { return histy_scale(plot_max) })
          .curve(d3.curveCardinal)
        )

      // draw histogram valid true
      const valid_true_bins = true_histogram(valid_true)
      svg.append('path')
        .datum(valid_true_bins)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return histy_scale(plot_max + d.length) })
          .y0(function (d) { return histy_scale(plot_max) })
          .curve(d3.curveCardinal)
        )

      // draw histogram train prediction
      const pred_histogram = this.getHistgram(y_scale, 10)
      const train_pred_bins = pred_histogram(train_pred)
      const pred_hist_max = this.getHistgramSizeMax(train_pred_bins)
      const histx_scale = getScale([y_max, y_max + pred_hist_max], [width - margin.right + margin.hist_inner, width - margin.hist_outer])
      svg.append('path')
        .datum(train_pred_bins)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x1(function (d) { return histx_scale(y_max + d.length) })
          .x0(function (d) { return histx_scale(y_max) })
          .y(function (d, index) { return y_scale((d.x0 + d.x1) / 2) })
          .curve(d3.curveCardinal)
        )

      // draw histogram valid prediction
      const valid_pred_bins = pred_histogram(valid_pred)
      svg.append('path')
        .datum(valid_pred_bins)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x1(function (d) { return histx_scale(plot_max + d.length) })
          .x0(function (d) { return histx_scale(plot_max) })
          .y(function (d, index) { return y_scale((d.x0 + d.x1) / 2) })
          .curve(d3.curveCardinal)
        )
    },
    drawDeployed: function () {
      if (!this.deployedModel) return
      for (let i in this.deployedModel.valid_true) {
        const id = '#deployed-plot' + i
        removeSvg(id)
        const train_true = this.deployedModel.sampled_train_true[i]
        const train_pred = this.deployedModel.sampled_train_pred[i]
        const valid_true = this.deployedModel.valid_true[i]
        const valid_pred = this.deployedModel.valid_predicted[i]
        const confidence_data = this.deployedModel.confidence_data[i]
        this.drawTruePredPlot(id, train_true, train_pred, valid_true, valid_pred, confidence_data)
      }
    },
    drawSelected: function () {
      if (!this.selectedModel) return
      for (let i in this.selectedModel.valid_true) {
        const id = '#selected-plot' + i
        removeSvg(id)
        const train_true = this.selectedModel.sampled_train_true[i]
        const train_pred = this.selectedModel.sampled_train_pred[i]
        const valid_true = this.selectedModel.valid_true[i]
        const valid_pred = this.selectedModel.valid_predicted[i]
        const confidence_data = this.selectedModel.confidence_data[i]
        this.drawTruePredPlot(id, train_true, train_pred, valid_true, valid_pred, confidence_data)
      }
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
  $model-id-height: 32px;

  width: 100%;
  min-height: $prediction-sample-height;

  .prediction-result-content {
    width: 100%;
    min-height: calc(#{$prediction-sample-height} - #{$panel-title-height} - 8px);
    padding-top: $padding-large;
  }
  .target-label, .model-type, .label, .value {
    height: $text-height-small;
    line-height: $text-height-small;
    font-size: $fs-small;
  }
  .target-label, .model-type, .label {
    color: $gray;
  }
  .target-label {
    height: $model-id-height;
    line-height: $model-id-height;
  }
  .label-value {
    height: $text-height-regular;
    line-height: $text-height-regular;
    .model-type {
      margin-right: $margin-middle;
    }
    .label {
      margin-right: $margin-small;
    }
  }
  .column {
    width: 50%;
    padding: 0 $padding-large;
    .plot-area {
      position: relative;
      padding: 0 $padding-large;
    }
    .x-axis-name, .y-axis-name {
      position: absolute;
      font-size: $fs-small;
      color: $light-gray;
    }
    .x-axis-name {
      bottom: 48px;
      right: 48px;
    }
    .y-axis-name {
      top: 48px;
      left: 16px;
    }
  }
}
</style>
