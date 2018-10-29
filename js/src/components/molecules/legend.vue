<template>
  <div class="legend">
    <div class="legend-color margin-right-4"
      v-bind:style="{ 'background': legendcolor }"></div>
    <PlainText :text="text"
      :w="w"
      :h="h"
      :textcolor="textcolor"
      :fontsize="fontsize"
      :fontweight="fontweight"></PlainText>
  </div>
</template>

<script>
import { BLACK, TEXT_FONT_SIZE } from '@/const'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'Legend',
  components: {
    PlainText
  },
  props: {
    // legend color
    legendcolor: { type: String, default: BLACK },
    // text
    text: {},
    w: { type: String },
    h: { type: String },
    textcolor: { type: String, default: BLACK },
    fontsize: { type: String, default: TEXT_FONT_SIZE },
    fontweight: { type: String, default: 'normal' }
  }
}
</script>

<style lang="scss" scoped>
.legend {
  @include prefix("display", "flex");
  justify-content: center;
  align-items: center;

  .legend-color {
    width: 8px;
    height: 8px;
  }
}
</style>
