<template>
  <div id="model-map">
    <Panel
      :banner_text="'Model Map'">
      <div slot="pannel_content">
        <ChartScatter
          :w="300"
          :h="300"
          :x_values="mapValues.x_values"
          :y_values="mapValues.y_values"
          :r="5"></ChartScatter>
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import ChartScatter from '@/components/organisms/chart_scatter'

export default {
  name: 'ModelMap',
  components: {
    Panel,
    ChartScatter
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
