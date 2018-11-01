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

      <div class="model-list-scrollable-area">
        <div class="model-list-item"
          v-bind:class="{ active: model.model_id === $store.state.selected_model_id }"
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

          <div v-if="model.deployed === 1" class="deployed">
            deployed
          </div>
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
      this.$store.dispatch('selectModel', {'model_id': m['model_id']})
    },
    showModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': true})
    }
  }
}
</script>

<style lang="scss" scoped>
#model-list {
  width: 100%;
  height: 100%;

  .add-button-area, .list-area {
    padding: 8px;
  }
  .add-button {
    width: 100%;
    .icon {
      color: $white;
    }
  }

  .list-area {
    width: 100%;
    height: calc(100% - 100px);
    .model-list-scrollable-area {
      overflow: scroll;
      width: 100%;
      height: 100%;
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
  .model-list-item:hover {
    background-color: #CCCCCC;
    cursor:pointer;
  }
  .active {
    border: solid 1px $blue;
  }
}
</style>
