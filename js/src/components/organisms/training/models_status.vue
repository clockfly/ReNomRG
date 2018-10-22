<template>
  <div id="models-status">
    <div class="content-left">
      <Dashboard></Dashboard>
    </div>
    <div class="content-right">
      <ModelMap></ModelMap>
    </div>
  </div>
</template>

<script>
import Dashboard from '@/components/organisms/training/dashboard.vue'
import ModelMap from '@/components/organisms/training/model_map.vue'

export default {
  name: 'ModelsStatus',
  components: {
    Dashboard,
    ModelMap
  }
}
</script>

<style lang="scss" scoped>
#models-status {
  @include prefix('display', 'flex');
  width: $full-parent-width;

  .content-left {
    width: $content-left-width;
  }
  .content-right {
    width: $content-right-width;
  }
}
</style>
