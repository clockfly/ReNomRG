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
            Feature Scaling
          </div>
          <div class="input-value">
            <select v-model="selected_scaling">
              <option
                v-for="(scaling, index) in $store.state.scalings"
                :key="index"
                :value="index"
              >
                {{ scaling }}
              </option>
            </select>
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block">
          <div class="label">
            Valiables
          </div>
          <div class="flex">
            <div class="selected-label">
              [Explanatory]
            </div>
            <div class="selected-label">
              [Target]
            </div>
          </div>
          <div class="flex">
            <div class="selected-scroll-area">
              <div
                v-for="id in explanatory_column_ids"
                :key="id"
                class="target-variable-name"
              >
                {{ $store.state.labels[id] }}
              </div>
            </div>
            <div class="selected-scroll-area">
              <div
                v-for="id in target_column_ids"
                :key="id"
                class="target-variable-name"
              >
                {{ $store.state.labels[id] }}
              </div>
            </div>
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div class="button-area">
        <button
          :disabled="name === '' || target_column_ids.length > 4 || target_column_ids.length === 0 || explanatory_column_ids.length === 0"
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
          Valiables
        </div>

        <div class="table-row flex">
          <div class="table-item-cb">
            Explanatory
          </div>
          <div class="table-item-cb">
            Target
          </div>
          <div class="table-item-tx">
            Valiable Name
          </div>
        </div>
        <div
          v-for="(label, index) in $store.state.labels"
          :key="index"
          class="table-row flex"
        >
          <div class="table-item-cb">
            <input
              :id="index"
              v-model="explanatory_column_ids"
              type="checkbox"
              :value="index"
              @click="select_explanatory(index)"
            >
          </div>
          <div class="table-item-cb">
            <input
              :id="index"
              v-model="target_column_ids"
              type="checkbox"
              :value="index"
              @click="select_target(index)"
            >
          </div>
          <div class="table-item-tx">
            {{ label }}
          </div>
        </div>
        <div class="table-row flex">
          <div class="table-item-cb">
            Check All
            <input
              type="checkbox"
              :checked="isAllSelected"
              @click="selectAll"
            >
          </div>
          <div class="table-item-cb">
          </div>
          <div class="table-item-tx">
          </div>
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
    let labels_array = [];
    for( let key in this.$store.state.labels ) {
      labels_array.push(Number(key));
    }
    return {
      'is_confirm': false,
      'name': '',
      'description': '',
      'train_ratio': 0.8,
      'train_ratio_list': [0.7, 0.8, 0.9],
      'explanatory_column_ids': labels_array,
      'isAllSelected': false,
      'target_column_ids': [],
      'selected_scaling': 1
    }
  },
  computed: {
    trainIndex: function () {
      return this.$store.state.train_index
    }
  },
  watch: {
    trainIndex: function () {
      const id = '#train-test-histogram'
      removeSvg(id)
      for (let hist of this.$store.state.true_histogram) {
        this.drawHistogram(id, hist.train, hist.valid)
      }
    }
  },
  methods: {
    select_target: function (val) {
      let e_columns = this.explanatory_column_ids;
      let idx = e_columns.indexOf(val);
      if(idx >= 0){
        e_columns.splice(idx, 1);
      }
      this.explanatory_column_ids = e_columns;
    },
    select_explanatory: function (val) {
      let t_columns = this.target_column_ids;
      let idx = t_columns.indexOf(val);
      if(idx >= 0){
        t_columns.splice(idx, 1);
      }
      this.target_column_ids = t_columns;
    },
    selectAll: function () {
      let labels_array = [];
      for( let key in this.$store.state.labels ) {
        labels_array.push(Number(key));
      }
      if (this.isAllSelected) {
        this.explanatory_column_ids = [];
        this.isAllSelected = false;
      } else {
        this.explanatory_column_ids = labels_array;
        this.target_column_ids = [];
        this.isAllSelected = true;
      }
    },
    params: function () {
      return {
        'name': this.name,
        'description': this.description,
        'train_ratio': this.train_ratio,
        'explanatory_column_ids': this.explanatory_column_ids,
        'target_column_ids': this.target_column_ids,
        'selected_scaling': this.selected_scaling
      }
    },
    drawHistogram: function (id, train_hist, valid_hist) {
      if (this.$store.state.train_index.length === 0) return

      // const parent_area = d3.select(id)
      // const width = parent_area._groups[0][0].clientWidth
      // const height = parent_area._groups[0][0].clientHeight
      const width = 120
      const height = 120
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

      // draw histogram train true
      const hist_max = max(train_hist.counts)
      const histy_scale = getScale([0, hist_max], [height - margin.bottom, margin.top])
      // const train_true_hist
      svg.append('path')
        .datum(train_hist.counts)
        .attr('fill', train_color)
        .attr('opacity', 0.2)
        .attr('stroke', train_color)
        .attr('stroke-width', 2)
        .attr('d', d3.area()
          .x(function (d, index) { return x_scale((train_hist.bins[index] + train_hist.bins[index + 1]) / 2) })
          .y1(function (d) { return histy_scale(d) })
          .y0(function (d) { return histy_scale(0) })
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
          .y1(function (d) { return histy_scale(d) })
          .y0(function (d) { return histy_scale(0) })
          .curve(d3.curveCardinal)
        )
    },
    confirmDataset: function () {
      this.$store.dispatch('confirmDataset', this.params())
      this.is_confirm = true
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

      .label, .input-value, .values, .target-variable-name, .train-number, .valid-number, .selected-label {
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
      .selected-label {
        padding-left: $padding-middle;
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
    .selected-scroll-area {
      overflow-y: auto;
      width: 50%;
      height: 140px;
      line-height: $text-height-small;
      font-size: $fs-small;
      color: $gray;
      padding-left: $padding-middle;
    }

    .variable-scroll-area {
      overflow-y: scroll;
      height: 90%;

      .table-row {
        width: 97%;
        margin: 0 auto;
        border-bottom: $border-width-regular solid $light-gray;
        .table-item-cb {
          width: 30%;
          height: $text-height-regular;
          line-height: $text-height-regular;
          text-align: center;
          font-size: $fs-small;
          color: $gray;
        }
        .table-item-tx {
          width: 40%;
          height: $text-height-regular;
          line-height: $text-height-regular;
          text-align: center;
          font-size: $fs-small;
          color: $gray;
        }
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
