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
        <div class="running-models">
          <div class="label">Running Models</div>

          <div class="running-model" v-for="(model, index) in $store.state.running_models">
            <div class="running-info">
              <div class="running-info-item">
                <div class="running-info-label">Model ID</div>
                <div class="running-info-value">{{model.model_id}}</div>
              </div>
              <div class="running-info-item">
                <div class="running-info-label">Epoch</div>
                <div class="running-info-value">{{model.nth_epoch}} / {{model.total_epoch}}</div>
              </div>
              <div class="running-info-item">
                <div class="running-info-label">Batch</div>
                <div class="running-info-value">{{model.nth_batch}} / {{model.total_batch}}</div>
              </div>
              <div class="running-info-item progress-bar">
                <div class="bar-background"></div>
                <div :class="'bar-foreground '+$store.state.algorithms[model.algorithm].toLowerCase()"
                  :style="{ width: model.nth_epoch * 100 / model.total_epoch + '%' }">
                </div>
              </div>
              <div class="running-info-item pause-button">
                <div class="running-info-label"></div>
                <div class="running-info-value">
                  <i class="far fa-pause-circle"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
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
    padding: $panel-content-padding;
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
  .running-info {
    @include prefix("display", "flex");
    .running-info-item {
      flex-grow: 1;
      .running-info-label, .running-info-value {
        height: 16px;
        line-height: 16px;
        font-size: $fs-small;
      }
      .running-info-label {
        color: $light-gray;
      }
    }
    .progress-bar {
      flex-grow: 4;
      position: relative;
      .bar-background {
        width: 100%;
        background-color: $light-gray;
      }
      .bar-background, .bar-foreground {
        position: absolute;
        height: 8px;
        top: 20px;
      }
    }
    .pause-button {
      text-align: right;
    }
  }
}
</style>
