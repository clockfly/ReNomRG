<template>
  <div id="dataset-modal">
    <div
      class="modal-background"
      @click="$emit('hide')"
    />

    <div class="modal-content">
      <ModalDatasetSetting @cancel="$emit('hide')" />
    </div>
  </div>
</template>

<script>
import ModalDatasetSetting from '@/components/common/modal_dataset_setting'

export default {
  name: 'Modal',
  components: {
    ModalDatasetSetting
  }
}
</script>

<style lang="scss" scoped>
#dataset-modal {
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
  }
}
</style>
