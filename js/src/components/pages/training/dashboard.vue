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
