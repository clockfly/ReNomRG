<template>
  <div class="modal-params-setting">
    <SelectBoxWithLabel
      :labeltext="'target column id:'"
      :options="$store.state.dataset_name_list"
      @change="dataset_id = $event"></SelectBoxWithLabel>

    <SelectBoxWithLabel
      :labeltext="'algorithm:'"
      :options="['C-GCNN', 'Kernel-GCNN', 'DBSCAN-GCNN']"
      @change="algorithm = $event"></SelectBoxWithLabel>

    <InputTextWithLabel
      :labeltext="'batch size:'"
      @change="batch_size = parseInt($event)"></InputTextWithLabel>

    <InputTextWithLabel
      :labeltext="'epoch:'"
      @change="epoch = parseInt($event)"></InputTextWithLabel>

    <InputTextWithLabel
      :labeltext="'neighbors:'"
      @change="algorithm_params['num_neighbors'] = parseInt($event)"></InputTextWithLabel>

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
        'algorithm_params': this.algorithm_params,
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
