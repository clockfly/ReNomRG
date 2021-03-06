/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="model-map">
    <div class="panel">
      <div class="panel-title">
        Model Map
      </div>

      <div
        id="value-map"
        class="panel-content"
      >
        <div class="x-axis-name">
          RMSE (Root Mean Squared Error)
        </div>
        <div class="y-axis-name">
          Max Absolute Error
        </div>
        <div id="map-tooltip" />
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import { mapState } from 'vuex'
import { algorithm_colors } from '@/const'
import { max, min, round, getScale, removeSvg, styleAxis } from '@/utils'

export default {
  name: 'ModelMap',
  computed: mapState(['model_list', 'selected_model_id']),
  watch: {
    model_list: function () {
      this.drawMap()
    },
    selected_model_id: function () {
      this.drawMap()
    }
  },
  created: function() {
    window.addEventListener('resize', this.drawMap, false)
  },
  beforeDestroy: function () {
    window.removeEventListener('resize', this.drawMap, false)
  },
  methods: {
    drawMap: function () {
      if (!this.$store.state.model_list) return
      const id = '#value-map'
      removeSvg(id)

      const store = this.$store
      const [rmse_list, max_abs_error_list, dataset] = this.shapeDataset()

      const parent_area = d3.select(id)
      const width = parent_area._groups[0][0].clientWidth
      const height = parent_area._groups[0][0].clientHeight
      const margin = { 'left': 60, 'top': 40, 'right': 40, 'bottom': 60 }
      const rmse_min = min(rmse_list)
      const rmse_max = max(rmse_list)
      const mae_min = min(max_abs_error_list)
      const mae_max = max(max_abs_error_list)

      const svg = d3.select(id)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      const x_scale = getScale([rmse_min, rmse_max], [margin.left, width - margin.right])
      const y_scale = getScale([mae_min, mae_max], [height - margin.bottom, margin.top])

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

      const tooltip = d3.select('#map-tooltip')
      const algorithms = this.$store.state.algorithms
      const selected_mi = this.$store.state.selected_model_id

      for( let m_v in dataset ) {
        if (dataset[m_v][4]) {
          svg.append('g')
            .selectAll('circle')
            .data(dataset)
            .enter()
            .append('circle')
            .attr('cx', function (d) { return x_scale(d[0]) })
            .attr('cy', function (d) { return y_scale(d[1]) })
            .attr('fill', function (d) { return algorithm_colors[algorithms[d[3]]] })
            .attr('r', function (d) {
              if (d[2] == selected_mi) {
                return 5
              } else {
                return 3
              }
            })
            .on('mouseover', function (d) {
              tooltip.html('model_id: ' + d[2] + '<br>algorithm: ' + algorithms[d[3]] + '<br>RMSE: ' + round(d[0], 1000) + '<br>MaxAbsError: ' + round(d[1], 1000))
                .attr('class', algorithms[d[3]].toLowerCase())
                .style('left', (parseInt(d3.select(this).attr('cx')) - 100) + 'px')
                .style('top', (parseInt(d3.select(this).attr('cy')) + 10) + 'px')
                .style('display', 'inline-block')
            })
            .on('mouseout', function (d) {
              tooltip.style('display', 'none')
            })
            .on('click', function (d) {
              store.commit('setSelectedModelId', {'model_id': d[2]})
            })
        } else {
          let arr = [];
          for (let i = 0; i < 100; i++) {
            arr.push(0)
          }
          const d_4 = dataset[m_v]
          arr.forEach(function(nd,ni){
            svg.append('g')
            .append('circle')
            .attr('cx', function (dataset) { return x_scale(d_4[0]) })
            .attr('cy', function (dataset) { return y_scale(d_4[1]) })
            .attr('fill', function (dataset) { return algorithm_colors[algorithms[d_4[3]]] })
            .attr('r', function (d) {
              if (d_4[2] == selected_mi) {
                return 5
              } else {
                return 3
              }
            })
            .on('mouseover', function (dataset) {
              tooltip.html('model_id: ' + d_4[2] + '<br>algorithm: ' + algorithms[d_4[3]] + '<br>RMSE: ' + round(d_4[0], 1000) + '<br>MaxAbsError: ' + round(d_4[1], 1000))
                .attr('class', algorithms[d_4[3]].toLowerCase())
                .style('left', (parseInt(d3.select(this).attr('cx')) - 100) + 'px')
                .style('top', (parseInt(d3.select(this).attr('cy')) + 10) + 'px')
                .style('display', 'inline-block')
            })
            .on('mouseout', function (dataset) {
              tooltip.style('display', 'none')
            })
            .on('click', function (dataset) {
              store.commit('setSelectedModelId', {'model_id': d_4[2]})
            })
            .transition().delay(ni * 1500).duration(750)
            .style('stroke', function (dataset) { return algorithm_colors[algorithms[d_4[3]]] })
            .style('stroke-width', 5)
            .transition().duration(750)
            .style('stroke', '#FFFFFF')
            .style('stroke-width', 5)
          })
        }
      }
    },
    shapeDataset: function () {
      let rmse_list = []
      let max_abs_error_list = []
      let dataset = []
      for (let m of this.$store.state.model_list) {
        let d = [m.best_epoch_rmse, m.best_epoch_max_abs_error, m.model_id, m.algorithm, m.importances]
        rmse_list.push(m.best_epoch_rmse)
        max_abs_error_list.push(m.best_epoch_max_abs_error)
        dataset.push(d)
      }
      return [rmse_list, max_abs_error_list, dataset]
    }
  }
}
</script>

<style lang="scss" scoped>
#model-map {
  width: 100%;
  height: $model-map-height;

  #value-map {
    position: relative;

    .x-axis-name, .y-axis-name {
      position: absolute;
      font-size: $fs-small;
      color: $light-gray;
    }
    .x-axis-name {
      bottom: 24px;
      left: 42%;
      @include prefix("transform", "translateX(-30%)");
    }
    .y-axis-name {
      top: 16px;
      left: 16px;
    }
    #map-tooltip {
      display: none;
      position: absolute;
      z-index: 999;
      width: 200px;
      padding: 16px;
      font-size: $fs-small;
      line-height:  1.5;
      color: $white;
    }
  }
}
</style>
