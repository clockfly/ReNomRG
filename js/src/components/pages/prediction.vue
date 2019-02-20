<template>
  <div
    id="page"
    class="flex"
  >
    <div class="model-detail-area">
      <div class="start-button-area">
        <button
          class="start-button"
          @click="runPrediction"
        >
          > Prediction Start
        </button>
      </div>

      <div class="panel model-detail-panel">
        <div class="panel-title">
          Model Detail
        </div>

        <div class="panel-content model-detail-content">
          <div v-if="deployedModel">
            <div class="label-value flex">
              <div class="label">
                Selected Model ID
              </div>
              <div class="value">
                {{ deployedModel.model_id }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Dataset
              </div>
              <div class="value">
                {{ deployedDataset.name }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Feature Scaling
              </div>
              <div class="value">
                {{ $store.state.scalings[deployedDataset.selected_scaling] }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Algorithm
              </div>
              <div class="value">
                {{ algorithms[deployedModel.algorithm] }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Total Epoch
              </div>
              <div class="value">
                {{ deployedModel.epoch }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Batch Size
              </div>
              <div class="value">
                {{ deployedModel.batch_size }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Validation Loss
              </div>
              <div class="value">
                {{ round(deployedModel.best_epoch_valid_loss) }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                RMSE
              </div>
              <div class="value">
                {{ round(deployedModel.best_epoch_rmse) }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Max Absolute Error
              </div>
              <div class="value">
                {{ round(deployedModel.best_epoch_max_abs_error) }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                R2 Score
              </div>
              <div class="value">
                {{ round(deployedModel.best_epoch_r2) }}
              </div>
            </div>

            <div class="label-value">
              <div class="label">
                Graph Comvolution Params
              </div>
            </div>

            <div class="label-value flex">
              <div class="label">
                Number of Neighbors
              </div>
              <div class="value">
                {{ deployedModel.algorithm_params.num_neighbors }}
              </div>
            </div>

            <br>
            <div v-if="this.$store.state.pred_x">
              <button @click="exportCSV">
                CSV DL
              </button>
            </div>
          </div>
          <div v-if="!deployedModel">
            Model is not Deployed.
          </div>
        </div>
      </div>
    </div> <!-- model detail -->

    <div class="prediction-results-area">
      <div class="panel">
        <div class="panel-title">
          Prediction Results
        </div>

        <div class="panel-content plot-area">
          <div
            v-if="deployedDataset"
            class="prediction-plot-area flex"
          >
            <div
              id="pred-y-hist"
              class="column"
            >
              <div class="plot-name">
                Predicted Y Histogram
              </div>
            </div>
            <div
              id="xy-plot"
              class="column"
            >
              <div class="plot-name">
                XY Plot
              </div>

              <div class="axis-y flex">
                <div class="axis-label">
                  Y
                </div>
                <div class="axis-selector">
                  <select
                    v-model="plot_y_index"
                    class="small"
                  >
                    <option
                      v-for="(l, i) in deployedDataset.target_column_ids"
                      :key="`y_${i}`"
                      :value="i"
                    >
                      {{ deployedDataset.labels[l] }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="axis-x flex">
                <div class="axis-label">
                  X
                </div>
                <div class="axis-selector">
                  <select
                    v-model="plot_x_index"
                    class="small"
                  >
                    <option
                      v-for="(l, i) in deployedDataset.explanatory_column_ids"
                      :key="`X_${i}`"
                      :value="i"
                    >
                      {{ deployedDataset.labels[l] }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div
            v-if="deployedDataset"
            class="prediction-table-area flex"
          >
            <table>
              <thead>
                <tr>
                  <th
                    v-for="(l, i) in deployedDataset.target_column_ids"
                    :key="`y_${i}`"
                    :style="'position: sticky;top: 0px;left: ' + i * sticky_width + 'px;z-index: 4;'"
                    :class="{ active: l === sort_index }"
                    @click="sortPredY(i)"
                  >
                    {{ deployedDataset.labels[l] | truncate(truncate_l, '…') }}
                    <span
                      v-if="desc"
                      class="icon"
                      :class="{ active: l === sort_index }"
                    >
                      ▼
                    </span>
                    <span
                      v-else
                      class="icon"
                      :class="{ active: l === sort_index }"
                    >
                      ▲
                    </span>
                  </th>

                  <th
                    v-for="(l, i) in deployedDataset.explanatory_column_ids"
                    :key="`X_${i}`"
                    :class="{ active: i === sort_index }"
                    @click="sortPredX(i)"
                  >
                    {{ deployedDataset.labels[l] | truncate(truncate_l, '…') }}
                    <span
                      v-if="desc"
                      class="icon"
                      :class="{ active: i === sort_index }"
                    >
                      ▼
                    </span>
                    <span
                      v-else
                      class="icon"
                      :class="{ active: i === sort_index }"
                    >
                      ▲
                    </span>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(data, i) in pred_y"
                  :key="i"
                >
                  <td
                    v-for="(d, j) in data"
                    :key="`y_${j}`"
                    :style="'position: sticky;left: ' + j * sticky_width + 'px;z-index: 3;'"
                  >
                    {{ round(d) }}
                  </td>
                  <td
                    v-for="(d, j) in pred_x[i]"
                    :key="`X_${j}`"
                  >
                    {{ round(d) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div> <!-- prediction results -->
  </div>
</template>

<script>
import * as d3 from 'd3'
import { mapState, mapGetters } from 'vuex'
import { train_color } from '@/const'
import { round, max, min, getScale, removeSvg, styleAxis } from '@/utils'

const width = 320
const height = 160
const margin = { 'left': 50, 'top': 10, 'right': 50, 'bottom': 20 }

export default {
  name: 'PredictionPage',
  filters: {
    truncate: function(value, length, omission) {
      var length = length ? parseInt(length, 10) : 20;
      var ommision = omission ? omission.toString() : '...';
      if(value.length <= length) {
        return value;
      }
      else {
        return value.substring(0, length) + ommision;
      }
    }
  },
  data: function () {
    return {
      'plot_x_index': 0,
      'plot_y_index': 0,
      'desc': false,
      'sort_index': -1,
      'sticky_width': 120,
      'truncate_l': 8
    }
  },
  computed: {
    ...mapState(['algorithms', 'pred_x', 'pred_y', 'pred_csv']),
    ...mapGetters(['deployedModel', 'deployedDataset']),
    target_labels: function () {
      const target_column_ids = this.deployedDataset.target_column_ids

      let filtered = []
      if (this.deployedDataset && this.deployedDataset.labels) {
        filtered = this.deployedDataset.labels.filter(function (element, index, array) {
          return target_column_ids.indexOf(index) !== -1
        })
      }
      return filtered
    },
    explanatory_labels: function () {
      const target_column_ids = this.deployedDataset.target_column_ids

      let filtered = []
      if (this.deployedDataset && this.deployedDataset.labels) {
        filtered = this.deployedDataset.labels.filter(function (element, index, array) {
          return target_column_ids.indexOf(index) === -1
        })
      }
      return filtered
    }
  },
  watch: {
    plot_x_index: function () {
      this.drawXYPlot()
    },
    plot_y_index: function () {
      this.drawPredYHist()
      this.drawXYPlot()
    },
    pred_y: function () {
      this.drawPredYHist()
      this.drawXYPlot()
    }
  },
  created: function () {
    this.$store.commit('resetPred')
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadModels')
  },
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    runPrediction: function () {
      let explanatory_column = []
      let target_column = []
      for (let d of this.deployedDataset.explanatory_column_ids) {
        explanatory_column.push(this.deployedDataset.labels[d])
      }
      for (let d of this.deployedDataset.target_column_ids) {
        target_column.push(this.deployedDataset.labels[d])
      }

      this.$store.dispatch('runPrediction',
      {
        'model_id': this.deployedModel.model_id,
        'explanatory_column': explanatory_column,
        'target_column': target_column,
        'explanatory_column_ids': this.deployedDataset.explanatory_column_ids
      })
    },
    exportCSV: function () {
      this.$store.dispatch('exportCSV', {'pred_csv': this.pred_csv})
    },
    shapeX: function () {
      let data = []
      for (let d of this.pred_x) {
        data.push(d[this.plot_x_index])
      }
      return data
    },
    shapeY: function () {
      let data = []
      for (let d of this.pred_y) {
        data.push(d[this.plot_y_index])
      }
      return data
    },
    shapeDataset: function (x, y) {
      let dataset = []
      for (let i in y) {
        dataset.push([x[i], y[i]])
      }
      return dataset
    },
    drawHist: function (id, x) {
      removeSvg(id)
      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .style('position', 'absolute')
        .style('top', '50%')
        .style('left', '50%')
        .style('transform', 'translateY(-50%) translateX(-50%)')
      const x_scale = getScale([min(x), max(x)], [margin.left, width - margin.right])
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

      const hist = this.getHistgram(x_scale, 10)
      const bins = hist(x)
      const hist_max = this.getHistgramSizeMax(bins)
      const y_scale = getScale([0, hist_max], [height - margin.bottom, margin.top])

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

      // draw cardinal area chart
      svg.append('path')
        .datum(bins)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d) { return x_scale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return y_scale(d.length) })
          .y0(function (d) { return y_scale(0) })
          .curve(d3.curveCardinal)
        )
    },
    drawPlot: function (id, x, y) {
      removeSvg(id)
      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .style('position', 'absolute')
        .style('top', '50%')
        .style('left', '50%')
        .style('transform', 'translateY(-50%) translateX(-50%)')
      const x_scale = getScale([min(x), max(x)], [margin.left, width - margin.right])
      const y_scale = getScale([min(y), max(y)], [height - margin.bottom, margin.top])

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

      const dataset = this.shapeDataset(x, y)
      svg.append('g')
        .selectAll('circle')
        .data(dataset)
        .enter()
        .append('circle')
        .attr('cx', function (d) { return x_scale(d[0]) })
        .attr('cy', function (d) { return y_scale(d[1]) })
        .attr('fill', train_color)
        .attr('r', 3)
    },
    drawXYPlot: function () {
      if (!this.pred_y) return

      const id = '#xy-plot'
      const x = this.shapeX()
      const y = this.shapeY()

      this.drawPlot(id, x, y)
    },
    drawPredYHist: function () {
      if (!this.pred_y) return

      const id = '#pred-y-hist'
      const x = this.shapeY()

      this.drawHist(id, x)
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
    sortPredX: function (value) {
      if (value === this.sort_index) {
        this.desc = !this.desc
      } else {
        this.desc = false
      }
      this.sort_index = value
      this.$store.commit('sortPredX', {'key': value, 'desc': this.desc})
    },
    sortPredY: function (value) {
      if (this.deployedDataset.target_column_ids[value] === this.sort_index) {
        this.desc = !this.desc
      } else {
        this.desc = false
      }
      this.sort_index = this.deployedDataset.target_column_ids[value]
      this.$store.commit('sortPredY', {'key': value, 'desc': this.desc})
    }
  }
}
</script>

<style lang="scss" scoped>
#page {
  $table-width: 90%;
  $table-item-height: 32px;

  width: 100%;
  height: calc(100vh - #{$footer-height} - #{$header-height});

  .model-detail-area {
    width: 20%;
    height: 100%;

    .start-button-area {
      width: 100%;
      padding: $padding-small;
      .start-button {
        width: 100%;
      }
    }

    .model-detail-panel {
      height: calc(100% - #{$button-height} - #{$padding-small}*2);
      .model-detail-content {
        padding: $padding-large;

        .label-value {
          margin-bottom: $margin-small;
          .label, .value {
            font-size: $fs-small;
          }
          .label {
            margin-right: $margin-small;
            color: $gray;
          }
        }
      }
    }
  }

  .prediction-results-area {
    width: 80%;
    height: 100%;

    .plot-area {
      padding: $padding-middle;
    }

    .prediction-plot-area {
      padding: $padding-small;
    }
    .prediction-plot-area {
      width: 100%;
      height: 40%;
    }
    .prediction-table-area {
      overflow: scroll;
      width: 100%;
      height: 60%;
      .icon {
        font-size: $fs-micro;
        color: $gray;
      }
      .active {
        color: $blue;
      }
      th{
        width: $th-td-width;
        min-width: $th-td-width;
      }
      td{
        width: $th-td-width;
        min-width: $th-td-width;
      }
    }
    #xy-plot, #pred-y-hist {
      position: relative;
      width: 48%;
      height: 100%;
    }
    .axis-x, .axis-y {
      position: absolute;
      .axis-label {
        height: $text-height-micro;
        margin-right: $margin-small;
        line-height: $text-height-micro;
        font-size: $fs-small;
        color: $gray;
      }
      .axis-selector {
        margin-right: $margin-middle;
      }
    }
    .axis-x {
      right: 0;
      bottom: 20px;
    }
    .axis-y {
      top: 0;
      left: 20%;
    }
    .plot-name {
      height: $text-height-small;
      line-height: $text-height-small;
      font-size: $fs-small;
      color: $gray;
    }
  }
  .active {
    color: $blue;
  }
}
</style>
