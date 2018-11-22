<template>
  <div id="model-list">
    <div class="panel list-area">
      <div class="panel-title panel-title-button-area model-list-title">
        Model List
        <div class="panel-title-button" @click="showModal">
          <i class="fa fa-plus icon"></i>New
        </div>
      </div>

      <div class="model-list-item model-list-item-deployed"
        v-if="deployedModel"
        v-bind:class="{ active: deployedModel.model_id === $store.state.selected_model_id }"
        @click="selectModel(deployedModel)">
        <div :class="'algorithm-color '+$store.state.algorithms[deployedModel.algorithm].toLowerCase()"></div>

        <div class="label-value flex">
          <div class="label">Model ID</div>
          <div class="value">{{deployedModel.model_id}}</div>
        </div>

        <div class="label-value flex">
          <div class="label">Algorithm</div>
          <div class="value">{{$store.state.algorithms[deployedModel.algorithm]}}</div>
        </div>

        <div class="label-value flex">
          <div class="label">RMSE</div>
          <div class="value">{{round(deployedModel.best_epoch_rmse)}}</div>
        </div>

        <div class="label-value flex">
          <div class="label">Max Absolute Error</div>
          <div class="value">{{round(deployedModel.best_epoch_max_abs_error)}}</div>
        </div>

        <div class="label-value flex">
          <div class="label">Validation Loss</div>
          <div class="value">{{round(deployedModel.best_epoch_valid_loss)}}</div>
        </div>

        <div class="deployed">
          deployed
        </div>
      </div>

      <div class="model-list-scrollable-area">
        <div class="model-list-item"
          v-bind:class="{ active: model.model_id === $store.state.selected_model_id }"
          v-for="(model,index) in $store.state.model_list"
          v-if="model.deployed === 0"
          @click="selectModel(model)">
          <div :class="'algorithm-color '+$store.state.algorithms[model.algorithm].toLowerCase()"></div>

          <div class="label-value flex">
            <div class="label">Model ID</div>
            <div class="value">{{model.model_id}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">Algorithm</div>
            <div class="value">{{$store.state.algorithms[model.algorithm]}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">RMSE</div>
            <div class="value">{{round(model.best_epoch_rmse)}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">Max Absolute Error</div>
            <div class="value">{{round(model.best_epoch_max_abs_error)}}</div>
          </div>

          <div class="label-value flex">
            <div class="label">Validation Loss</div>
            <div class="value">{{round(model.best_epoch_valid_loss)}}</div>
          </div>

          <div class="delete-button" @click="delete_model=model">
            <i class="fa fa-times icon"></i>
          </div>
        </div>
      </div>
    </div>

    <ModalConfirm v-if='delete_model'
      @ok='deleteModel'
      @cancel='delete_model=undefined'>
      <div slot='contents'>
        Would you like to delete Model ID: {{delete_model.model_id}}?
      </div>
      <span slot="okbutton">
        <button class="button-ok" @click="deleteModel">
          Delete
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
  name: 'ModelList',
  components: {
    ModalConfirm
  },
  data: function () {
    return {
      'delete_model': undefined
    }
  },
  computed: mapGetters(['deployedModel']),
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    selectModel: function (m) {
      this.$store.commit('setSelectedModelId', {'model_id': m['model_id']})
    },
    showModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': true})
    },
    deleteModel: function () {
      if (this.delete_model) {
        this.$store.commit('setSelectedModelId', {'model_id': undefined})
        this.$store.dispatch('deleteAndUpdate', {'model_id': this.delete_model['model_id']})
        this.delete_model = undefined
      }
    }
  }
}
</script>

<style lang="scss" scoped>
#model-list {
  width: 100%;
  height: 100%;

  .list-area {
    position: sticky;
    top: $header-height;
    bottom: $footer-height;
    width: 100%;
    height: calc(100vh - #{$header-height});

    .model-list-title {
      width: calc(100% - #{$scroll-bar-width});
    }

    .model-list-scrollable-area {
      overflow-y: scroll;
      width: 100%;
      height: calc(100% - #{$panel-title-height} - #{$model-list-item-height} - 16px);
      margin-top: $margin-small;
    }
  }

  .model-list-item {
    position: relative;
    width: 100%;
    height: $model-list-item-height;
    margin-top: $margin-small;
    padding: $padding-middle;
    background: $white;

    .algorithm-color {
      position: absolute;
      top: 0;
      left: 0;
      width: 8px;
      height: 100%;
    }

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

    .delete-button, .deployed {
      position: absolute;
      right: $margin-small;
      bottom: $margin-small;
      font-size: $fs-small;
    }
    .delete-button {
      .icon {
        color: $gray;
        font-size: $fs-micro;
      }
      .icon:hover {
        color: $white;
      }
    }
    .deployed {
      color: $blue;
    }
  }
  .model-list-item:hover {
    background-color: $light-gray;
    cursor:pointer;
    .delete-button:hover {
      color: $white;
    }
  }
  .active {
    border: solid $border-width-regular $blue;
  }
  .model-list-item-deployed {
    width: calc(100% - #{$scroll-bar-width});
    border: $border-width-bold solid $blue;
  }
}
</style>
