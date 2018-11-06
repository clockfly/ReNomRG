<template>
  <div id="model-params">
    <div class="panel">
      <div class="panel-title panel-with-button">
        Model Detail
        <div class="deploy-button" v-if="model && model.deployed === 0" @click="deploy">
          > Deploy Model
        </div>
        <div class="deploy-button" v-if="model && model.deployed === 1" @click="undeploy">
          > Undeploy Model
        </div>
      </div>

      <div class="panel-content detail">
        <div class="column">
          <div class="label-value model-id">
            <div class="label">Model ID</div>
            <div class="value" v-if="model">{{model.model_id}}</div>
          </div>
        </div>

        <div class="column" v-if="model">
          <div class="label-value">
            <div class="label">Algorithm</div>
            <div class="value">{{$store.state.algorithms[model.algorithm]}}</div>
          </div>

          <div class="label-value">
            <div class="label">Total Epoch</div>
            <div class="value">{{model.epoch}}</div>
          </div>

          <div class="label-value">
            <div class="label">Batch Size</div>
            <div class="value">{{model.batch_size}}</div>
          </div>

          <div class="label-value">
            <div class="label">Validation Loss</div>
            <div class="value">{{round(model.best_epoch_valid_loss)}}</div>
          </div>

          <div class="label-value">
            <div class="label">RMSE</div>
            <div class="value">{{round(model.best_epoch_rmse)}}</div>
          </div>

          <div class="label-value">
            <div class="label">Max Absolute Error</div>
            <div class="value">{{round(model.best_epoch_max_abs_error)}}</div>
          </div>

          <div class="label-value">
            <div class="label">R2 Score</div>
            <div class="value">{{round(model.best_epoch_r2)}}</div>
          </div>
        </div>

        <div class="column" v-if="model">
          <div class="label-value">
            <div class="label">Graph Comvolution Params</div>
          </div>

          <div class="label-value">
            <div class="label">Number of Neighbors</div>
            <div class="value">{{model.algorithm_params.num_neighbors}}</div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { round } from '@/utils'

export default {
  name: 'ModelParams',
  computed: {
    model: function () {
      return this.$store.state.selected_model
    }
  },
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    deploy: function () {
      this.$store.dispatch('deployAndUpdate', { 'model_id': this.model.model_id })
      this.$store.commit('updateDeployModel')
    },
    undeploy: function () {
      this.$store.dispatch('undeployAndUpdate', { 'model_id': this.model.model_id })
    }
  }
}
</script>

<style lang="scss" scoped>
#model-params {
  width: 100%;
  height: $model-detail-height;

  .panel-with-button {
    @include prefix("display", "flex");
    .deploy-button {
      margin-left: auto;
      padding: 0 $panel-content-padding;
      background: $blue;
      color: $white;
    }
  }

  .detail {
    @include prefix("display", "flex");
    width: 100%;
    padding: $panel-content-padding;

    .column {
      flex-grow: 1;
      height: 100%;

      .label-value {
        @include prefix("display", "flex");
        margin-bottom: 8px;
        font-size: $fs-small;
        .label {
          margin-right: 8px;
          color: $gray;
        }
      }
      .model-id {
        font-size: $fs-regular;
      }
    }
  }
}
</style>
