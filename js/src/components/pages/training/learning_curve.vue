<template>
  <div id="learning-curve">
    <div class="panel">
      <div class="panel-title">
        Learning Curve
      </div>
      <div
        id="curve-canvas"
        :class="gray_back"
      >
        <div v-if="selectedModel && selectedModel.algorithm != 3">
          <div class="x-axis-name">
            Epoch
          </div>
          <div class="y-axis-name">
            Loss [-]
          </div>
          <div class="bar-legends flex">
            <div class="legend flex">
              <div class="legend-color train" />
              <div class="legend-name">
                Train
              </div>
            </div>

            <div class="legend flex">
              <div class="legend-color validation" />
              <div class="legend-name">
                Validation
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
import { mapGetters } from 'vuex'
import { train_color, valid_color } from '@/const'
import { max, getScale, removeSvg, styleAxis } from '@/utils'

export default {
  name: 'LerningCurve',
  computed: {
    ...mapGetters(['selectedModel']),
    gray_back: function () {
      if (this.selectedModel && this.selectedModel.algorithm == 3) {
        return 'panel-content gray-back'
      } else {
        return 'panel-content'
      }
    }
  },
  watch: {
    selectedModel: function () {
      const id = '#curve-canvas'
      removeSvg(id)
      this.drawCurve()
    }
  },
  mounted: function () {
    this.drawCurve()
  },
  methods: {
    drawCurve: function () {
      if (!this.selectedModel || !this.selectedModel.train_loss_list || !this.selectedModel.valid_loss_list) return

      const id = '#curve-canvas'
      const train_list = this.selectedModel.train_loss_list
      const valid_list = this.selectedModel.valid_loss_list

      const parent_area = d3.select(id)
      const width = parent_area._groups[0][0].clientWidth
      const height = parent_area._groups[0][0].clientHeight
      const margin = { 'left': 60, 'top': 40, 'right': 60, 'bottom': 40 }
      const train_max = max(train_list)
      const valid_max = max(valid_list)

      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const x_scale = getScale([0, train_list.length], [margin.left, width - margin.right])
      const y_scale = getScale([0, max([train_max, valid_max])], [height - margin.bottom, margin.top])

      // draw x axis
      const x_axis_define = d3.axisBottom(x_scale)
        .tickSizeInner(-(height - margin.top - margin.bottom))
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)
      const x_axis = svg.append('g')
        .attr('transform', 'translate(' + 0 + ',' + (height - margin.bottom) + ')')
        .call(x_axis_define)
      styleAxis(x_axis)

      // draw y axis
      const y_axis_define = d3.axisLeft(y_scale)
        .tickSizeInner(-(width - margin.left - margin.right))
        .tickSizeOuter(0)
        .ticks(10)
        .tickPadding(10)
      const y_axis = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + 0 + ')')
        .call(y_axis_define)
      styleAxis(y_axis)

      // draw line chart
      svg.append('path')
        .datum(train_list)
        .attr('fill', 'none')
        .attr('stroke', train_color)
        .attr('stroke-width', 1.5)
        .attr('d', d3.line()
          .x(function (d, index) { return x_scale(index) })
          .y(function (d) { return y_scale(d) })
          .curve(d3.curveLinear)
        )

      // draw line chart
      svg.append('path')
        .datum(valid_list)
        .attr('fill', 'none')
        .attr('stroke', valid_color)
        .attr('stroke-width', 1.5)
        .attr('d', d3.line()
          .x(function (d, index) { return x_scale(index) })
          .y(function (d) { return y_scale(d) })
          .curve(d3.curveLinear)
        )
    }
  }
}
</script>

<style lang="scss" scoped>
#learning-curve {
  width: 100%;
  height: $learning-curve-height;

  #curve-canvas {
    position: relative;

    .x-axis-name, .y-axis-name, .bar-legends {
      position: absolute;
      font-size: $fs-micro;
      color: $light-gray;
    }
    .x-axis-name {
      bottom: 12px;
      right: 40px;
    }
    .y-axis-name {
      top: 16px;
      left: 32px;
    }
    .bar-legends {
      top: 16px;
      right: 16px;

      .legend {
        justify-content: center;
        align-items: center;
        margin-right: $margin-middle;

        .legend-color {
          width: 8px;
          height: 8px;
          margin-right: 4px;
        }
        .legend-name {
          font-size: $fs-micro;
          color: $gray;
        }
      }
    }
  }
  .gray-back {
    background-color: $grayout-back;
    filter: grayscale(1);
  }
}
</style>
