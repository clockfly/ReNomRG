<template>
  <div class="modal-dataset flex">
    <div class="column">
      <div class="setting-block">
        <div class="setting-type">
          Dataset Setting
        </div>

        <div class="sub-block flex">
          <div class="label">
            Dataset Name
          </div>
          <div class="input-value">
            <input
              v-model="name"
              type="text"
            >
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block flex">
          <div class="label">
            Description
          </div>
          <div class="input-value description">
            <textarea
              v-model="description"
              name="description"
              rows="3"
            />
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block flex">
          <div class="label">
            Ratio of training data
          </div>
          <div class="input-value">
            <select v-model="train_ratio">
              <option
                v-for="ratio in train_ratio_list"
                :key="ratio"
                :value="ratio"
              >
                {{ ratio }}
              </option>
            </select>
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block flex">
          <div class="label">
            Target Valiables
          </div>
          <div class="input-value">
            <div
              v-for="id in target_column_ids"
              :key="id"
              class="target-variable-name"
            >
              {{ $store.state.labels[id] }}
            </div>
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div class="button-area">
        <button
          :disabled="name === '' || target_column_ids.length > 4 || target_column_ids.length === 0"
          @click="confirmDataset"
        >
          Confirm
        </button>
        <button
          class="button-cancel"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
      </div>
    </div>  <!-- column -->

    <div
      v-if="!is_confirm"
      class="column"
    >
      <div class="variable-scroll-area">
        <div class="setting-type">
          Target Valiables
        </div>
        <div
          v-for="(label, index) in $store.state.labels"
          :key="index"
          class="variable-item"
        >
          <input
            :id="index"
            v-model="target_column_ids"
            type="checkbox"
            :value="index"
          >
          <label :for="index">
            {{ label }}
          </label>
        </div>
      </div>
    </div> <!-- column before confirm -->

    <div
      v-if="is_confirm"
      class="column"
    >
      <div class="setting-block">
        <div class="setting-type">
          Detail
        </div>

        <div class="sub-block">
          <div class="flex">
            <div class="label">
              Number of data size
            </div>
            <div class="values flex">
              <div class="train-number">
                Train {{ $store.state.train_index.length }}
              </div>
              <div class="valid-number">
                Validation {{ $store.state.valid_index.length }}
              </div>
            </div>
          </div>
          <div class="flex">
            <div class="label">
              All {{ $store.state.train_index.length+$store.state.valid_index.length }}
            </div>
            <div class="values flex">
              <div class="train-ratio-bar flex">
                <div
                  class="bar-item train"
                  :style="{ 'flex-grow': $store.state.train_index.length }"
                />
                <div
                  class="bar-item validation"
                  :style="{ 'flex-grow': $store.state.valid_index.length }"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="sub-block flex">
          <div class="label">
            Histogram
          </div>
        </div>
        <div id="train-test-histogram" />
      </div> <!-- setting block -->

      <div class="button-area">
        <button @click="saveDataset">
          Save
        </button>
        <button
          class="button-cancel"
          @click="is_confirm = false"
        >
          Back
        </button>
      </div>
    </div> <!-- column after confirm -->
  </div>
</template>

<script>
import * as d3 from 'd3'
import { train_color, valid_color } from '@/const'
import { max, min, getScale, removeSvg, styleAxis } from '@/utils'

export default {
  name: 'ModalDataset',
  data: function () {
    return {
      'is_confirm': false,
      'name': '',
      'description': '',
      'train_ratio': 0.8,
      'train_ratio_list': [0.7, 0.8, 0.9],
      'target_column_ids': []
    }
  },
  computed: {
    targetTrain: function () {
      return this.$store.state.target_train
    }
  },
  watch: {
    targetTrain: function () {
      const id = '#train-test-histogram'
      removeSvg(id)
      for (let i in this.$store.state.target_train) {
        this.drawHistogram(id, this.$store.state.target_train[i], this.$store.state.target_valid[i])
      }
    }
  },
  methods: {
    params: function () {
      return {
        'name': this.name,
        'description': this.description,
        'train_ratio': this.train_ratio,
        'target_column_ids': this.target_column_ids
      }
    },
    drawHistogram: function (id, train, valid) {
      if (this.$store.state.train_index.length === 0) return

      // const parent_area = d3.select(id)
      // const width = parent_area._groups[0][0].clientWidth
      // const height = parent_area._groups[0][0].clientHeight
      const width = 120
      const height = 120
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
    confirmDataset: function () {
      this.$store.dispatch('confirmDataset', this.params())
      this.is_confirm = true
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
    saveDataset: function (value) {
      this.$store.dispatch('saveAndUpdateDataset', this.params())
      this.$emit('cancel')
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-dataset {
  width: 100%;
  height: calc(100% - #{$modal-tab-height});

  .column {
    position: relative;
    width: 50%;
    height: 100%;
    padding: $padding-large;

    .setting-type {
      height: $text-height-regular;
      line-height: $text-height-regular;
      font-size: $fs-regular;
    }
    .sub-block {
      margin-top: $margin-middle;
      margin-left: $margin-middle;

      .label, .input-value, .values, .target-variable-name, .train-number, .valid-number {
        width: 50%;
        height: $text-height-small;
        line-height: $text-height-small;
        font-size: $fs-small;
        color: $gray;
      }
      .description {
        height: calc(#{$text-height-small}*3);
      }
      .values {
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
    .variable-scroll-area {
      overflow-y: scroll;
      height: 90%;
      padding: 0 $padding-large;
      .variable-item {
        padding-left: $padding-large;
      }
      .variable-item, .variable-item label {
        height: $text-height-regular;
        line-height: $text-height-regular;
        font-size: $fs-small;
        color: $gray;
      }
    }
  }

  .train-ratio-bar {
    width: 100%;
    padding-top: $padding-small;
    .bar-item {
      height: 8px;
    }
  }
}
</style>
