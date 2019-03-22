/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="dashboard">
    <div class="panel">
      <div class="panel-title">
        Dashboard
      </div>

      <div class="panel-content dashboard-content">
        <!-- ratio bar -->
        <div class="total-models flex">
          <div class="label">
            Total Models:
          </div>
          <div class="value">
            {{ model_list.length }}
          </div>
        </div>

        <div class="dashboard-ratio-bar">
          <div class="bar-legends flex">
            <div
              v-for="(a, index) in algorithms"
              :key="index"
              class="legend flex"
            >
              <div :class="'legend-color '+a.toLowerCase()" />
              <div class="legend-name">
                {{ a }}
              </div>
            </div>
          </div>

          <div class="horizontal-bar flex">
            <div
              v-for="(a, index) in algorithms"
              :key="index"
              class="bar-item"
              :class="a.toLowerCase()"
              :style="{ 'flex-grow': model_counts_per_algorith[a] }"
            />
          </div>
        </div>

        <!-- running models -->
        <div class="running-models">
          <div class="label">
            Running Models
          </div>

          <div
            v-for="(model, index) in $store.state.running_models"
            :key="index"
            class="running-model"
          >
            <div class="running-info flex">
              <div class="running-info-item">
                <div class="running-info-label">
                  Model ID
                </div>
                <div class="running-info-value">
                  {{ model.model_id }}
                </div>
              </div>
              <div
                v-if="![3, 4].includes(model.algorithm)"
                class="running-info-item"
              >
                <div class="running-info-label">
                  Epoch
                </div>
                <div class="running-info-value">
                  {{ model.nth_epoch }} / {{ model.total_epoch }}
                </div>
              </div>
              <div
                v-if="![3, 4].includes(model.algorithm)"
                class="running-info-item"
              >
                <div class="running-info-label">
                  Batch
                </div>
                <div class="running-info-value">
                  {{ model.nth_batch }} / {{ model.total_batch }}
                </div>
              </div>
              <div class="running-info-item progress-bar">
                <div
                  v-if="model.nth_epoch == model.total_epoch || model.canceled"
                  class="running-info-label"
                >
                  In calculating Feature Importance...
                </div>
                <div class="bar-background" />
                <div
                  :class="'bar-foreground '+$store.state.algorithms[model.algorithm].toLowerCase()"
                  :style="{ width: model.nth_batch * 100 / model.total_batch + '%' }"
                />
              </div>
              <div
                v-if="![3, 4].includes(model.algorithm) && model.nth_epoch != model.total_epoch && !model.canceled"
                class="running-info-item pause-button"
                @click="stop_model = model"
              >
                <div class="running-info-label" />
                <div class="running-info-value">
                  <i class="far fa-stop-circle icon" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ModalConfirm
      v-if="stop_model"
      @ok="deleteModel"
      @cancel="stop_model=undefined"
    >
      <div slot="contents">
        Would you like to stop Model ID: {{ stop_model.model_id }}?
      </div>
      <span slot="okbutton">
        <button
          class="button-ok"
          @click="stopModel"
        >
          Stop
        </button>
      </span>
    </ModalConfirm>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ModalConfirm from '@/components/common/modal_confirm'

export default {
  name: 'Dashboard',
  components: {
    ModalConfirm
  },
  data: function () {
    return {
      'stop_model': undefined
    }
  },
  computed: mapState(['algorithms', 'model_list', 'model_counts_per_algorith']),
  methods: {
    stopModel: function (model_id) {
      this.$store.dispatch('stopModel', { 'model_id': this.stop_model.model_id })
    }
  }
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
      .running-info-value {
        .icon {
          font-size: $fs-small;
          color: $light-gray;
        }
        .icon:hover {
          color: $gray;
        }
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
