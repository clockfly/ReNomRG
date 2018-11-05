<template>
  <div class="modal-dataset">
    <div class="column">

      <div class="setting-block">
        <div class="setting-type">
          Dataset Setting
        </div>

        <div class="sub-block">
          <div class="label">Dataset Name</div>
          <div class="input-value">
            <input type="text" v-model="name">
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block">
          <div class="label">Description</div>
          <div class="input-value">
            <input type="text" v-model="description">
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block">
          <div class="label">Ratio of training data</div>
          <div class="input-value">
            <input type="text" v-model="train_ratio">
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block">
          <div class="label">Target Valiable</div>
          <div class="input-value">
            <select v-model="target_column_id">
              <option v-for="(o, index) in $store.state.labels"
                :value="index" :key="index">
                {{ o }}
              </option>
            </select>
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div class="button-area">
        <button @click="confirmDataset">Confirm</button>
      </div>

    </div>  <!-- column -->

    <div class="column">

      <div class="setting-block">
        <div class="setting-type">
          Detail
        </div>

        <div class="sub-block">
          <div class="label">Number of data size</div>
          <div class="values">
            <div class="train-number">Train {{$store.state.train_index.length}}</div>
            <div class="valid-number">Validation {{$store.state.valid_index.length}}</div>
          </div>
        </div>

        <div class="sub-block">
          <div class="label">All {{$store.state.train_index.length+$store.state.valid_index.length}}</div>
          <div class="values">
            <div class="train-ratio-bar">
              <div class="bar-item train"
                v-bind:style="{ 'flex-grow': $store.state.train_index.length }"></div>
              <div class="bar-item validation"
                v-bind:style="{ 'flex-grow': $store.state.valid_index.length }"></div>
            </div>
          </div>
        </div>

        <div class="sub-block">
          <div class="label">Histogram</div>
        </div>
        <div id="train-test-histogram"></div>
      </div> <!-- setting block -->

      <div class="button-area">
        <button @click="saveDataset">Save</button>
        <button class="button-cancel"
          @click="$emit('cancel')">Cancel</button>
      </div>

    </div> <!-- column -->
  </div>
</template>

<script>
import * as d3 from 'd3'
import { max, min } from '@/utils'
const train_color = '#0762ad'
const valid_color = '#ef8200'
const width = 150
const height = 150

export default {
  name: 'ModalDataset',
  data: function () {
    return {
      'name': '',
      'description': '',
      'train_ratio': 0.8,
      'target_column_id': 0
    }
  },
  computed: {
    targetTrain: function () {
      return this.$store.state.target_train
    }
  },
  watch: {
    targetTrain: function () {
      this.drawHistogram()
    }
  },
  methods: {
    params: function () {
      return {
        'name': this.name,
        'description': this.description,
        'train_ratio': this.train_ratio,
        'target_column_id': this.target_column_id
      }
    },
    drawHistogram: function () {
      if (this.$store.state.train_index.length === 0) return
      this.removeHistogram()

      const target_train = this.$store.state.target_train
      const target_valid = this.$store.state.target_valid
      const train_max = max(target_train)
      const train_min = min(target_train)
      const valid_max = max(target_valid)
      const valid_min = min(target_valid)

      const svg = d3.select('#train-test-histogram')
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const xScale = d3.scaleLinear()
        .domain([min([train_min, valid_min]), max([train_max, valid_max])])
        .range([0, width])
      const yScale = d3.scaleLinear()
        .domain([height, 0])
        .range([height, 0])

      let histogram = d3.histogram()
        .value(function (d) { return d })
        .domain(xScale.domain())
        .thresholds(xScale.ticks(10))
      const train_bins = histogram(target_train)
      const valid_bins = histogram(target_valid)

      let LineLayer = svg.append('g').attr('clip-path', 'url(#clip)')

      // draw cardinal area chart
      LineLayer.append('path')
        .datum(train_bins)
        .attr('fill', train_color)
        .attr('opacity', 0.3)
        .attr('stroke', train_color)
        .attr('stroke-width', 1.5)
        .attr('d', d3.area()
          .x(function (d, index) { return xScale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return yScale(height - d.length) })
          .y0(function (d) { return yScale(height) })
          .curve(d3.curveCardinal)
        )

      LineLayer.append('path')
        .datum(valid_bins)
        .attr('fill', valid_color)
        .attr('opacity', 0.3)
        .attr('stroke', valid_color)
        .attr('stroke-width', 1.5)
        .attr('d', d3.area()
          .x(function (d, index) { return xScale((d.x0 + d.x1) / 2) })
          .y1(function (d) { return yScale(height - d.length) })
          .y0(function (d) { return yScale(height) })
          .curve(d3.curveCardinal)
        )
    },
    removeHistogram: function () {
      d3.select('#train-test-histogram').selectAll('*').remove()
    },
    confirmDataset: function () {
      this.$store.dispatch('confirmDataset', this.params())
    },
    saveDataset: function (value) {
      this.$store.dispatch('saveDataset', this.params())
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-dataset {
  @include prefix("display", "flex");
  width: 100%;
  height: calc(100% - #{$modal-tab-height});

  .column {
    position: relative;
    width: 50%;

    .setting-block {
      margin-top: 24px;
      margin-left: 24px;
    }
    .sub-block {
      @include prefix("display", "flex");
      margin-top: 16px;
      margin-left: 16px;

      .label, .input-value, .values {
        width: 50%;
      }
      .values {
        @include prefix("display", "flex");
        .train-number, .valid-number {
          color: $gray;
        }
        .valid-number {
          margin-left: auto;
        }
      }
    }
    .setting-type, .label {
      color: $gray;
    }

    .button-area {
      position: absolute;
      bottom: 0px;
      right: 0px;
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
</style>
