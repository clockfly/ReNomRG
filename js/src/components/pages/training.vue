<template>
  <div id="page">
    <div class="training">

      <div class="content">
        <div class="content-columns">
          <div class="content-left">
            <Dashboard></Dashboard>
          </div>
          <div class="content-right">
            <ModelMap></ModelMap>
          </div>
        </div>

        <div class="content-columns">
          <div class="content-left">
            <ModelDetail></ModelDetail>
          </div>
          <div class="content-right">
            <LearningCurve></LearningCurve>
          </div>
        </div>

        <PredictionSample></PredictionSample>
        <Features></Features>
      </div>

      <div class="list">
        <ModelList></ModelList>
      </div>
    </div>

    <ModalAdd v-if="$store.state.add_model_modal_shown_flag"></ModalAdd>
  </div>
</template>

<script>
import Dashboard from '@/components/pages/training/dashboard.vue'
import Features from '@/components/pages/training/features'
import LearningCurve from '@/components/pages/training/learning_curve.vue'
import ModalAdd from '@/components/pages/training/modal_add'
import ModelDetail from '@/components/pages/training/model_detail.vue'
import ModelList from '@/components/pages/training/model_list'
import ModelMap from '@/components/pages/training/model_map.vue'
import PredictionSample from '@/components/pages/training/prediction_sample'

export default {
  name: 'TrainingPage',
  components: {
    Dashboard,
    Features,
    LearningCurve,
    ModalAdd,
    ModelDetail,
    ModelList,
    ModelMap,
    PredictionSample
  },
  created: function () {
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadLabels')
  }
}
</script>

<style lang="scss" scoped>
#page {
  width: 100%;
  height: 100%;

  .training {
    @include prefix('display', 'flex');
    position: relative;
    width: 100%;
    height: 100%;

    .content {
      width: $content-width;
      height: 100%;
      height: 100%;

      .content-columns {
        @include prefix('display', 'flex');
        width: 100%;

        .content-left {
          width: $content-left-width;
        }
        .content-right {
          width: $content-right-width;
        }
      }
    }
    .list {
      position: absolute;
      right: 0px;
      top: 0px;
      width: #{$list-width};
      height: 100%;
    }
  }
}
</style>
