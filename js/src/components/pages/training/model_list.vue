<template>
  <div id="model-list">
    <div class="add-button-area">
      <button class="add-button" @click="showModal">
        <i class="fa fa-plus icon" aria-hidden="true"></i>
        Add new model
      </button>
    </div>

    <div class="panel list-area">
      <div class="panel-title">Model List</div>

      <div class="model-list-item"
        v-for="(model,index) in $store.state.model_list"
        @click="selectModel(model)">

        <div class="label-value">
          <div class="label">Model ID:</div>
          <div class="value">{{model.model_id}}</div>
        </div>

        <div class="label-value">
          <div class="label">Algorithm:</div>
          <div class="value">{{model.algorithm}}</div>
        </div>

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
      </div>
    </div>
  </div>
</template>

<script>
import { round } from '@/utils'

export default {
  name: 'ModelList',
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    selectModel: function (m) {
      this.$store.commit('setSelectedModelId', {'model_id': m['model_id']})
      this.$store.dispatch('loadModel', {'model_id': m['model_id']})
    },
    showModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': true})
    }
  },
  created: function () {
    this.$store.dispatch('loadModels')
  }
}
</script>

<style lang="scss" scoped>
#model-list {
  .add-button-area, .list-area {
    padding: 8px;
  }
  .add-button {
    width: 100%;
    .icon {
      color: $white;
    }
  }

  .model-list-item {
    margin-top: 8px;
    background: $white;

    .label-value {
      @include prefix('display', 'flex');
      .label {
        color: $gray;
      }
    }
  }
}
</style>