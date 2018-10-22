<template>
  <div id="prediction">
    <div class="model-detail-area">
      <model-detail></model-detail>
    </div>
    <div class="prediction-result-area">
      <!-- <prediction-result></prediction-result> -->
    </div>
  </div>
</template>

<script>
import ModelDetail from './model_detail'

export default {
  name: 'Prediction',
  components: {
    'model-detail': ModelDetail
  },
  created: function () {
    this.$store.dispatch('loadHeader')
    this.$store.dispatch('loadDeployedModel')
  }
}
</script>

<style lang="scss" scoped>
#prediction {
  display: flex;
  display: -webkit-flex;
  flex-direction: column;
  -webkit-flex-direction: column;

  width: 100%;
  padding-bottom: 64px;

  .model-detail-area {
    width: 100%;
  }

  .prediction-result-area {
    width: 100%;
  }
}
</style>
