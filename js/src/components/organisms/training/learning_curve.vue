<template>
  <div id="learning-curve">
    <Panel
      :banner_text="'Learning Curve'">
      <div slot="pannel_content">
        curve
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
