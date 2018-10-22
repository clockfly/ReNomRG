<template>
  <div id="model-detail-random-forest">
    <value-item :label="'Algorithm'" :val="'RandomForest'"></value-item>
    <value-item :label="'Target'" :val="$store.state.header[target_column_id]"></value-item>
    <value-item :label="'Estimators'" :val="params.n_estimators"></value-item>
    <value-item :label="'Depth'" :val="params.max_depth"></value-item>
  </div>
</template>

<script>
import ModelDetailValueItem from './model_detail_value_item.vue'

export default {
  name: 'ModelDetailRandomForest',
  components: {
    'value-item': ModelDetailValueItem
  },
  props: {
    'params': {
      type: Object,
      required: true
    },
    'target_column_id': {
      type: Number,
      required: true
    }
  }
}
</script>

<style lang="scss" scoped>
#model-detail-random-forest {
}
</style>
