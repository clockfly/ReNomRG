<template>
  <div id="dashboard">
    <Panel
      :banner_text="'Dashboard'">
      <div slot="pannel_content">
        <ModelRatioBar></ModelRatioBar>
        <RunningModels></RunningModels>
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import ModelRatioBar from '@/components/organisms/training/model_ratio_bar'
import RunningModels from '@/components/organisms/training/running_models'

export default {
  name: 'Dashboard',
  components: {
    Panel,
    ModelRatioBar,
    RunningModels
  }
}
</script>

<style lang="scss" scoped>
#dashboard {
}
</style>
