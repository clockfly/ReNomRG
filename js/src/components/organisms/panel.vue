<template>
  <div class="panel">
    <BannerText
      :text="banner_text"></BannerText>

    <div class="panel-content">
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
    banner_text: {
      type: String
    }
  }
}
</script>

<style lang="scss" scoped>
.panel {
  padding: 8px;

  .panel-content {
    margin-top: 8px;
    background-color: $white;
  }
}
</style>
