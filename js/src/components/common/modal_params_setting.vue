<template>
  <div class="modal-params-setting flex">
    <div class="column">
      <div class="setting-block">
        <div class="setting-type">
          Dataset Setting
        </div>

        <div class="sub-block flex">
          <div class="label">
            Dataset Name
          </div>
          <div class="input-value">
            <select v-model="dataset_index">
              <option
                v-for="(dataset, index) in $store.state.dataset_list"
                :key="index"
                :value="index"
              >
                {{ dataset.name }}
              </option>
            </select>
            <div
              class="to-setting-dataset"
              @click="$emit('todataset')"
            >
              > Setting of Dataset
            </div>
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div class="setting-block">
        <div class="setting-type">
          Algorithm Setting
        </div>

        <div class="sub-block flex">
          <div class="label">
            Architecture
          </div>
          <div class="input-value">
            <select v-model="algorithm">
              <option
                v-for="(a, index) in algorithms"
                :key="index"
                :value="algorithm_ids[index]"
              >
                {{ a }}
              </option>
            </select>
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block flex">
          <div class="label">
            Script file name
          </div>
          <div class="input-value">
            <input
              v-model="algorithm_params['script_file_name']"
              :disabled="algorithm !== 0xffffffff"
            >
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div
        v-if="algorithm != 3"
        class="setting-block"
      >
        <div class="setting-type">
          Training Loop Setting
        </div>

        <div class="sub-block flex">
          <div class="label">
            Batch Size
          </div>
          <div class="input-value">
            <input
              v-model="batch_size"
              type="text"
            >
          </div>
        </div>  <!-- sub block -->

        <div class="sub-block flex">
          <div class="label">
            Total Epoch
          </div>
          <div class="input-value">
            <input
              v-model="epoch"
              type="text"
            >
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->
    </div>  <!-- column -->

    <div class="column">
      <div
        v-if="algorithm != 3"
        class="setting-block"
      >
        <div class="setting-type">
          Graph Comvolution Params
        </div>

        <div class="sub-block flex">
          <div class="label">
            Number of neighbors
          </div>
          <div class="input-value">
            <input
              v-model="algorithm_params['num_neighbors']"
              type="text"
            >
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->

      <div
        v-else-if="algorithm == 3"
        class="setting-block"
      >
        <div class="setting-type">
          Random Forest Params
        </div>

        <div class="sub-block flex">
          <div class="label">
            Number of trees
          </div>
          <div class="input-value">
            <input
              v-model="algorithm_params['n_estimators']"
              type="text"
            >
          </div>
        </div>  <!-- sub block -->
        <div class="sub-block flex">
          <div class="label">
            Maximum Depth<br>
            ("None" or integer)
          </div>
          <div class="input-value">
            <input
              v-model="algorithm_params['max_depth']"
              type="text"
            >
          </div>
        </div>  <!-- sub block -->
      </div>  <!-- setting block -->
    </div>  <!-- column -->

    <div class="button-area">
      <button @click="runModel">
        Run
      </button>
      <button
        class="button-cancel"
        @click="hideModal"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalParamsSetting',
  data: function () {
    return {
      'algorithms': ['C-GCNN', 'Kernel-GCNN', 'DBSCAN-GCNN', 'Random Forest', 'User defined'],
      'algorithm_ids': [0, 1, 2, 3, 0xffffffff],
      'dataset_index': 0,
      'algorithm': 0,
      'algorithm_params': {
        'script_file_name': '',
        'num_neighbors': 5,
        'fc_unit': [100, 50],
        'channels': [10, 20, 20],
        'n_estimators': 100,
        'max_depth': 'None'
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
      this.$emit('run')
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
  width: 100%;
  height: calc(100% - #{$modal-tab-height});

  .column {
    position: relative;
    width: 50%;
    padding: $padding-large;

    .setting-block {
      margin-bottom: $margin-large;

      .setting-type {
        height: $text-height-regular;
        line-height: $text-height-regular;
        font-size: $fs-regular;
      }
    }
  }

  .sub-block {
    margin-top: $margin-middle;
    margin-left: $margin-middle;

    .label, .input-value {
      width: 50%;
      height: $text-height-small;
      line-height: $text-height-small;
      font-size: $fs-small;
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
