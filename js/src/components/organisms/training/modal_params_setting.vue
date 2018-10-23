<template>
  <div class="modal-params-setting">
    params
    <Button :text="'Run'" @click="run"></Button>
    <Button :text="'Cancel'" @click="cancel"></Button>
  </div>
</template>

<script>
import Button from '@/components/atoms/button.vue'

export default {
  name: 'ModalParamsSetting',
  components: {
    Button
  },
  methods: {
    cancel: function () {
      this.$emit('cancel')
    },
    run: function () {
      let params = {
        'dataset_id': 1,
        'algorithm': 1,
        'algorithm_params': {
          'num_neighbors': 5
        },
        'batch_size': 32,
        'epoch': 10
      }
      this.$emit('run', params)
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-params-setting {
}
</style>
