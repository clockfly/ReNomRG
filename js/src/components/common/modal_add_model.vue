<template>
  <div id="add-model-modal">
    <div class="modal-background" @click="hideModal"></div>

    <div class="modal-content">
      <div class="modal-tab flex">
        <div class="tab-item"
          v-bind:class="{ 'tab-active': tab === 'params' }"
          @click="tab = 'params'">Setting of new Model</div>
        <div class="tab-item"
          v-bind:class="{ 'tab-active': tab === 'dataset' }"
          @click="tab = 'dataset'">Setting of Dataset</div>
        <div class="tab-rest"></div>
      </div>

      <ModalParamsSetting v-if="tab === 'params'" @todataset="tab = 'dataset'" @run="$emit('run')"></ModalParamsSetting>
      <ModalDatasetSetting v-if="tab === 'dataset'" @cancel="tab = 'params'"></ModalDatasetSetting>
    </div>
  </div>
</template>

<script>
import ModalDatasetSetting from '@/components/common/modal_dataset_setting'
import ModalParamsSetting from '@/components/common/modal_params_setting'

export default {
  name: 'ModalAdd',
  components: {
    ModalDatasetSetting,
    ModalParamsSetting
  },
  data: function () {
    return {
      'tab': 'params'
    }
  },
  created: function () {
    if (this.$store.state.dataset_list.length === 0) this.tab = 'dataset'
  },
  methods: {
    hideModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': false})
    }
  }
}
</script>

<style lang="scss" scoped>
#add-model-modal {
  position: fixed;
  left: 0;
  top: $header-height;
  width: $full-screen-width;
  height: calc(#{$full-screen-height} - #{$header-height});

  .modal-background {
    width: 100%;
    height: 100%;
    background-color: $black;
    opacity: $modal-opacity;
  }

  .modal-content {
    @include transform-center();
    width: $modal-content-width;
    height: $modal-content-height;
    padding: $modal-content-padding;
    background-color: $white;

    .modal-tab {
      .tab-item {
        flex-grow: 0;
        width: $modal-tab-width;
        height: $modal-tab-height;
        background: $dark-blue;
        text-align: center;
        line-height: $modal-tab-height;
        color: $white;
      }
      .tab-active {
        background: $white;
        border: 1px solid $light-gray;
        border-bottom: none;
        color: $black;
      }
      .tab-rest {
        flex-grow: 1;
        border-bottom: 1px solid $light-gray;
      }
    }
  }
}
</style>
