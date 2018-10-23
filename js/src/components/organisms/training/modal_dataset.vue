<template>
  <div class="modal-dataset">
    <InputTextWithLabel
      :labeltext="'dataset name:'"
      :value="name"
      @input="name = $event"></InputTextWithLabel>

    <InputTextWithLabel
      :labeltext="'description:'"
      :value="description"
      @input="description = $event"></InputTextWithLabel>

    <InputTextWithLabel
      :labeltext="'train ratio:'"
      :value="train_ratio"
      @input="train_ratio = parseFloat($event)"></InputTextWithLabel>

    <SelectBoxWithLabel
      :labeltext="'target column id:'"
      :options="$store.state.labels"
      :value="target_column_id"
      @input="target_column_id = parseInt($event)"></SelectBoxWithLabel>

    <Button :text="'Confirm'" @click="$emit('confirm', params())"></Button>
    <Button :text="'Save'" @click="$emit('save', params())"></Button>
    <Button :text="'Cancel'" @click="$emit('cancel')"></Button>
  </div>
</template>

<script>
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
      'target_column_id': 0
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
}
</style>
