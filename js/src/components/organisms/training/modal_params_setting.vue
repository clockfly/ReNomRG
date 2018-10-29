<template>
  <div class="modal-params-setting">
    <SelectBoxWithLabel
      class="margin-bottom-8"
      :labeltext="'dataset id:'"
      :labelwidth="label_width"
      :options="$store.state.dataset_name_list"
      :value="dataset_index"
      @input="dataset_index = $event"></SelectBoxWithLabel>

    <SelectBoxWithLabel
      class="margin-bottom-8"
      :labeltext="'algorithm:'"
      :labelwidth="label_width"
      :options="['C-GCNN', 'Kernel-GCNN', 'DBSCAN-GCNN']"
      :value="algorithm"
      @input="algorithm = parseInt($event)"></SelectBoxWithLabel>

    <InputTextWithLabel
      class="margin-bottom-8"
      :labeltext="'batch size:'"
      :labelwidth="label_width"
      :value="batch_size"
      @input="batch_size = parseInt($event)"></InputTextWithLabel>

    <InputTextWithLabel
      class="margin-bottom-8"
      :labeltext="'epoch:'"
      :labelwidth="label_width"
      :value="epoch"
      @input="epoch = parseInt($event)"></InputTextWithLabel>

    <InputTextWithLabel
      class="margin-bottom-8"
      :labeltext="'neighbors:'"
      :labelwidth="label_width"
      :value="algorithm_params['num_neighbors']"
      @input="algorithm_params['num_neighbors'] = parseInt($event)"></InputTextWithLabel>

    <div class="button-area">
      <Button :text="'Run'" @click="$emit('run', params())"></Button>
      <Button :text="'Cancel'"
        :bordercolor="gray"
        :backgroundcolor="white"
        :textcolor="gray"
        @click="$emit('cancel')"></Button>
    </div>
  </div>
</template>

<script>
import { GRAY, WHITE } from '@/const'
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
      'dataset_index': 0,
      'algorithm': 0,
      'algorithm_params': {
        'num_neighbors': 5
      },
      'batch_size': 16,
      'epoch': 10,
      'gray': GRAY,
      'white': WHITE,
      'label_width': '120px'
    }
  },
  methods: {
    params: function () {
      return {
        'dataset_index': this.dataset_index,
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
  .button-area {
    position: absolute;
    bottom: 16px;
    right: 16px;
  }
}
</style>
