<template>
  <div id="add-model-modal">
    <div class="modal-background" @click="hideAddModelModal"></div>

    <div class="modal-content">

      <div class="modal-title">
        Setting of New Model
      </div>

      <div class="modal-param-area">
        <div class="param-item">
          <div class="label">Target</div>
          <div class="item">
            <select class="target-select-box" v-model="target_column_id">
              <option v-for="(h,index) in $store.state.header" :key="index" :value="index">{{h}}</option>
            </select>
          </div>
        </div>

        <div class="param-item">
          <div class="label">Algorithm</div>
          <div class="item">
            <select class="algorithm-select-box" v-model="algorithm">
              <option value="0">Random Forest</option>
            </select>
          </div>
        </div>

        <div v-if="algorithm == 0" class="param-item">
          <div class="label">Estimators</div>
          <div class="item">
            <input type="text" v-model="n_estimators" maxlength="4">
          </div>
        </div>

        <div v-if="algorithm == 0" class="param-item">
          <div class="label">Depth</div>
          <div class="item">
            <input type="text" v-model="max_depth" maxlength="2">
          </div>
        </div>
      </div>

      <div class="modal-button-area">
        <button @click="hideAddModelModal">Cancel</button>
        <button @click="runModel">Run</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'AddModelModal',
  data: function () {
    return {
      algorithm: 0,
      target_column_id: 0,

      // random forest params
      n_estimators: 10,
      max_depth: 2
    }
  },
  methods: {
    hideAddModelModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': false})
    },
    runModel: function () {
      let params = {}
      if (parseInt(this.algorithm) === 0) {
        params = {
          'n_estimators': this.n_estimators,
          'max_depth': this.max_depth
        }
      }

      this.$store.dispatch('addModel', {
        'algorithm': this.algorithm,
        'params': params,
        'target_column_id': this.target_column_id
      })

      this.hideAddModelModal()
    }
  }
}
</script>

<style lang="scss" scoped>
#add-model-modal {
  $app-max-width: 1280px;
  $header-height: 35px;

  $modal-color: #000000;
  $modal-opacity: 0.7;

  $modal-content-width: 80%;
  $modal-content-height: 70%;
  $modal-content-bg-color: #fefefe;
  $modal-content-padding: 32px;

  $modal-title-font-size: 24px;
  $modal-sub-title-font-size: 16px;

  $content-margin: 8px;
  $content-label-width: 120px;
  $content-font-size: 16px;

  position: fixed;
  left: 0;
  top: $header-height;
  width: 100vw;
  height: calc(100vh - #{$header-height});

  .modal-background {
    width: 100%;
    height: 100%;
    background-color: $modal-color;
    opacity: $modal-opacity;
  }

  .modal-content {
    display: flex;
    flex-direction: column;

    position: absolute;
    top: 50%;
    left: 50%;
    -webkit-transform: translateY(-50%) translateX(-50%);
    transform: translateY(-50%) translateX(-50%);

    width: $modal-content-width;
    height: $modal-content-height;
    max-width: $app-max-width;
    padding: $modal-content-padding;
    background-color: $modal-content-bg-color;
    opacity: 1;

    .modal-title {
      font-size: $modal-title-font-size;
      font-weight: bold;
    }

    .modal-param-area {
      display: flex;
      display: -webkit-flex;
      flex-direction: column;
      -webkit-flex-direction: column;

      .param-item {
        display: flex;
        position: relative;
        margin-top: $content-margin;

        .label {
          width: $content-label-width;
          font-weight: 500;
          font-size: $content-font-size;
          line-height: $content-font-size*1.5;
        }
        .item {
          margin-left: $content-margin;
          width: $content-label-width;
          input {
            width: 100%;
          }
        }
      }
    }

    .modal-button-area {
      display: flex;
      flex-direction: row-reverse;

      position: absolute;
      bottom: $modal-content-padding;
      right: $modal-content-padding;
    }
  }
}
</style>
