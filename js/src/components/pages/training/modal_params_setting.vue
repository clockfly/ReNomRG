<template>
  <div class="modal-params-setting">

    <div class="input-with-label">
      <div class="label">dataset id: </div>
      <select v-model="dataset_index">
        <option v-for="(name, index) in $store.state.dataset_name_list"
          :value="index" :key="index">
          {{ name }}
        </option>
      </select>
    </div>

    <div class="input-with-label">
      <div class="label">algorithm: </div>
      <select v-model="algorithm">
        <option v-for="(algorithm, index) in algorithms"
          :value="index" :key="index">
          {{ algorithm }}
        </option>
      </select>
    </div>

    <div class="input-with-label">
      <div class="label">batch size: </div>
      <input type="text" v-model="batch_size">
    </div>

    <div class="input-with-label">
      <div class="label">epoch: </div>
      <input type="text" v-model="epoch">
    </div>

    <div class="input-with-label">
      <div class="label">neighbors: </div>
      <input type="text" v-model="algorithm_params['num_neighbors']">
    </div>

    <div class="button-area">
      <button @click="runModel">Run</button>
      <button class="button-cancel" @click="$emit('cancel')">Cancel</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalParamsSetting',
  data: function () {
    return {
      'algorithms': ['C-GCNN', 'Kernel-GCNN', 'DBSCAN-GCNN'],
      'dataset_index': 0,
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
        'dataset_index': this.dataset_index,
        'algorithm': this.algorithm,
        'algorithm_params': this.algorithm_params,
        'batch_size': this.batch_size,
        'epoch': this.epoch
      }
    },
    runModel: function () {
      this.$store.dispatch('addModel', this.params())
      this.hideModal()
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-params-setting {
  .input-with-label {
    @include prefix("display", "flex");
    .label {
      color: $gray;
    }
  }

  .button-area {
    position: absolute;
    bottom: 16px;
    right: 16px;
  }
}
</style>
