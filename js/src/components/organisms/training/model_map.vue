<template>
  <div id="model-map">
    <Panel
      :banner_text="'Model Map'">
      <div slot="pannel_content">
        <ScatterPlot
          :w="300"
          :h="300"
          :x_values="mapValues.x_values"
          :y_values="mapValues.y_values"
          :r="0.1"></ScatterPlot>
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import ScatterPlot from '@/components/organisms/scatter_plot'

export default {
  name: 'ModelMap',
  components: {
    Panel,
    ScatterPlot
  },
  computed: {
    mapValues: function () {
      let x_values = []
      let y_values = []
      for (let m of this.$store.state.model_list) {
        x_values.push(m['best_epoch_rmse'])
        y_values.push(m['best_epoch_max_abs_error'])
      }
      return {
        'x_values': x_values,
        'y_values': y_values
      }
    }
  }
}
</script>

<style lang="scss" scoped>
#model-map {
}
</style>
