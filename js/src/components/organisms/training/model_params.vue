<template>
  <div id="model-params">
    <Panel
      :banner_text="'Model Detail'">
      <div slot="pannel_content">
        <LabelValueText
          :labeltext="'Model ID:'"
          :valuetext="$store.state.selected_model_id"></LabelValueText>
        <LabelValueText v-for="(item, index) in $store.state.selected_model"
          :key="index"
          :labeltext="index+':'"
          :valuetext="item"></LabelValueText>
      </div>
    </Panel>
  </div>
</template>

<script>
import LabelValueText from '@/components/molecules/label_value_text'
import Panel from '@/components/organisms/panel'

export default {
  name: 'ModelParams',
  components: {
    LabelValueText,
    Panel
  }
}
</script>

<style lang="scss" scoped>
#model-params {
}
</style>
