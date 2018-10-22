<template>
  <div id="model-map">
    <Panel
      :banner_text="'Model Map'">
      <div slot="pannel_content">
        map
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
export default {
  name: 'ModelMap',
  components: {
    Panel
  }
}
</script>

<style lang="scss" scoped>
#model-map {
}
</style>
