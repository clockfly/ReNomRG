<template>
  <div id="regression">
    <div class="model-select">
      <div class="dashboard-and-detail">
        <dashboard></dashboard>
        <!-- <model-detail></model-detail> -->
      </div>
      <div class="model-list">
        <!-- <model-list></model-list> -->
      </div>
    </div>

    <!-- <div class="regression-result">
      <div class="regression-result-graph">
        <result></result>
      </div>
      <div class="regression-result-features">
        <result-feature></result-feature>
      </div>
    </div>

    <add-model-modal v-if="$store.state.add_model_modal_shown_flag"></add-model-modal> -->
  </div>
</template>

<script>
import AddModelModal from './add_model_modal.vue'
import Dashboard from './dashboard.vue'
import ModelDetail from './model_detail.vue'
import ModelList from './model_list.vue'
import Result from './result.vue'
import ResultFeature from './result_feature.vue'

export default {
  name: 'Regression',
  components: {
    'add-model-modal': AddModelModal,
    'dashboard': Dashboard,
    'model-detail': ModelDetail,
    'model-list': ModelList,
    'result': Result,
    'result-feature': ResultFeature
  },
  created: function () {
    // this.$store.dispatch('loadHeader')
    // this.$store.dispatch('loadModels')
  }
}
</script>

<style lang="scss" scoped>
#regression {
  display: flex;
  display: -webkit-flex;
  flex-direction: column;
  -webkit-flex-direction: column;

  width: 100%;

  .model-select {
    display: flex;
    display: -webkit-flex;
    height: 784px;

    .dashboard-and-detail {
      width: calc(100%);
      height: 100%;
    }
  //
  //   .model-list {
  //     width: $side-bar-width;
  //     height: 100%;
  //     margin-left: $side-bar-margin;
  //   }
  // }
  //
  // .regression-result {
  //   display: flex;
  //   display: -webkit-flex;
  //   height: $result-height;
  //   margin-bottom: 44px;
  //
  //   .regression-result-graph {
  //     width: calc(100% - #{$side-bar-width});
  //     height: 100%;
  //   }
  //
  //   .regression-result-features {
  //     width: $side-bar-width;
  //     height: 100%;
  //     margin-left: $side-bar-margin;
  //   }
  }

}
</style>
