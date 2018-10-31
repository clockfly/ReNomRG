<template>
  <div id="model-params">
    <div class="panel">
      <div class="panel-title">
        Model Detail
      </div>

      <div class="panel-content detail">
        <div class="column" v-if="model">

          <div class="label-value">
            <div class="label">Model ID:</div>
            <div class="value">{{model.model_id}}</div>
          </div>

          <div class="label-value">
            <div class="label">Algorithm:</div>
            <div class="value">{{model.algorithm}}</div>
          </div>

          <div class="label-value">
            <div class="label">Total Epoch:</div>
            <div class="value">{{model.epoch}}</div>
          </div>

          <div class="label-value">
            <div class="label">Batch Size:</div>
            <div class="value">{{model.batch_size}}</div>
          </div>

          <div class="label-value">
            <div class="label">Number of Neighbors:</div>
            <div class="value">{{model.algorithm_params.num_neighbors}}</div>
          </div>

        </div>

        <div class="column" v-if="model">
          <div class="label-value">
            <div class="label">Validation Loss:</div>
            <div class="value">{{round(model.best_epoch_valid_loss)}}</div>
          </div>

          <div class="label-value">
            <div class="label">RMSE:</div>
            <div class="value">{{round(model.best_epoch_rmse)}}</div>
          </div>

          <div class="label-value">
            <div class="label">Max Absolute Error:</div>
            <div class="value">{{round(model.best_epoch_max_abs_error)}}</div>
          </div>

          <div class="label-value">
            <div class="label">R2 Score:</div>
            <div class="value">{{round(model.best_epoch_r2)}}</div>
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
    }
  }
}
</script>

<style lang="scss" scoped>
#model-params {
  .detail {
    @include prefix("display", "flex");
    width: 100%;
    height: 100%;

    .column {
      width: 50%;
      height: 100%;

      .label-value {
        @include prefix("display", "flex");
        .label {
          color: $gray;
        }
      }
    }
  }
}
</style>
