<template>
  <div class="modal-dataset">
    <Button :text="'Confirm'" @click="confirm"></Button>
    <Button :text="'Save'" @click="save"></Button>
    <Button :text="'Cancel'" @click="cancel"></Button>
  </div>
</template>

<script>
import Button from '@/components/atoms/button.vue'

export default {
  name: 'ModalDataset',
  components: {
    Button
  },
  methods: {
    cancel: function () {
      this.$emit('cancel')
    },
    confirm: function () {
      let params = {
        'name': 'test',
        'description': 'hoge',
        'train_ratio': 0.8,
        'target_column_id': 13
      }
      this.$emit('confirm', params)
    },
    save: function () {
      let params = {
        'name': 'test',
        'description': 'hoge',
        'train_ratio': 0.8,
        'target_column_id': 13
      }
      this.$emit('save', params)
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-dataset {
}
</style>
