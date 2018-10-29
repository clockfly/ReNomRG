<template>
  <div class="banner-text padding-left-16"
    v-bind:style="{ 'background': bgcolor }">
    <PlainText
      :text="text"
      :w="w"
      :h="h"
      :textcolor="textcolor"></PlainText>
  </div>
</template>

<script>
import { WHITE, DARK_BLUE, TEXT_FONT_SIZE } from '@/const'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'BannerText',
  components: {
    PlainText
  },
  props: {
    // banner
    bgcolor: { type: String, default: DARK_BLUE },
    // text
    text: {},
    w: { type: String },
    h: { type: String },
    textcolor: { type: String, default: WHITE },
    fontsize: { type: String, default: TEXT_FONT_SIZE },
    fontweight: { type: String, default: 'normal' }
  }
}
</script>

<style lang="scss" scoped>
.banner-text {
}
</style>
