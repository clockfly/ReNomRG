<template>
  <div id="learning-curve">
    <Panel
      :banner_text="'Learning Curve'">
      <div slot="pannel_content">
        <ChartLine
          :w="300" :h="300"
          :line_values="[$store.state.valid_loss_list,$store.state.train_loss_list]">
        </ChartLine>
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import ChartLine from '@/components/organisms/chart_line'

export default {
  name: 'LerningCurve',
  components: {
    Panel,
    ChartLine
  }
}
</script>

<style lang="scss" scoped>
#learning-curve {
}
</style>
