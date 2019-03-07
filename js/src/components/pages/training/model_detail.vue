/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="model-params">
    <div class="panel">
      <div class="panel-title panel-title-button-area">
        Model Detail
        <div
          v-if="selectedModel && selectedModel.deployed === 0"
          class="panel-title-button"
          @click="deploy_model=selectedModel"
        >
          > Deploy Model
        </div>
        <div
          v-else-if="selectedModel && selectedModel.deployed === 1"
          class="panel-title-button"
          @click="undeploy_model=selectedModel"
        >
          > Undeploy Model
        </div>
      </div>

      <div class="panel-content detail flex">
        <div class="column">
          <div class="label-value model-id flex">
            <div class="label">
              Model ID
            </div>
            <div
              v-if="selectedModel"
              class="value"
            >
              {{ selectedModel.model_id }}
            </div>
          </div>
        </div>

        <div
          v-if="selectedModel && selectedDataset"
          class="column"
        >
          <div class="label-value flex">
            <div class="label">
              Dataset
            </div>
            <div class="value">
              {{ selectedDataset.name }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              Feature Scaling
            </div>
            <div class="value">
              {{ $store.state.scalings[selectedDataset.selected_scaling] }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              Algorithm
            </div>
            <div class="value">
              {{ $store.state.algorithms[selectedModel.algorithm] }}
            </div>
          </div>

          <div v-if="![3, 4].includes(selectedModel.algorithm)">
            <div class="label-value flex">
              <div class="label">
                Total Epoch
              </div>
              <div class="value">
                {{ selectedModel.epoch }}
              </div>
            </div>

            <div class="label-value flex">
              <div class="label">
                Batch Size
              </div>
              <div class="value">
                {{ selectedModel.batch_size }}
              </div>
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              Validation Loss
            </div>
            <div class="value">
              {{ round(selectedModel.best_epoch_valid_loss) }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              RMSE
            </div>
            <div class="value">
              {{ round(selectedModel.best_epoch_rmse) }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              Max Absolute Error
            </div>
            <div class="value">
              {{ round(selectedModel.best_epoch_max_abs_error) }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              R2 Score
            </div>
            <div class="value">
              {{ round(selectedModel.best_epoch_r2) }}
            </div>
          </div>
        </div>

        <div
          v-if="selectedModel"
          class="column"
        >
          <div v-if="![3, 4].includes(selectedModel.algorithm)">
            <div class="label-value">
              <div class="label">
                Graph Comvolution Params
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Number of Neighbors
              </div>
              <div class="value">
                {{ selectedModel.algorithm_params.num_neighbors }}
              </div>
            </div>
          </div>
          <div v-else>
            <div class="label-value">
              <div
                v-if="selectedModel.algorithm == 3"
                class="label"
              >
                Random Forest Params
              </div>
              <div
                v-else-if="selectedModel.algorithm == 4"
                class="label"
              >
                XGBoost Params
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Number of trees
              </div>
              <div class="value">
                {{ selectedModel.algorithm_params.n_estimators }}
              </div>
            </div>
            <div class="label-value flex">
              <div class="label">
                Maximum Depth
              </div>
              <div class="value">
                {{ selectedModel.algorithm_params.max_depth }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ModalConfirm
      v-if="deploy_model"
      @ok="deploy"
      @cancel="deploy_model=undefined"
    >
      <div slot="contents">
        Would you like to deploy Model ID: {{ deploy_model.model_id }}?
      </div>
      <span slot="okbutton">
        <button
          class="button-ok"
          @click="deploy"
        >
          Deploy
        </button>
      </span>
    </ModalConfirm>

    <ModalConfirm
      v-if="undeploy_model"
      @ok="undeploy"
      @cancel="undeploy_model=undefined"
    >
      <div slot="contents">
        Would you like to undeploy Model ID: {{ undeploy_model.model_id }}?
      </div>
      <span slot="okbutton">
        <button
          class="button-ok"
          @click="undeploy"
        >
          Undeploy
        </button>
      </span>
    </ModalConfirm>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { round } from '@/utils'
import ModalConfirm from '@/components/common/modal_confirm'

export default {
  name: 'ModelParams',
  components: {
    ModalConfirm
  },
  data: function () {
    return {
      'deploy_model': undefined,
      'undeploy_model': undefined
    }
  },
  computed: mapGetters(['selectedModel', 'selectedDataset']),
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    deploy: function () {
      this.$store.dispatch('deployAndUpdate', { 'model_id': this.selectedModel.model_id })
    },
    undeploy: function () {
      this.$store.dispatch('undeployAndUpdate', { 'model_id': this.selectedModel.model_id })
    }
  }
}
</script>

<style lang="scss" scoped>
#model-params {
  width: 100%;
  height: $model-detail-height;

  .detail {
    width: 100%;
    padding: $padding-large;

    .column {
      flex-grow: 1;
      height: 100%;

      .label-value {
        .label, .value {
          height: $text-height-small;
          line-height: $text-height-small;
          font-size: $fs-small;
        }
        .label {
          margin-right: $margin-small;
          color: $gray;
        }
      }
      .model-id {
        .label, .value {
          font-size: $fs-regular;
        }
      }
    }
  }
}
</style>
