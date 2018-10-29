<template>
  <div id="dashboard">
    <Panel
      :banner_text="'Dashboard'">
      <div slot="pannel_content">
        <DashboardRatioBar></DashboardRatioBar>
        <!-- <DashboardRunning></DashboardRunning> -->
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import DashboardRatioBar from '@/components/organisms/training/dashboard_ratio_bar'
import DashboardRunning from '@/components/organisms/training/dashboard_running'

export default {
  name: 'Dashboard',
  components: {
    Panel,
    DashboardRatioBar,
    DashboardRunning
  }
}
</script>

<style lang="scss" scoped>
#dashboard {
}
</style>
