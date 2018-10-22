<template>
  <div id="model-detail">
    <div class="title">
      Model Detail
    </div>

    <div class="information" v-if="!model">
      Please choose a model which you want to deploy from model list.
    </div>

    <div class="content">
      <div class="model-detail-area" v-if="model">
        <component :is="algorithm_components[model.algorithm]"
          :model="model"
          :params="model.params"
          :target_column_id="model.target_column_id">
        </component>
      </div>

      <div class="button-area">
        <run-prediction-button></run-prediction-button>
        <!-- <export-button></export-button> -->
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ModelDetailRandomForest from './model_detail_random_forest.vue'
import RunPredictionButton from './run_prediction_button'

export default {
  name: 'ModelDetail',
  components: {
    'model-detail-random-forest': ModelDetailRandomForest,
    'run-prediction-button': RunPredictionButton
  },
  data: function () {
    return {
      algorithm_components: ['model-detail-random-forest']
    }
  },
  computed: mapState({'model': 'deployed_model'})
}
</script>

<style lang="scss" scoped>
#model-detail {
  $component-margin-top: 32px;

  $model-detail-height: 150px;

  $border-width: 2px;
  $border-color: #006699;

  $title-height: 44px;
  $title-font-size: 15pt;
  $font-weight-medium: 500;

  $content-padding-top: 8px;
  $content-padding-bottom: 8px;
  $content-padding-horizontal: 16px;

  $content-bg-color: #ffffff;
  $content-border-color: #cccccc;

  width: 100%;
  height: $model-detail-height;
  margin: 0;
  margin-top: $component-margin-top;
  border-top: $border-width solid $border-color;

  .title {
    line-height: $title-height;
    font-size: $title-font-size;
    font-weight: $font-weight-medium;
  }

  .content {
    display: flex;
    display: -webkit-flex;

    width: 100%;
    height: calc(100% - #{$title-height});

    .model-detail-area {
      width: 84%;
      height: 100%;
      padding: $content-padding-top $content-padding-horizontal $content-padding-bottom;
      background-color: $content-bg-color;
      border: 1px solid $content-border-color;
      border-radius: 4px;
    }

    .button-area {
      display: flex;
      flex-direction: column;
      position: relative;

      width: 16%;
      height: 100%;
    }
  }
}
</style>
