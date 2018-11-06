<template>
  <div id="page">

    <div class="model-detail">
      <div class="start-button-area">
        <button class="start-button" @click="runPrediction">
          > Prediction Start
        </button>
      </div>

      <div class="panel model-detail-panel">
        <div class="panel-title">
          Model Detail
        </div>

        <div class="panel-content model-detail-content">
          <div v-if="deployed_model_id">
            <div class="label-value">
              <div class="label">Selected Model ID</div>
              <div class="value">{{deployed_model_id}}</div>
            </div>
            <div class="label-value">
              <div class="label">Dataset</div>
              <div class="value">{{deployed_model.dataset_id}}</div>
            </div>
            <div class="label-value">
              <div class="label">Algorithm</div>
              <div class="value">{{algorithms[deployed_model.algorithm]}}</div>
            </div>
            <div class="label-value">
              <div class="label">Total Epoch</div>
              <div class="value">{{deployed_model.epoch}}</div>
            </div>
            <div class="label-value">
              <div class="label">Batch Size</div>
              <div class="value">{{deployed_model.batch_size}}</div>
            </div>
            <div class="label-value">
              <div class="label">Validation Loss</div>
              <div class="value">{{round(deployed_model.best_epoch_valid_loss)}}</div>
            </div>
            <div class="label-value">
              <div class="label">RMSE</div>
              <div class="value">{{round(deployed_model.best_epoch_rmse)}}</div>
            </div>
            <div class="label-value">
              <div class="label">Max Absolute Error</div>
              <div class="value">{{round(deployed_model.best_epoch_max_abs_error)}}</div>
            </div>
            <div class="label-value">
              <div class="label">R2 Score</div>
              <div class="value">{{round(deployed_model.best_epoch_r2)}}</div>
            </div>

            <div class="label-value">
              <div class="label">Graph Comvolution Params</div>
            </div>

            <div class="label-value">
              <div class="label">Number of Neighbors</div>
              <div class="value">{{deployed_model.algorithm_params.num_neighbors}}</div>
            </div>
          </div>

          <div v-if="!deployed_model_id">Model is not Deployed.</div>
        </div>
      </div>
    </div> <!-- model detail -->

    <div class="prediction-results">
      <div class="panel">
        <div class="panel-title">
          Prediction Results
        </div>
        <div class="panel-content">
          results
        </div>
      </div>
    </div> <!-- prediction results -->

  </div>
</template>

<script>
import { mapState } from 'vuex'
import { round } from '@/utils'

export default {
  name: 'PredictionPage',
  computed: mapState(['algorithms', 'deployed_model_id', 'deployed_model', 'dataset_name_list']),
  created: function () {
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadModels')
  },
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    runPrediction: function () {
      this.$store.dispatch('runPrediction', { 'model_id': this.deployed_model_id })
    }
  }
}
</script>

<style lang="scss" scoped>
#page {
  @include prefix('display', 'flex');
  width: 100%;
  height: calc(100vh - 200px);

  .model-detail {
    width: 20%;
    .start-button-area {
      width: 100%;
      padding: 8px;
      .start-button {
        width: 100%;
      }
    }
    .model-detail-panel {
      height: calc(100% - 56px);
    }
    .model-detail-content {
      padding: 16px;
    }
    .label-value {
      @include prefix('display', 'flex');
      margin-bottom: 8px;
      font-size: $fs-small;
      .label {
        margin-right: 8px;
        color: $gray;
      }
    }
  }
  .prediction-results {
    width: 80%;
  }
}
</style>
