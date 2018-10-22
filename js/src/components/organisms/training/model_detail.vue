<template>
  <div id="model-detail">
    <div class="content-left">
      <ModelParams></ModelParams>
    </div>
    <div class="content-right">
      <LearningCurve></LearningCurve>
    </div>
  </div>
</template>

<script>
import LearningCurve from '@/components/organisms/training/learning_curve.vue'
import ModelParams from '@/components/organisms/training/model_params.vue'

export default {
  name: 'ModelDetail',
  components: {
    LearningCurve,
    ModelParams
  }
}
</script>

<style lang="scss" scoped>
#model-detail {
  @include prefix('display', 'flex');
  width: $full-parent-width;

  .content-left {
    width: $content-left-width;
  }
  .content-right {
    width: $content-right-width;
  }
}
</style>
