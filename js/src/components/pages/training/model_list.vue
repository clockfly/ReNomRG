/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="model-list">
    <div class="panel list-area">
      <div class="panel-title panel-title-button-area model-list-title">
        Model List
        <div
          class="panel-title-button"
          @click="showModal"
        >
          <i class="fa fa-plus icon" />New
        </div>
      </div>

      <div
        v-if="deployedModel"
        class="model-list-item model-list-item-deployed"
        :class="{ active: deployedModel.model_id === $store.state.selected_model_id }"
        @click="selectModel(deployedModel)"
      >
        <div :class="'algorithm-color '+$store.state.algorithms[deployedModel.algorithm].toLowerCase()" />

        <div class="label-value flex">
          <div class="label">
            Model ID
          </div>
          <div class="value">
            {{ deployedModel.model_id }}
          </div>
        </div>

        <div class="label-value flex">
          <div class="label">
            Algorithm
          </div>
          <div class="value">
            {{ $store.state.algorithms[deployedModel.algorithm] }}
          </div>
        </div>

        <div class="label-value flex">
          <div class="label">
            RMSE
          </div>
          <div class="value">
            {{ round(deployedModel.best_epoch_rmse) }}
          </div>
        </div>

        <div class="label-value flex">
          <div class="label">
            Max Absolute Error
          </div>
          <div class="value">
            {{ round(deployedModel.best_epoch_max_abs_error) }}
          </div>
        </div>

        <div class="label-value flex">
          <div class="label">
            Validation Loss
          </div>
          <div class="value">
            {{ round(deployedModel.best_epoch_valid_loss) }}
          </div>
        </div>

        <div class="deployed">
          deployed
        </div>
      </div>

      <div :class="{ 'model-list-scrollable-area': deployed_flg, 'model-list-scrollable-area-un': !deployed_flg }">
        <div
          v-for="(model,index) in undeployed_models"
          :key="index"
          class="model-list-item"
          :class="{ active: model.model_id === $store.state.selected_model_id }"
          @click="selectModel(model)"
        >
          <div :class="'algorithm-color '+$store.state.algorithms[model.algorithm].toLowerCase()" />

          <div class="label-value flex">
            <div class="label">
              Model ID
            </div>
            <div class="value">
              {{ model.model_id }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              Algorithm
            </div>
            <div class="value">
              {{ $store.state.algorithms[model.algorithm] }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              RMSE
            </div>
            <div class="value">
              {{ round(model.best_epoch_rmse) }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              Max Absolute Error
            </div>
            <div class="value">
              {{ round(model.best_epoch_max_abs_error) }}
            </div>
          </div>

          <div class="label-value flex">
            <div class="label">
              Validation Loss
            </div>
            <div class="value">
              {{ round(model.best_epoch_valid_loss) }}
            </div>
          </div>

          <div
            class="delete-button"
            @click="delete_model=model"
          >
            <i class="fa fa-times icon" />
          </div>
        </div>
      </div>
    </div>

    <ModalConfirm
      v-if="delete_model"
      @ok="deleteModel"
      @cancel="delete_model=undefined"
    >
      <div slot="contents">
        Would you like to delete Model ID: {{ delete_model.model_id }}?
      </div>
      <span slot="okbutton">
        <button
          class="button-ok"
          @click="deleteModel"
        >
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
      'delete_model': undefined,
      'deployed_flg': false
    }
  },
  computed: {
    ...mapGetters(['deployedModel']),
    undeployed_models: function () {
      const filtered = this.$store.state.model_list.filter(function (element, index, array) {
        return element.deployed === 0
      })
      return filtered
    }
  },
  updated: function () {
    if (this.deployedModel) {
      this.deployed_flg = true
    } else {
      this.deployed_flg = false
    }
  },
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
    .model-list-scrollable-area-un {
      overflow-y: scroll;
      width: 100%;
      height: calc(100% - #{$panel-title-height} - 16px);
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
