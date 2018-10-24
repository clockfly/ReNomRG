<template>
  <div id="prediction-result">
    <Panel
      :banner_text="'Prediction Sample'">
      <div slot="pannel_content">
        <ScatterPlot
          :w="500"
          :h="500"
          :x_values="$store.state.selected_y_valid"
          :y_values="$store.state.selected_y_pred"
          :r="0.1"></ScatterPlot>
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import ScatterPlot from '@/components/organisms/scatter_plot'

export default {
  name: 'PreictionResult',
  components: {
    Panel,
    ScatterPlot
  }
}
</script>

<style lang="scss" scoped>
#prediction-result {
}
</style>
