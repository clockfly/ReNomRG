<template>
  <div class="modal-dataset padding-bottom-16">
    <div class="column">
      <InputTextWithLabel
        class="margin-bottom-8"
        :labeltext="'dataset name:'"
        :labelwidth="label_width"
        :value="name"
        @input="name = $event"></InputTextWithLabel>

      <InputTextWithLabel
        class="margin-bottom-8"
        :labeltext="'description:'"
        :labelwidth="label_width"
        :value="description"
        @input="description = $event"></InputTextWithLabel>

      <InputTextWithLabel
        class="margin-bottom-8"
        :labeltext="'train ratio:'"
        :labelwidth="label_width"
        :value="train_ratio"
        @input="train_ratio = parseFloat($event)"></InputTextWithLabel>

      <SelectBoxWithLabel
        class="margin-bottom-8"
        :labeltext="'target columns:'"
        :labelwidth="label_width"
        :options="$store.state.labels"
        :value="target_column_id"
        @input="target_column_id = parseInt($event)"></SelectBoxWithLabel>

      <div class="button-area">
        <Button :text="'Confirm'" @click="$emit('confirm', params())"></Button>
      </div>
    </div>

    <div class="column">
      <div class="button-area">
        <Button :text="'Save'" @click="$emit('save', params())"></Button>
        <Button :text="'Cancel'"
          :bordercolor="gray"
          :backgroundcolor="white"
          :textcolor="gray"
          @click="$emit('cancel')"></Button>
      </div>
    </div>
  </div>
</template>

<script>
import { GRAY, WHITE } from '@/const'
import Button from '@/components/atoms/button'
import InputTextWithLabel from '@/components/molecules/input_text_with_label'
import SelectBoxWithLabel from '@/components/molecules/select_box_with_label'

export default {
  name: 'ModalDataset',
  components: {
    Button,
    InputTextWithLabel,
    SelectBoxWithLabel
  },
  data: function () {
    return {
      'name': '',
      'description': '',
      'train_ratio': 0.8,
      'target_column_id': 0,
      'gray': GRAY,
      'white': WHITE,
      'label_width': '160px'
    }
  },
  methods: {
    params: function () {
      return {
        'name': this.name,
        'description': this.description,
        'train_ratio': this.train_ratio,
        'target_column_id': this.target_column_id
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-dataset {
  @include prefix("display", "flex");
  width: 100%;
  height: 100%;

  .column {
    position: relative;
    width: 50%;
    height: 100%;
    .button-area {
      position: absolute;
      bottom: 0;
      right: 0;
    }
  }
}
</style>
