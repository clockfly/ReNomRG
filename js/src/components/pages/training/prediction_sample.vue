/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="prediction-result">
    <div class="panel">
      <div class="panel-title">
        Prediction Sample
      </div>

      <div class="panel-content prediction-result-content flex">
        <div class="column">
          <div class="label-value flex">
            <div class="model-type">
              Deploy Model
            </div>
            <div class="label">
              Model ID：
            </div>
            <div
              v-if="deployedModel"
              class="value"
            >
              {{ deployedModel.model_id }}
            </div>
          </div>
          <div class="label-value flex">
            <div class="label">
              Feature Scaling：
            </div>
            <div
              v-if="deployedModel && deployedDataset"
              class="value"
            >
              {{ $store.state.scalings[deployedDataset.selected_scaling] }}
            </div>
          </div>
          <div v-if="deployedModel && deployedDataset">
            <div
              v-for="(d, index) in deployedModel.valid_true"
              :key="index"
            >
              <div class="label-value flex">
                <div class="label">
                  Target：
                </div>
                <div class="value">
                  {{ deployedDataset.labels[deployedDataset.target_column_ids[index]] }}
                </div>
              </div>
              <div
                :id="'deployed-plot'+index"
                class="plot-area"
              >
                <div class="x-axis-name">
                  True
                </div>
                <div class="y-axis-name">
                  Prediction
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="column">
          <div class="label-value flex">
            <div class="model-type">
              Select Model
            </div>
            <div class="label">
              Model ID：
            </div>
            <div
              v-if="selectedModel"
              class="value"
            >
              {{ selectedModel.model_id }}
            </div>
          </div>
          <div class="label-value flex">
            <div class="label">
              Feature Scaling：
            </div>
            <div
              v-if="selectedModel && selectedDataset"
              class="value"
            >
              {{ $store.state.scalings[selectedDataset.selected_scaling] }}
            </div>
          </div>
          <div v-if="selectedModel && selectedDataset">
            <div
              v-for="(d, index) in selectedModel.valid_true"
              :key="index"
            >
              <div class="label-value flex">
                <div class="label">
                  Target：
                </div>
                <div class="value">
                  {{ selectedDataset.labels[selectedDataset.target_column_ids[index]] }}
                </div>
              </div>
              <div
                :id="'selected-plot'+index"
                class="plot-area"
              >
                <div class="x-axis-name">
                  True
                </div>
                <div class="y-axis-name">
                  Prediction
                </div>
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
  data: function () {
    return {
      'draw_width': 420
    }
  },
  computed: {
    ...mapState(['dataset_list']),
    ...mapGetters(['deployedModel', 'deployedDataset', 'selectedModel', 'selectedDataset'])
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
  created: function() {
    this.setInnerWidth()
    window.addEventListener('resize', this.setInnerWidth, false)
  },
  mounted: function () {
    this.drawSelected()
    this.drawDeployed()
  },
  beforeDestroy: function () {
    window.removeEventListener('resize', this.setInnerWidth, false)
  },
  methods: {
    setInnerWidth: function() {
      if (window.innerWidth / 3.2 < 420) {
        this.draw_width = window.innerWidth / 3.2
      } else {
        this.draw_width = 420
      }
      this.drawDeployed()
      this.drawSelected()
    },
    drawTruePredPlot: function (id, train_true, train_pred, valid_true, valid_pred, confidence_data, true_histogram, pred_histogram) {
      if (!train_true || !train_pred || !valid_true || !valid_pred) return
      // define svg element
      const width = this.draw_width
      const height = width
      const bins_end = 10
      const margin = { 'left': 60, 'top': 80, 'right': 80, 'bottom': 60, 'hist_inner': 20, 'hist_outer': 20 }
      const plot_max = max([true_histogram.train.bins[bins_end], true_histogram.valid.bins[bins_end]])
      const plot_min = min([true_histogram.train.bins[0], true_histogram.valid.bins[0]])
      const y_max = max([plot_max, pred_histogram.train.bins[bins_end], pred_histogram.valid.bins[bins_end]])
      const y_min = min([plot_min, pred_histogram.train.bins[0], pred_histogram.valid.bins[0]])
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
          .y1(function (d, index) {
            let y_1 = d[4]
            let sd = d[4] - d[0]
            let gh = y_max - y_min
            // データが存在し(データが1つでもあれば0にならない処理を「train_task.py」ファイル内で追加している)、
            // かつ、標準偏差が極端に低い場合はグラフが線のようになってしまうため、
            // y_1の値に少し幅をもたせる(y_0も同様)
            if (0 != sd && sd < gh / 25) y_1 = y_1 + gh / 50
            if (y_1 < y_min) y_1 = y_min
            return y_scale(min([y_max, y_1]))
          })
          .y0(function (d, index) {
            let y_0 = d[0]
            let sd = d[4] - d[0]
            let gh = y_max - y_min
            if (0 != sd && sd < gh / 25) y_0 = y_0 - gh / 50
            if (y_0 > y_max) y_0 = y_max
            return y_scale(max([y_min, y_0]))
          })
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
          .y1(function (d, index) {
            let y_1 = d[3]
            let sd = d[3] - d[1]
            let gh = y_max - y_min
            // データが存在し(データが1つでもあれば0にならない処理を「train_task.py」ファイル内で追加している)、
            // かつ、標準偏差が極端に低い場合はグラフが線のようになってしまうため、
            // y_1の値に少し幅をもたせる(y_0も同様)
            if (0 != sd && sd < gh / 50) y_1 = y_1 + gh / 100
            if (y_1 < y_min) y_1 = y_min
            return y_scale(min([y_max, y_1]))
          })
          .y0(function (d, index) {
            let y_0 = d[1]
            let sd = d[3] - d[1]
            let gh = y_max - y_min
            if (0 != sd && sd < gh / 50) y_0 = y_0 - gh / 100
            if (y_0 > y_max) y_0 = y_max
            return y_scale(max([y_min, y_0]))
          })
          .curve(d3.curveCardinal)
        )

      // draw histogram train true
      const true_hist_max = max(true_histogram.train.counts)
      const histy_scale = getScale([plot_max, plot_max + true_hist_max], [margin.top - margin.hist_inner, margin.hist_outer])
      // const train_true_hist
      svg.append('path')
        .datum(true_histogram.train.counts)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) {
            if (index == 0) {
              return x_scale(true_histogram.train.bins[index])
            } else if (index == bins_end - 1) {
              return x_scale(true_histogram.train.bins[bins_end])
            } else {
              return x_scale((true_histogram.train.bins[index] + true_histogram.train.bins[index + 1]) / 2)
            }
          })
          .y1(function (d) { return histy_scale(plot_max + d) })
          .y0(function (d) { return histy_scale(plot_max) })
          .curve(d3.curveCardinal)
        )

      // draw histogram valid true
      svg.append('path')
        .datum(true_histogram.valid.counts)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) {
            if (index == 0) {
              return x_scale(true_histogram.valid.bins[index])
            } else if (index == bins_end - 1) {
              return x_scale(true_histogram.valid.bins[bins_end])
            } else {
              return x_scale((true_histogram.valid.bins[index] + true_histogram.valid.bins[index + 1]) / 2)
            }
          })
          .y1(function (d) { return histy_scale(plot_max + d) })
          .y0(function (d) { return histy_scale(plot_max) })
          .curve(d3.curveCardinal)
        )

      // draw histogram train prediction
      const pred_hist_max = max(pred_histogram.train.counts)
      const histx_scale = getScale([y_max, y_max + pred_hist_max], [width - margin.right + margin.hist_inner, width - margin.hist_outer])
      svg.append('path')
        .datum(pred_histogram.train.counts)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x1(function (d) { return histx_scale(y_max + d) })
          .x0(function (d) { return histx_scale(y_max) })
          .y(function (d, index) {
            if (index == 0) {
              return y_scale(pred_histogram.train.bins[index])
            } else if (index == bins_end - 1) {
              return y_scale(pred_histogram.train.bins[bins_end])
            } else {
              return y_scale((pred_histogram.train.bins[index] + pred_histogram.train.bins[index + 1]) / 2)
            }
          })
          .curve(d3.curveCardinal)
        )

      // draw histogram valid prediction
      svg.append('path')
        .datum(pred_histogram.valid.counts)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x1(function (d) { return histx_scale(y_max + d) })
          .x0(function (d) { return histx_scale(y_max) })
          .y(function (d, index) {
            if (index == 0) {
              return y_scale(pred_histogram.valid.bins[index])
            } else if (index == bins_end - 1) {
              return y_scale(pred_histogram.valid.bins[bins_end])
            } else {
              return y_scale((pred_histogram.valid.bins[index] + pred_histogram.valid.bins[index + 1]) / 2)
            }
          })
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
        const true_histogram = this.deployedModel.true_histogram[i]
        const pred_histogram = this.deployedModel.pred_histogram[i]
        this.drawTruePredPlot(id, train_true, train_pred, valid_true, valid_pred, confidence_data, true_histogram, pred_histogram)
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
        const true_histogram = this.selectedModel.true_histogram[i]
        const pred_histogram = this.selectedModel.pred_histogram[i]
        this.drawTruePredPlot(id, train_true, train_pred, valid_true, valid_pred, confidence_data, true_histogram, pred_histogram)
      }
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
      right: calc(100vw / 65);
    }
    .y-axis-name {
      top: 48px;
      left: 16px;
    }
  }
}
</style>
