<template>
  <div class="modal-dataset padding-bottom-16">
    <div class="column">
      dataset setting
      <InputTextWithLabel
        class="margin-bottom-8"
        :labeltext="'dataset name:'"
        :labelwidth="label_width"
        :value="name"
        @input="name = $event"></InputTextWithLabel>

      <InputTextWithLabel
        class="margin-bottom-8"
        :labeltext="'description:'"
        :labelwidth="label_width"
        :value="description"
        @input="description = $event"></InputTextWithLabel>

      <InputTextWithLabel
        class="margin-bottom-8"
        :labeltext="'train ratio:'"
        :labelwidth="label_width"
        :value="train_ratio"
        @input="train_ratio = parseFloat($event)"></InputTextWithLabel>

      <SelectBoxWithLabel
        class="margin-bottom-8"
        :labeltext="'target columns:'"
        :labelwidth="label_width"
        :options="$store.state.labels"
        :value="target_column_id"
        @input="target_column_id = parseInt($event)"></SelectBoxWithLabel>

      <div class="button-area">
        <Button :text="'Confirm'" @click="$emit('confirm', params())"></Button>
      </div>
    </div>

    <div class="column">
      <div class="dataset-detail">
        detail
        <div class="train-test-ratio">
          total: {{$store.state.train_index.length+$store.state.valid_index.length}}
          train: {{$store.state.train_index.length}}
          validation: {{$store.state.valid_index.length}}
          <div class="train-ratio-bar">
            <div class="bar-item"
              v-bind:style="{ 'background': curve_colors.train, 'flex-grow': $store.state.train_index.length }"></div>
            <div class="bar-item"
              v-bind:style="{ 'background': curve_colors.validation, 'flex-grow': $store.state.valid_index.length }"></div>
          </div>
        </div>
        <div id="train-test-histogram"></div>
      </div>
      <div class="button-area">
        <Button :text="'Save'" @click="$emit('save', params())"></Button>
        <Button :text="'Cancel'"
          :bordercolor="gray"
          :backgroundcolor="white"
          :textcolor="gray"
          @click="$emit('cancel')"></Button>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import { GRAY, WHITE, CURVE_COLORS } from '@/const'
import { max, min } from '@/utils'
import Button from '@/components/atoms/button'
import InputTextWithLabel from '@/components/molecules/input_text_with_label'
import SelectBoxWithLabel from '@/components/molecules/select_box_with_label'

export default {
  name: 'ModalDataset',
  components: {
    Button,
    InputTextWithLabel,
    SelectBoxWithLabel
  },
  data: function () {
    return {
      'name': '',
      'description': '',
      'train_ratio': 0.8,
      'target_column_id': 0,
      'gray': GRAY,
      'white': WHITE,
      'label_width': '160px',
      'w': 300,
      'h': 300,
      'curve_colors': CURVE_COLORS
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
      const threshold = (train_max - train_min) / 10
      const width = this.w
      const height = this.h

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
        .thresholds(threshold)
      const train_bins = histogram(target_train)
      const valid_bins = histogram(target_valid)
      console.log(valid_bins)

      svg.selectAll('.train_bars')
        .data(train_bins)
        .enter().append('rect')
        .attr('class', 'train_bars')
        .attr('fill', CURVE_COLORS.train)
        .attr('opacity', 0.5)
        .attr('x', 1)
        .attr('transform', function (d) { return 'translate(' + xScale(d.x0) + ',' + yScale(height - d.length) + ')' })
        .attr('width', function (d) { return xScale(d.x1) - xScale(d.x0) - 1 })
        .attr('height', function (d) { return yScale(d.length) })

      svg.selectAll('.valid_bars')
        .data(valid_bins)
        .enter().append('rect')
        .attr('class', 'valid_bars')
        .attr('fill', CURVE_COLORS.validation)
        .attr('opacity', 0.5)
        .attr('x', 1)
        .attr('transform', function (d) { return 'translate(' + xScale(d.x0) + ',' + yScale(height - d.length) + ')' })
        .attr('width', function (d) { return xScale(d.x1) - xScale(d.x0) - 1 })
        .attr('height', function (d) { return yScale(d.length) })
    },
    removeHistogram: function () {
      d3.select('#train-test-histogram').selectAll('*').remove()
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-dataset {
  @include prefix("display", "flex");
  width: 100%;
  height: 100%;

  .column {
    position: relative;
    width: 50%;
    height: 100%;
    .button-area {
      position: absolute;
      bottom: 0;
      right: 0;
    }
  }

  .train-ratio-bar {
    @include prefix("display", "flex");
    .bar-item {
      height: 8px;
    }
  }
}
</style>
