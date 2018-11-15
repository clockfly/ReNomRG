<template>
  <div id="page">

    <div class="model-detail-area">
      <div class="start-button-area">
        <button class="start-button" @click="runPrediction">
          > Prediction Start
        </button>
      </div>

      <div class="panel model-detail-panel">
        <div class="panel-title">
          Model Detail
        </div>

        <div class="panel-content model-detail-content">
          <div v-if="deployedModel">
            <div class="label-value">
              <div class="label">Selected Model ID</div>
              <div class="value">{{deployedModel.model_id}}</div>
            </div>
            <div class="label-value">
              <div class="label">Dataset</div>
              <div class="value">{{deployedModel.dataset_id}}</div>
            </div>
            <div class="label-value">
              <div class="label">Algorithm</div>
              <div class="value">{{algorithms[deployedModel.algorithm]}}</div>
            </div>
            <div class="label-value">
              <div class="label">Total Epoch</div>
              <div class="value">{{deployedModel.epoch}}</div>
            </div>
            <div class="label-value">
              <div class="label">Batch Size</div>
              <div class="value">{{deployedModel.batch_size}}</div>
            </div>
            <div class="label-value">
              <div class="label">Validation Loss</div>
              <div class="value">{{round(deployedModel.best_epoch_valid_loss)}}</div>
            </div>
            <div class="label-value">
              <div class="label">RMSE</div>
              <div class="value">{{round(deployedModel.best_epoch_rmse)}}</div>
            </div>
            <div class="label-value">
              <div class="label">Max Absolute Error</div>
              <div class="value">{{round(deployedModel.best_epoch_max_abs_error)}}</div>
            </div>
            <div class="label-value">
              <div class="label">R2 Score</div>
              <div class="value">{{round(deployedModel.best_epoch_r2)}}</div>
            </div>

            <div class="label-value">
              <div class="label">Graph Comvolution Params</div>
            </div>

            <div class="label-value">
              <div class="label">Number of Neighbors</div>
              <div class="value">{{deployedModel.algorithm_params.num_neighbors}}</div>
            </div>
          </div>

          <div v-if="!deployedModel">Model is not Deployed.</div>
        </div>
      </div>
    </div> <!-- model detail -->

    <div class="prediction-results-area">
      <div class="panel">
        <div class="panel-title">
          Prediction Results
        </div>

        <div class="panel-content">
          <div class="prediction-plot-area" v-if="deployedDataset">

            <div id="sorted-y-plot" class="column">
              <div class="plot-name">Sorted Y Plot</div>
            </div>
            <div id="xy-plot" class="column">
              <div class="plot-name">XY Plot</div>
            </div>
          </div>

          <div class="prediction-table-area" v-if="deployedDataset">

            <div class="pred-y-area">
              <div class="table-header">
                <div class="table-row">
                  <div class="table-item"
                    v-if="deployedDataset.target_column_ids.indexOf(i) !== -1"
                    v-for="(l, i) in deployedDataset.labels"
                    @click="plot_y_index = i">
                    {{l}}
                  </div>
                </div>
              </div>

              <div class="table-content scrollable-y">
                <div class="table-row" v-for="(data, index) in pred_y" :key="index">
                  <div class="table-item"
                    v-for="(l, i) in Array(data.length)">
                    {{ round(data[i]) }}
                  </div>
                </div>
              </div>

            </div>

            <div class="pred-x-area">
              <div class="table-header">
                <div class="table-row">
                  <div class="table-item"
                    v-if="deployedDataset.target_column_ids.indexOf(i) === -1"
                    v-for="(l, i) in deployedDataset.labels"
                    @click="plot_x_index = i">
                    {{l}}
                  </div>
                </div>
              </div>

              <div class="table-content scrollable">
                <div class="table-row" v-for="(data, index) in pred_x" :key="index">
                  <div class="table-item"
                    v-for="(l, i) in Array(data.length)"
                    @click="plot_x_index = i">
                    {{round(data[i])}}
                  </div>
                </div>
              </div>
            </div>

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

const width = 240
const height = 160
const margin = { 'left': 20, 'top': 0, 'right': 0, 'bottom': 20 }

export default {
  name: 'PredictionPage',
  data: function () {
    return {
      'plot_x_index': 0,
      'plot_y_index': 0
    }
  },
  computed: {
    ...mapState(['algorithms', 'model_list', 'dataset_list', 'pred_x', 'pred_y']),
    ...mapGetters(['deployedModel', 'deployedDataset'])
  },
  watch: {
    plot_x_index: function () {
      this.drawSortedYPlot()
      this.drawXYPlot()
    },
    plot_y_index: function () {
      this.drawSortedYPlot()
      this.drawXYPlot()
    },
    pred_y: function () {
      this.drawSortedYPlot()
      this.drawXYPlot()
    }
  },
  created: function () {
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadModels')
  },
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    runPrediction: function () {
      this.$store.dispatch('runPrediction', { 'model_id': this.deployedModel.model_id })
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
    shapeSortedY: function () {
      let sorted_y = this.shapeY()
      return sorted_y.sort((a, b) => a - b)
    },
    shapeDataset: function (x, y) {
      let dataset = []
      for (let i in y) {
        dataset.push([x[i], y[i]])
      }
      return dataset
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
    drawSortedYPlot: function () {
      if (!this.pred_y) return

      const id = '#sorted-y-plot'
      const y = this.shapeSortedY()
      const x = [...Array(y.length).keys()]

      this.drawPlot(id, x, y)
    }
  }
}
</script>

<style lang="scss" scoped>
#page {
  $table-width: 90%;
  $table-item-height: 32px;

  @include prefix('display', 'flex');
  width: 100%;
  height: calc(100vh - #{$footer-height} - #{$header-height});

  .model-detail-area {
    width: 20%;
    height: 100%;

    .start-button-area {
      width: 100%;
      padding: 8px;
      .start-button {
        width: 100%;
      }
    }

    .model-detail-panel {
      height: calc(100% - #{$button-area-height});
      .model-detail-content {
        padding: 16px;

        .label-value {
          @include prefix('display', 'flex');
          margin-bottom: 8px;
          font-size: $fs-small;
          .label {
            margin-right: 8px;
            color: $gray;
          }
        }
      }
    }
  }

  .prediction-results-area {
    width: 80%;
    .prediction-plot-area, .prediction-table-area {
      @include prefix('display', 'flex');
      padding: 16px;
    }
    .prediction-plot-area {
      height: 40%;
    }
    #sorted-y-plot, #xy-plot {
      position: relative;
      width: 50%;
      height: 100%;
    }
    .plot-name {
      color: $gray;
    }
    .prediction-table-area {
      overflow: scroll;
      height: 60%;
      width: 100%;
      .pred-y-area {
        height: 100%;
        border-right: 1px solid $light-gray;
      }
      .table-content {
        width: 100%;
        height: calc(100% - #{$table-item-height});
      }
      .table-row {
        @include prefix('display', 'flex');
        border-bottom: 1px solid $light-gray;
      }
      .table-item {
        width: 100px;
        height: $table-item-height;
        line-height: $table-item-height;
        text-align: center;
        font-size: $fs-small;
        color: $gray;
      }
      .pred-x-area, .pred-y-area {
        .table-row {
          .table-header {
            .table-item:hover {
              color: $light-gray;
            }
          }
        }
      }
    }
  }
}
</style>
