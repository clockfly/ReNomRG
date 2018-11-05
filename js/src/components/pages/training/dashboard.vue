<template>
  <div id="dashboard">
    <div class="panel">
      <div class="panel-title">
        Dashboard
      </div>

      <div class="panel-content dashboard-content">
        <!-- ratio bar -->
        <div class="total-models">
          <div class="label">Total Models:</div>
          <div class="value">{{model_list.length}}</div>
        </div>

        <div class="dashboard-ratio-bar">
          <div class="bar-legends">
            <div class="legend" v-for="(a, index) in algorithms">
              <div :class="'legend-color '+a.toLowerCase()"></div>
              <div class="legend-name">{{a}}</div>
            </div>
          </div>

          <div class="horizontal-bar">
            <div class="bar-item"
              v-for="(a, index) in algorithms"
              :class="a.toLowerCase()"
              v-bind:style="{ 'flex-grow': model_counts_per_algorith[a] }">
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
  computed: mapState(['algorithms', 'model_list', 'model_counts_per_algorith'])
}
</script>

<style lang="scss" scoped>
#dashboard {
  $group-margin: 16px;
  width: 100%;
  height: $dashboard-height;

  .dashboard-content {
    padding: 16px;
  }
  .total-models {
    @include prefix("display", "flex");
  }
  .dashboard-ratio-bar, .running-models {
    width: 100%;
    margin-top: $group-margin;
  }
  .dashboard-ratio-bar {
    .bar-legends {
      @include prefix("display", "flex");
      .legend {
        @include prefix("display", "flex");
        justify-content: center;
        align-items: center;
        margin-right: 8px;

        .legend-color {
          width: 8px;
          height: 8px;
          margin-right: 4px;
        }
        .legend-name {
          font-size: $fs-small;
        }
      }
    }

    .horizontal-bar {
      @include prefix("display", "flex");
      margin-top: 8px;
      .bar-item {
        height: 16px;
      }
    }
  }
}
</style>
