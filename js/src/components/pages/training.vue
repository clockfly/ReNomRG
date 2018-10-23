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
            <ModelParams></ModelParams>
          </div>
          <div class="content-right">
            <LearningCurve></LearningCurve>
          </div>
        </div>

        <PredictionResult></PredictionResult>
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
import Dashboard from '@/components/organisms/training/dashboard.vue'
import Features from '@/components/organisms/training/features'
import LearningCurve from '@/components/organisms/training/learning_curve.vue'
import ModalAdd from '@/components/organisms/training/modal_add'
import ModelList from '@/components/organisms/training/model_list'
import ModelMap from '@/components/organisms/training/model_map.vue'
import ModelParams from '@/components/organisms/training/model_params.vue'
import PredictionResult from '@/components/organisms/training/prediction_result'

export default {
  name: 'TrainingPage',
  components: {
    Dashboard,
    Features,
    LearningCurve,
    ModalAdd,
    ModelList,
    ModelMap,
    ModelParams,
    PredictionResult
  },
  created: function () {
    this.$store.dispatch('loadLabels')
  }
}
</script>

<style lang="scss" scoped>
#page {
  width: $full-parent-width;

  .training {
    @include prefix('display', 'flex');
    width: $full-parent-width;

    .content {
      width: $content-width;

      .content-columns {
        @include prefix('display', 'flex');
        width: $full-parent-width;

        .content-left {
          width: $content-left-width;
        }
        .content-right {
          width: $content-right-width;
        }
      }
    }
    .list {
      width: $list-width;
    }
  }
}
</style>
