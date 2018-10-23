<template>
  <div id="prediction-result">
    <Panel
      :banner_text="'Prediction Sample'">
      <div slot="pannel_content">
        {{$store.state.selected_y_valid}}
        {{$store.state.selected_y_pred}}
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
export default {
  name: 'PreictionResult',
  components: {
    Panel
  }
}
</script>

<style lang="scss" scoped>
#prediction-result {
}
</style>
