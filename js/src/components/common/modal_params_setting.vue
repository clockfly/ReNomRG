<template>
  <div class="modal-params-setting">
    <div class="column">

      <div class="setting-block">
        <div class="setting-type">
          Dataset Setting
        </div>

        <div class="sub-block">
          <div class="label">Dataset Name</div>
          <div class="input-value">
            <select v-model="dataset_index">
              <option v-for="(dataset, index) in $store.state.dataset_list"
                :value="index" :key="index">
                {{ dataset.name }}
              </option>
            </select>
            <div class="to-setting-dataset" @click="$emit('todataset')">
              > Setting of Dataset
            </div>
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div class="setting-block">
        <div class="setting-type">
          Algorithm Setting
        </div>

        <div class="sub-block">
          <div class="label">CNN Architecture</div>
          <div class="input-value">
            <select v-model="algorithm">
              <option v-for="(algorithm, index) in algorithms"
                :value="index" :key="index">
                {{ algorithm }}
              </option>
            </select>
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div class="setting-block">
        <div class="setting-type">
          Training Loop Setting
        </div>

        <div class="sub-block">
          <div class="label">Batch Size</div>
          <div class="input-value">
            <input type="text" v-model="batch_size">
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block">
          <div class="label">Total Epoch</div>
          <div class="input-value">
            <input type="text" v-model="epoch">
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

    </div>  <!-- column -->

    <div class="column">
      <div class="setting-block">
        <div class="setting-type">
          Graph Comvolution Params
        </div>

        <div class="sub-block">
          <div class="label">Number of neighbors</div>
          <div class="input-value">
            <input type="text" v-model="algorithm_params['num_neighbors']">
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

    </div>  <!-- column -->

    <div class="button-area">
      <button @click="runModel">Run</button>
      <button class="button-cancel" @click="hideModal">Cancel</button>
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
        'num_neighbors': 5,
        'fc_unit': [100, 50],
        'channels': [10, 20, 20]
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
    },
    hideModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': false})
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-params-setting {
  @include prefix("display", "flex");
  width: 100%;
  height: calc(100% - #{$modal-tab-height});

  .column {
    position: relative;
    width: 50%;
  }
  .setting-block {
    margin-top: 24px;
    margin-left: 24px;
  }
  .sub-block {
    @include prefix("display", "flex");
    margin-top: 16px;
    margin-left: 16px;

    .label, .input-value {
      width: 50%;
    }
  }
  .setting-type, .label {
    color: $gray;
  }

  .to-setting-dataset {
    font-size: $fs-small;
    color: $blue;
  }

  .button-area {
    position: absolute;
    bottom: $modal-content-padding;
    right: $modal-content-padding;
  }
}
</style>
