<template>
  <div id="model-map">
    <Panel
      :banner_text="'Model Map'">
      <div slot="pannel_content">
        <div v-for="(m, index) in $store.state.model_list">
          {{m['best_epoch_rmse']}},{{m['best_epoch_max_abs_error']}}
        </div>
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
