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
            <select
              v-model="dataset_index"
              @change="changeDataset"
            >
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
            <select
              v-model="algorithm"
              @change="changeAlgorithm"
            >
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
        <div class="sub-block">
          <div class="vali_mes">
            {{ vali_one_target }}
          </div>
        </div>

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
        v-if="![3, 4].includes(algorithm)"
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
        v-if="![3, 4].includes(algorithm)"
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
        <div class="sub-block">
          <div class="vali_mes">
            {{ vali_neighbors }}
          </div>
        </div>
      </div>  <!-- setting block -->

      <div
        v-else
        class="setting-block"
      >
        <div
          v-if="algorithm == 3"
          class="setting-type"
        >
          Random Forest Params
        </div>
        <div
          v-else-if="algorithm == 4"
          class="setting-type"
        >
          XGBoost Params
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
            <div class="label-in">
              Maximum Depth
            </div>
            <div
              v-if="algorithm == 3"
              class="label-in"
            >
              ("None" or integer)
            </div>
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
      <button
        :disabled="(vali_neighbors != '' || vali_one_target != '')"
        @click="runModel"
      >
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
      'algorithms': ['C-GCNN', 'Kernel-GCNN', 'DBSCAN-GCNN', 'Random Forest', 'XGBoost', 'User defined'],
      'algorithm_ids': [0, 1, 2, 3, 4, 0xffffffff],
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
      'epoch': 10,
      'vali_neighbors': '',
      'vali_one_target': ''
    }
  },
  mounted: function () {
    this.neighborsSet()
  },
  updated: function () {
    this.neighborsCheck()
    this.singleTargetCheck()
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
    },
    changeAlgorithm: function () {
      if (this.algorithm == 4) {
        this.algorithm_params['max_depth'] = 6
      } else {
        this.algorithm_params['max_depth'] = 'None'
      }
    },
    changeDataset: function () {
      this.neighborsSet()
    },
    neighborsSet: function () {
      if(this.$store.state.dataset_list[this.dataset_index]){
        const explanatory_len = this.$store.state.dataset_list[this.dataset_index].explanatory_column_ids.length
        if (explanatory_len < this.algorithm_params['num_neighbors']
            || this.algorithm_params['num_neighbors'] < 5) {
          if (explanatory_len < 5 || explanatory_len < this.algorithm_params['num_neighbors']) {
            this.algorithm_params['num_neighbors'] = explanatory_len
          } else {
            this.algorithm_params['num_neighbors'] = 5
          }
        }
      }
    },
    neighborsCheck: function () {
      if(this.$store.state.dataset_list[this.dataset_index]){
        const explanatory_len = this.$store.state.dataset_list[this.dataset_index].explanatory_column_ids.length
        if (explanatory_len < this.algorithm_params['num_neighbors'] && ![3, 4].includes(this.algorithm)) {
          this.vali_neighbors = '"Number of neighbors" should be less than the number of explanatory variables in the dataset.'
        } else {
          this.vali_neighbors = ''
        }
      }
    },
    singleTargetCheck: function () {
      if (this.$store.state.dataset_list[this.dataset_index].target_column_ids.length > 1
          && this.algorithm == 4) {
        this.vali_one_target = 'XGBoost can only use dataset of one target variable.'
      } else {
        this.vali_one_target = ''
      }
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
        color: $gray;
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
    }
    .label, .label-in {
      color: $gray;
      font-size: $fs-small;
    }
    .vali_mes {
      color: $err_red;
      font-size: $fs-small;
    }
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
