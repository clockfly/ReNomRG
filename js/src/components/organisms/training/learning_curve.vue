<template>
  <div id="learning-curve">
    <Panel
      :banner_text="'Learning Curve'">
      <div slot="pannel_content">
        {{$store.state.valid_loss_list}}
        {{$store.state.train_loss_list}}
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
export default {
  name: 'LerningCurve',
  components: {
    Panel
  }
}
</script>

<style lang="scss" scoped>
#learning-curve {
}
</style>
