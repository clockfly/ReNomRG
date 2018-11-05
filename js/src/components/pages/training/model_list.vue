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

          <div :class="'algorithm-color '+$store.state.algorithms[model.algorithm].toLowerCase()"></div>

          <div class="label-value">
            <div class="label">Model ID</div>
            <div class="value">{{model.model_id}}</div>
          </div>

          <div class="label-value">
            <div class="label">Algorithm</div>
            <div class="value">{{$store.state.algorithms[model.algorithm]}}</div>
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
            <div class="label">Validation Loss</div>
            <div class="value">{{round(model.best_epoch_valid_loss)}}</div>
          </div>

          <div v-if="model.deployed === 0" class="delete-button" @click="deleteModel(model)">
            <i class="fa fa-times" aria-hidden="true"></i>
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
    },
    deleteModel: function (m) {
      alert('削除　未実装')
      // this.$store.dispatch('deleteModel', {'model_id': m['model_id']})
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
    position: relative;
    width: 100%;
    height: $model-list-item-height;
    margin-top: 8px;
    padding: 8px 8px 8px 16px;
    background: $white;

    .algorithm-color {
      position: absolute;
      top: 0;
      left: 0;
      width: 8px;
      height: 100%;
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

    .delete-button, .deployed {
      position: absolute;
      right: 8px;
      bottom: 8px;
      font-size: $fs-small;
    }
    .delete-button {
      color: $gray;
    }
    .deployed {
      color: $blue;
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
