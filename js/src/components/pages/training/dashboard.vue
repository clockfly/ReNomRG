<template>
  <div id="dashboard">
    <div class="panel">
      <div class="panel-title">
        Dashboard
      </div>

      <div class="panel-content">
        <!-- ratio bar -->
        <div class="dashboard-ratio-bar">
          <div class="label-value">
            <div class="label">Total Models:</div>
            <div class="value">{{model_list.length}}</div>
          </div>

          <div class="bar-legends">
            <div class="legend" v-for="(color, index) in bar_colors">
              <div class="legend-color" v-bind:style="{ 'background': color }"></div>
              <div class="legend-name">{{index}}</div>
            </div>
          </div>

          <div class="horizontal-bar">
            <div class="bar-item"
              v-for="(model_count, index) in model_counts_per_algorith"
              v-bind:style="{ 'background': bar_colors[index], 'flex-grow': model_count }">
            </div>
          </div>
        </div>

        <!-- running models -->
        <div class="running-models"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Dashboard',
  data: function () {
    return {
      'bar_colors': {
        'C-GCNN': '#903e84',
        'Kernel-GCNN': '#423885',
        'DBSCAN-GCNN': '#136eab',
        'Running': '#0099ce',
        'Reserved': '#cccccc'
      }
    }
  },
  computed: mapState(['model_list', 'model_counts_per_algorith'])
}
</script>

<style lang="scss" scoped>
#dashboard {
  .dashboard-ratio-bar {
    width: 100%;
    .label-value {
      @include prefix("display", "flex");
    }
    .bar-legends {
      @include prefix("display", "flex");
      .legend {
        @include prefix("display", "flex");
        justify-content: center;
        align-items: center;
        margin-right: 16px;

        .legend-color {
          width: 8px;
          height: 8px;
          margin-right: 4px;
        }
      }
    }

    .horizontal-bar {
      @include prefix("display", "flex");
      .bar-item {
        height: 8px;
      }
    }
  }

  .running-models {}
}
</style>
