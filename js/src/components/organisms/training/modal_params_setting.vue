<template>
  <div class="modal-params-setting">
    <SelectBoxWithLabel
      :labeltext="'target column id:'"
      :options="$store.state.dataset_list"
      @change="dataset_id = $event"></SelectBoxWithLabel>

    <Button :text="'Run'" @click="$emit('run', params())"></Button>
    <Button :text="'Cancel'" @click="$emit('cancel')"></Button>
  </div>
</template>

<script>
import Button from '@/components/atoms/button.vue'
import InputTextWithLabel from '@/components/molecules/input_text_with_label'
import SelectBoxWithLabel from '@/components/molecules/select_box_with_label'

export default {
  name: 'ModalParamsSetting',
  components: {
    Button,
    InputTextWithLabel,
    SelectBoxWithLabel
  },
  data: function () {
    return {
      'dataset_id': 1,
      'algorithm': 0,
      'algorithm_params': {
        'num_neighbors': 5
      },
      'batch_size': 16,
      'epoch': 10
    }
  },
  methods: {
    params: function () {
      return {
        'dataset_id': this.dataset_id,
        'algorithm': this.algorithm,
        'algorithm_params': {
          'num_neighbors': 5
        },
        'batch_size': this.batch_size,
        'epoch': this.epoch
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-params-setting {
}
</style>
