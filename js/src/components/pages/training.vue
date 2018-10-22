<template>
  <div id="training">
    <div id="content">
      <ModelsStatus></ModelsStatus>
      <ModelDetail></ModelDetail>
      <PredictionResult></PredictionResult>
      <Features></Features>
    </div>
    <div id="list">
      <ModelList></ModelList>
    </div>
  </div>
</template>

<script>
import Features from '@/components/organisms/training/features.vue'
import ModelDetail from '@/components/organisms/training/model_detail.vue'
import ModelList from '@/components/organisms/training/model_list.vue'
import ModelsStatus from '@/components/organisms/training/models_status.vue'
import PredictionResult from '@/components/organisms/training/prediction_result.vue'

export default {
  name: 'TrainingPage',
  components: {
    Features,
    ModelDetail,
    ModelList,
    ModelsStatus,
    PredictionResult
  }
}
</script>

<style lang="scss" scoped>
#training {
  @include prefix('display', 'flex');
  width: $full-parent-width;

  #content {
    width: $content-width;
  }
  #list {
    width: $list-width;
  }
}
</style>
