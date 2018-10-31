<template>
  <div id="add-model-modal">
    <div class="modal-background" @click="hideModal"></div>

    <div class="modal-content">
      <div class="modal-tab">
        <div @click="setTab('params')">params</div>
        <div @click="setTab('dataset')">dataset</div>
      </div>
      <ModalParamsSetting v-if="tab === 'params'"></ModalParamsSetting>
      <ModalDataset v-if="tab === 'dataset'"
        @cancel="setTab('params')"></ModalDataset>
    </div>
  </div>
</template>

<script>
import ModalDataset from '@/components/pages/training/modal_dataset'
import ModalParamsSetting from '@/components/pages/training/modal_params_setting'

export default {
  name: 'ModalAdd',
  components: {
    ModalDataset,
    ModalParamsSetting
  },
  data: function () {
    return {
      'tab': 'params'
    }
  },
  methods: {
    hideModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': false})
    },
    setTab: function (value) {
      this.tab = value
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
    padding: 16px;
    background-color: $white;

    .modal-tab {
      @include prefix("display", "flex");
    }
  }
}
</style>
