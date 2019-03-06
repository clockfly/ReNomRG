/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="page">
    <div class="page-content">
      <div class="panel">
        <div class="panel-title panel-title-button-area">
          Dataset List
          <div
            class="panel-title-button"
            @click="show_modal = true"
          >
            > Setting of Dataset
          </div>
        </div>

        <div class="panel-content dataset-list-and-detail flex">
          <div class="column-left">
            <div class="table-header padding-for-scroll-bar">
              <div class="table-row flex">
                <div class="table-item">
                  Name
                </div>
                <div class="table-item">
                  Train Ratio
                </div>
                <div class="table-item">
                  Train
                </div>
                <div class="table-item">
                  Validation
                </div>
              </div>
            </div>
            <div class="table-content">
              <div
                v-for="(dataset, index) in $store.state.dataset_list"
                :key="index"
                class="table-row flex"
                @click="selected_dataset_index = index"
              >
                <div
                  class="table-item"
                  :class="{ 'active': selected_dataset_index === index }"
                >
                  {{ dataset.name }}
                </div>
                <div
                  class="table-item"
                  :class="{ 'active': selected_dataset_index === index }"
                >
                  {{ dataset.train_ratio * 100 }}%
                </div>
                <div
                  class="table-item"
                  :class="{ 'active': selected_dataset_index === index }"
                >
                  {{ dataset.train_index.length }}
                </div>
                <div
                  class="table-item"
                  :class="{ 'active': selected_dataset_index === index }"
                >
                  {{ dataset.valid_index.length }}
                </div>
              </div>
            </div>
          </div> <!-- content-left dataset list -->

          <div
            v-if="selectedDataset"
            class="column-right"
          >
            <div class="dataset-name">
              {{ selectedDataset.name }}
            </div>
            <div class="dataset-detail flex">
              <div class="column">
                <div class="selected-scaling-area">
                  <div class="label">
                    Feature Scaling : {{ $store.state.scalings[selectedDataset.selected_scaling] }}
                  </div>
                </div> <!-- selected scaling area -->
                <div class="dataset-description-area">
                  <div class="label">
                    Description :
                  </div>
                  <textarea
                    class="description-text"
                    :placeholder="selectedDataset.description"
                    disabled
                  />
                </div> <!-- dataset description area -->
                <div class="train-ratio-area">
                  <div class="train-ratio-block flex">
                    <div class="label">
                      Number of data size :
                    </div>
                    <div class="values flex">
                      <div class="train-number">
                        Train {{ selectedDataset.train_index.length }}
                      </div>
                      <div class="valid-number">
                        Validation {{ selectedDataset.valid_index.length }}
                      </div>
                    </div>
                  </div>

                  <div class="train-ratio-block flex">
                    <div class="all-size">
                      All {{ selectedDataset.train_index.length+selectedDataset.valid_index.length }}
                    </div>
                    <div class="values flex">
                      <div class="train-ratio-bar flex">
                        <div
                          class="bar-item train"
                          :style="{ 'flex-grow': selectedDataset.train_index.length }"
                        />
                        <div
                          class="bar-item validation"
                          :style="{ 'flex-grow': selectedDataset.valid_index.length }"
                        />
                      </div>
                    </div>
                  </div>
                  <br>
                  <div class="selected-explanatory-area">
                    <div class="label">
                      Explanatory Valiables :
                    </div>
                    <div
                      v-for="(data, index) in selectedDataset.explanatory_column_ids"
                      :key="index"
                      class="explanatory-name"
                    >
                      {{ selectedDataset.labels[data] }}
                    </div>
                  </div> <!-- selected explanatory area -->
                </div> <!-- dataset train valid ratio area -->
              </div> <!-- dataset detail column -->

              <div class="column">
                <div class="label">
                  Histogram of Target Valiables :
                </div>
                <div class="histogram-area flex">
                  <div
                    v-for="(data, index) in selectedDataset.true_histogram"
                    :id="'train-test-histogram'+index"
                    :key="index"
                    class="histogram-plot"
                  >
                    <div class="target-name">
                      {{ selectedDataset.labels[selectedDataset.target_column_ids[index]] }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div> <!-- content-right dataset detail -->
        </div>
      </div>
    </div>

    <ModalDataset
      v-if="show_modal"
      @hide="show_modal = false"
    />
  </div>
</template>

<script>
// import { mapState } from 'vuex'
import * as d3 from 'd3'
import { train_color, valid_color } from '@/const'
import { max, min, getScale, removeSvg, styleAxis } from '@/utils'
import ModalDataset from '@/components/common/modal_dataset'

export default {
  name: 'DatasetPage',
  components: {
    ModalDataset
  },
  data: function () {
    return {
      'show_modal': false,
      'selected_dataset_index': 0
    }
  },
  computed: {
    selectedDataset: function () {
      return this.$store.state.dataset_list[this.selected_dataset_index]
    }
  },
  watch: {
    selectedDataset: function () {
      this.$nextTick(function () {
        this.drawHistograms()
      })
    }
  },
  created: function () {
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadLabels')
  },
  mounted: function () {
    this.drawHistograms()
  },
  methods: {
    drawHistograms: function () {
      if (!this.selectedDataset) return
      for (let i in this.selectedDataset.true_histogram) {
        const id = '#train-test-histogram' + i
        const hist = this.selectedDataset.true_histogram[i]
        removeSvg(id)
        this.drawHistogram(id, hist.train, hist.valid)
      }
    },
    drawHistogram: function (id, train_hist, valid_hist) {
      const width = 150
      const height = 150
      const margin = { 'left': 20, 'top': 20, 'right': 20, 'bottom': 20 }

      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const x_scale = getScale([min(train_hist.bins), max(train_hist.bins)], [margin.left, width - margin.right])
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

      // calc histogram
      const hist_max = max(train_hist.counts)
      const y_scale = getScale([0, hist_max], [height - margin.bottom, margin.top])

      // draw y axis
      // const y_axis_define = d3.axisLeft(y_scale)
      //   .tickSizeInner(-(width - margin.left - margin.right))
      //   .tickSizeOuter(0)
      //   .ticks(5)
      //   .tickPadding(10)
      // const y_axis = svg.append('g')
      //   .attr('transform', 'translate(' + margin.left + ',' + 0 + ')')
      //   .call(y_axis_define)
      // styleAxis(y_axis)

      // draw cardinal area chart
      svg.append('path')
        .datum(train_hist.counts)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((train_hist.bins[index] + train_hist.bins[index + 1]) / 2) })
          .y1(function (d) { return y_scale(d) })
          .y0(function (d) { return y_scale(0) })
          .curve(d3.curveCardinal)
        )

      svg.append('path')
        .datum(valid_hist.counts)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((valid_hist.bins[index] + valid_hist.bins[index + 1]) / 2) })
          .y1(function (d) { return y_scale(d) })
          .y0(function (d) { return y_scale(0) })
          .curve(d3.curveCardinal)
        )
    }
  }
}
</script>

