<template>
  <div id="model-params">
    <div class="panel">
      <div class="panel-title panel-title-button-area">
        Model Detail
        <div class="panel-title-button" v-if="selectedModel && selectedModel.deployed === 0" @click="deploy">
          > Deploy Model
        </div>
        <div class="panel-title-button" v-if="selectedModel && selectedModel.deployed === 1" @click="show_confirm_modal=true">
          > Undeploy Model
        </div>
      </div>

      <div class="panel-content detail flex">
        <div class="column">
          <div class="label-value flex">
            <div class="label">Model ID</div>
            <div class="value" v-if="selectedModel">{{selectedModel.model_id}}</div>
          </div>
        </div>

        <div class="column" v-if="selectedModel">
          <div class="label-value flex">
            <div class="label">Algorithm</div>
            <div class="value">{{$store.state.algorithms[selectedModel.algorithm]}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">Total Epoch</div>
            <div class="value">{{selectedModel.epoch}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">Batch Size</div>
            <div class="value">{{selectedModel.batch_size}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">Validation Loss</div>
            <div class="value">{{round(selectedModel.best_epoch_valid_loss)}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">RMSE</div>
            <div class="value">{{round(selectedModel.best_epoch_rmse)}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">Max Absolute Error</div>
            <div class="value">{{round(selectedModel.best_epoch_max_abs_error)}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">R2 Score</div>
            <div class="value">{{round(selectedModel.best_epoch_r2)}}</div>
          </div>
        </div>

        <div class="column" v-if="selectedModel">
          <div class="label-value">
            <div class="label">Graph Comvolution Params</div>
          </div>

          <div class="label-value flex">
            <div class="label">Number of Neighbors</div>
            <div class="value">{{selectedModel.algorithm_params.num_neighbors}}</div>
          </div>
        </div>

      </div>
    </div>

    <ModalConfirm v-if='show_confirm_modal'
      @ok='undeploy'
      @cancel='show_confirm_modal=false'>
      <div slot='contents'>
        Would you like to undeploy Model ID: {{selectedModel.model_id}}?
      </div>
      <span slot="okbutton">
        <button class="button-ok" @click="undeploy">
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
      'show_confirm_modal': false
    }
  },
  computed: mapGetters(['selectedModel']),
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
        margin-bottom: $margin-small;
        .label, .value {
          font-size: $fs-small;
        }
        .label {
          margin-right: $margin-small;
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
