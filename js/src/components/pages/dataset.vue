<template>
  <div id="page">
    <DatasetList></DatasetList>
  </div>
</template>

<script>
import DatasetList from '@/components/organisms/dataset/dataset_list'

export default {
  name: 'DatasetPage',
  components: {
    DatasetList
  },
  created: function () {
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadLabels')
  }
}
</script>

<style lang="scss" scoped>
#page {
  width: $full-parent-width;
  height: calc(#{$full-screen-height} - #{$header-height});
}
</style>
