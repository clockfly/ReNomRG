<template>
  <div id="add-model-modal">
    <div class="modal-background" @click="hideModal"></div>

    <div class="modal-content padding-16">
      <div class="modal-tab">
        <div @click="setTab('params')">params</div>
        <div @click="setTab('dataset')">dataset</div>
      </div>
      <ModalParamsSetting v-if="tab === 'params'"
        @cancel="hideModal"
        @run="runModel"></ModalParamsSetting>
      <ModalDataset v-if="tab === 'dataset'"
        @cancel="setTab('params')"
        @confirm="confirmDataset"
        @save="saveDataset"></ModalDataset>
    </div>
  </div>
</template>

<script>
import ModalDataset from '@/components/organisms/training/modal_dataset'
import ModalParamsSetting from '@/components/organisms/training/modal_params_setting'

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
    },
    runModel: function (value) {
      this.$store.dispatch('addModel', value)
      this.hideModal()
    },
    confirmDataset: function (value) {
      this.$store.dispatch('confirmDataset', value)
    },
    saveDataset: function (value) {
      this.$store.dispatch('saveDataset', value)
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
    width: $full-parent-width;
    height: $full-parent-height;
    background-color: $black;
    opacity: $modal-opacity;
  }
  //
  .modal-content {
    @include transform-center();
    width: $modal-content-width;
    height: $modal-content-height;
    background-color: $white;

    .modal-tab {
      @include prefix("display", "flex");
    }
  }
}
</style>
