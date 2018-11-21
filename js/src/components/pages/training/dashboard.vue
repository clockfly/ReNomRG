<template>
  <div id="dashboard">
    <div class="panel">
      <div class="panel-title">
        Dashboard
      </div>

      <div class="panel-content dashboard-content">
        <!-- ratio bar -->
        <div class="total-models flex">
          <div class="label">Total Models:</div>
          <div class="value">{{model_list.length}}</div>
        </div>

        <div class="dashboard-ratio-bar">
          <div class="bar-legends flex">
            <div class="legend flex" v-for="(a, index) in algorithms">
              <div :class="'legend-color '+a.toLowerCase()"></div>
              <div class="legend-name">{{a}}</div>
            </div>
          </div>

          <div class="horizontal-bar flex">
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
            <div class="running-info flex">
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
  $info-height: 16px;
  $legend-box-size: 8px;

  width: 100%;
  height: $dashboard-height;

  .dashboard-content {
    padding: $padding-large;
  }
  .total-models {
    height: $text-height-regular;
    line-height: $text-height-regular;
    font-size: $fs-regular;
  }
  .dashboard-ratio-bar, .running-models {
    width: 100%;
    margin-top: $margin-middle;
  }
  .dashboard-ratio-bar {
    .bar-legends {
      .legend {
        justify-content: center;
        align-items: center;
        margin-right: $margin-small;

        .legend-color {
          width: $legend-box-size;
          height: $legend-box-size;
          margin-right: 4px;
        }
        .legend-name {
          font-size: $fs-small;
        }
      }
    }

    .horizontal-bar {
      margin-top: $margin-small;
      .bar-item {
        height: $info-height;
      }
    }
  }
  .running-models {
    .label {
      height: $text-height-regular;
      line-height: $text-height-regular;
      font-size: $fs-regular;
    }
    margin-top: $margin-large;
  }
  .running-model {
    margin-top: $margin-small;
  }
  .running-info {
    .running-info-item {
      flex-grow: 1;
      .running-info-label, .running-info-value {
        height: $info-height;
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
        top: calc(#{$info-height} + 4px);
      }
    }
    .pause-button {
      text-align: right;
    }
  }
}
</style>
