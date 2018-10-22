<template>
  <div id="model-detail">
    <div class="title">
      Model Detail
    </div>

    <div class="content">
      <div class="content-text" v-if="model">
        <div class="model-id">
          Model ID {{model.model_id}}
        </div>
        <component :is="algorithm_components[model.algorithm]"
          :params="model.params"
          :target_column_id="model.target_column_id">
        </component>

        <model-deploy-button v-if="model.deployed === 0" :model_id="model.model_id"></model-deploy-button>
        <model-undeploy-button v-if="model.deployed === 1" :model_id="model.model_id"></model-undeploy-button>
      </div>

      <div class="content-graph"></div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ModelDetailRandomForest from './model_detail_random_forest.vue'
import ModelDeployButton from './model_deploy_button.vue'
import ModelUndeployButton from './model_undeploy_button.vue'

export default {
  name: 'ModelDetail',
  components: {
    'model-detail-random-forest': ModelDetailRandomForest,
    'model-deploy-button': ModelDeployButton,
    'model-undeploy-button': ModelUndeployButton
  },
  data: function () {
    return {
      algorithm_components: ['model-detail-random-forest']
    }
  },
  computed: mapState({'model': 'selected_model'})
}
</script>

<style lang="scss" scoped>
#model-detail {
  $component-margin-top: 32px;

  $model-detail-height: 360px;

  $border-width: 2px;
  $border-color: #006699;

  $title-height: 44px;
  $title-font-size: 15pt;
  $font-weight-medium: 500;

  $subtitle-height: 24px;
  $subtitle-font-size: 16px;

  $content-padding-top: 24px;
  $content-padding-horizontal: 24px;
  $content-padding-bottom: 16px;

  $content-bg-color: #ffffff;
  $content-border-color: #cccccc;

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

    height: calc(100% - #{$title-height});
    padding: $content-padding-top $content-padding-horizontal $content-padding-bottom;

    background-color: $content-bg-color;
    border: 1px solid $content-border-color;
    border-radius: 4px;

    .content-text {
      display: flex;
      display: -webkit-flex;
      flex-direction: column;
      -webkit-flex-direction: column;

      width: 50%;

      .model-id {
        line-height: $subtitle-height;
        font-size: $subtitle-font-size;
        font-weight: $font-weight-medium;
        border-bottom: 1px solid #ccc;
      }
    }

    .content-graph {}
  }
}
</style>
