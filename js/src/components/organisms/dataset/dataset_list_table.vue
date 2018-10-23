<template>
  <div class="dataset-list-table">
    <div v-for="(dataset, index) in $store.state.dataset_list"
      @click="selectDataset(dataset)">
      {{dataset}}
    </div>
  </div>
</template>

<script>
export default {
  name: 'DatasetListTable',
  methods: {
    selectDataset: function (d) {
      this.$store.commit('setSelectedDatasetId', {'dataset_id': d['dataset_id']})
      this.$store.dispatch('loadSelectedDataset', {'dataset_id': d['dataset_id']})
    }
  }
}
</script>

<style lang="scss" scoped>
.dataset-list-table {
}
</style>