<style lang="scss" scoped>
#page {
  $table-width: 90%;

  width: 100%;
  height: calc(100vh - #{$footer-height} - #{$header-height});

  .page-content {
    width: 100%;
    height: 100%;
  }

  .dataset-list-and-detail {
    padding: $padding-large;
  }
  .column-left {
    width: 30%;
    height: 100%;
    padding-right: $padding-large;
    border-right: $border-width-regular solid $light-gray;

    .table-content {
      width: 100%;
      height: calc(100% - #{$text-height-regular});
      overflow-y: scroll;
    }
    .table-row {
      width: $table-width;
      margin: 0 auto;
      border-bottom: $border-width-regular solid $light-gray;
      cursor:pointer;
    }
    .table-row:hover .table-item {
      color: $light-gray;
    }
    .table-item {
      width: 25%;
      height: $text-height-regular;
      line-height: $text-height-regular;
      text-align: center;
      font-size: $fs-small;
      color: $gray;
    }
    .active {
      color: $blue;
    }
  }

  .column-right {
    width: 70%;
    height: 100%;
    padding: 0 $padding-large;

    .dataset-name {
      height: $text-height-regular;
      line-height: $text-height-regular;
      font-size: $fs-regular;
      color: $blue;
    }
    .dataset-detail {
      width: 100%;
      height: calc(100% - #{$text-height-regular});
      .column {
        width: 50%;
        height: 100%;
        padding: $padding-middle;
      }
      .train-ratio-area {
        margin-top: $margin-large;
      }
      .label, .train-number, .valid-number, .target-name, .all-size, .explanatory-name {
        height: $text-height-small;
        line-height: $text-height-small;
        font-size: $fs-small;
        color: $gray;
      }
      .all-size, .explanatory-name, .target-name {
        padding-left: $padding-small;
        width: 50%;
      }
      .selected-explanatory-area {
        overflow-y: auto;
        width: 100%;
        height: 300px;
      }
      .description-text {
        width: 100%;
        margin-top: $margin-small;
      }
      .train-ratio-block {
        .label, .values {
          width: 50%;
        }
        .values {
          .valid-number {
            margin-left: auto;
          }
        }
      }
      .train-ratio-bar {
        width: 100%;
        .bar-item {
          height: 8px;
        }
      }
      .histogram-area {
        width: 100%;
        height: 100%;
        flex-wrap: wrap;
      }
      .histogram-plot {
        width: 50%;
      }
    }
  }
}
</style>
