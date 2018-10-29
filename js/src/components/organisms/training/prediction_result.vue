<template>
  <div id="prediction-result">
    <Panel
      :banner_text="'Prediction Sample'">
      <div slot="pannel_content">
        <ChartScatter
          :w="500"
          :h="500"
          :x_values="$store.state.selected_y_valid"
          :y_values="$store.state.selected_y_pred"
          :r="5"></ChartScatter>
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import ChartScatter from '@/components/organisms/chart_scatter'

export default {
  name: 'PreictionResult',
  components: {
    Panel,
    ChartScatter
  }
}
</script>

<style lang="scss" scoped>
#prediction-result {
}
</style>
