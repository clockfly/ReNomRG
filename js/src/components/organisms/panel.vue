<template>
  <div class="panel">
    <BannerText
      :text="banner_text"
      :h="'32px'"></BannerText>

    <div class="panel-content margin-top-8">
      <slot name="pannel_content"></slot>
    </div>
  </div>
</template>

<script>
import BannerText from '@/components/molecules/banner_text'

export default {
  name: 'Panel',
  components: {
    BannerText
  },
  props: {
    banner_text: {}
  }
}
</script>

<style lang="scss" scoped>
.panel {
  padding: 8px;

  .panel-content {
    padding: 16px;
    background-color: $white;
  }
}
</style>
