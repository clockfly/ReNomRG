<template>
  <div id="page">

  </div>
</template>

<script>
export default {
  name: 'DatasetPage',
  created: function () {
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadLabels')
  }
}
</script>

<style lang="scss" scoped>
#page {
  width: 100%;
  height: calc(#{$full-screen-height} - #{$header-height});
}
</style>
