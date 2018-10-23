<template>
  <div id="dashboard-running">
    <PlainText
      :text="'Running Models'"></PlainText>

    <div v-for="(model, index) in $store.state.running_models">
      {{model}}
    </div>
  </div>
</template>

<script>
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'DashboardRunning',
  components: {
    PlainText
  }
}
</script>

<style lang="scss" scoped>
#dashboard-running {
}
</style>
