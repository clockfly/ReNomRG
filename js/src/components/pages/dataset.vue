<template>
  <div id="page">
    <div class="dataset-list">
      <div class="panel">
        <div class="panel-title panel-with-button">
          Dataset List
          <div class="setting-button" @click="show_modal = true">
            > Setting of Dataset
          </div>
        </div>

        <div class="panel-content dataset-list-content">
          <div class="content-left">
            <div class="table-header">
              <div class="table-row">
                <div class="table-item">Dataset Name</div>
                <div class="table-item">Train Data</div>
                <div class="table-item">Validation Date</div>
              </div>
            </div>
            <div class="table-content">
              <div class="table-row" v-for="(dataset, index) in $store.state.dataset_list" :key="index" @click="selected_dataset_index = index">
                <div class="table-item">{{ dataset.name }}</div>
                <div class="table-item">{{ dataset.train_index.length }}</div>
                <div class="table-item">{{ dataset.valid_index.length }}</div>
              </div>
            </div>
          </div> <!-- content-left dataset list -->

          <div class="content-right" v-if="selectedDataset">
            <div class="dataset-name">
              {{selectedDataset.name}}
            </div>
            <div class="dataset-detail">
              <div class="column">

                <div class="dataset-description-area">
                  <div class="label">Description</div>
                  <textarea class="description-text" :placeholder="selectedDataset.description" disabled></textarea>
                </div> <!-- dataset description area -->

                <div class="train-ratio-area">
                  <div class="sub-block">
                    <div class="label">Number of data size</div>
                    <div class="values">
                      <div class="train-number">Train {{selectedDataset.train_index.length}}</div>
                      <div class="valid-number">Validation {{selectedDataset.valid_index.length}}</div>
                    </div>
                  </div>

                  <div class="sub-block">
                    <div class="label">All {{selectedDataset.train_index.length+selectedDataset.valid_index.length}}</div>
                    <div class="values">
                      <div class="train-ratio-bar">
                        <div class="bar-item train"
                          v-bind:style="{ 'flex-grow': selectedDataset.train_index.length }"></div>
                        <div class="bar-item validation"
                          v-bind:style="{ 'flex-grow': selectedDataset.valid_index.length }"></div>
                      </div>
                    </div>
                  </div>
                </div> <!-- dataset train valid ratio area -->
              </div> <!-- dataset detail column -->

              <div class="column">
                <div class="label">Histogram</div>
                <div id="train-test-histogram"></div>
              </div>
            </div>
          </div> <!-- content-right dataset detail -->
        </div>
      </div>
    </div>

    <ModalDataset v-if="show_modal" @hide="show_modal = false"></ModalDataset>
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
      this.drawHistograms()
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
      const id = '#train-test-histogram'
      removeSvg(id)
      for (let i in this.selectedDataset.target_train) {
        this.drawHistogram(id, this.selectedDataset.target_train[i], this.selectedDataset.target_valid[i])
      }
    },
    drawHistogram: function (id, train, valid) {
      const width = 150
      const height = 150
      const margin = { 'left': 20, 'top': 20, 'right': 20, 'bottom': 20 }

      const target_train = train
      const target_valid = valid
      const train_max = max(target_train)
      const train_min = min(target_train)
      const valid_max = max(target_valid)
      const valid_min = min(target_valid)

      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const x_scale = getScale([min([train_min, valid_min]), max([train_max, valid_max])], [margin.left, width - margin.right])
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
      const histogram = this.getHistgram(x_scale, 10)
      const train_bins = histogram(target_train)
      const valid_bins = histogram(target_valid)
      const hist_max = this.getHistgramSizeMax(train_bins)

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
        .datum(train_bins)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return y_scale(d.length) })
          .y0(function (d) { return y_scale(0) })
          .curve(d3.curveCardinal)
        )

      svg.append('path')
        .datum(valid_bins)
        .attr('fill', valid_color)
        .attr('opacity', 0.2)
        .attr('stroke', valid_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return y_scale(d.length) })
          .y0(function (d) { return y_scale(0) })
          .curve(d3.curveCardinal)
        )
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
    removeHistogram: function (id) {
      d3.select(id).selectAll('svg').remove()
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

  .dataset-list {
    width: 100%;
    height: 100%;
  }

  .panel-with-button {
    @include prefix("display", "flex");
    .setting-button {
      margin-left: auto;
      padding: 0 $panel-content-padding;
      background: $blue;
      color: $white;
    }
  }

  .dataset-list-content {
    @include prefix('display', 'flex');
    padding: $panel-content-padding;
  }
  .content-left {
    width: 30%;
    height: 100%;
    padding-right: $panel-content-padding;
    border-right: 1px solid $light-gray;

    .table-header {
      padding-right: 10px; // margin of table-content scrollbar size
    }
    .table-content {
      width: 100%;
      height: calc(100% - #{$table-item-height});
      overflow-y: scroll;
    }
    .table-row {
      @include prefix('display', 'flex');
      width: $table-width;
      margin: 0 auto;
      border-bottom: 1px solid $light-gray;
    }
    .table-row:hover .table-item {
      color: $light-gray;
    }
    .table-item {
      width: 33%;
      height: $table-item-height;
      line-height: $table-item-height;
      text-align: center;
      font-size: $fs-small;
      color: $gray;
    }
  }

  .content-right {
    width: 70%;
    height: 100%;
    padding: 32px;

    .dataset-name {
      color: $blue;
    }
    .dataset-detail {
      @include prefix('display', 'flex');
      width: 100%;
      .column {
        width: 50%;
        padding: 16px;
      }
      .train-ratio-area {
        margin-top: 32px;
      }
      .label, .train-number, .valid-number {
        color: $gray;
      }
      .description-text {
        width: 100%;
        margin-top: 8px;
      }
      .sub-block {
        @include prefix("display", "flex");
        margin-top: 16px;
        .label, .values {
          width: 50%;
        }
        .values {
          @include prefix("display", "flex");
          .valid-number {
            margin-left: auto;
          }
        }
      }
      .train-ratio-bar {
        @include prefix("display", "flex");
        width: 100%;
        .bar-item {
          height: 8px;
        }
      }
    }
  }
}
</style>
