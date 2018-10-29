<template>
  <div class="label-value-text">
    <PlainText
      :text="labeltext"
      :w="labelwidth"
      :h="h"
      :textcolor="labelcolor"
      :fontsize="labelfontsize"
      :fontweight="labelfontweight"></PlainText>

    <PlainText
      :text="valuetext"
      :w="valuewidth"
      :h="h"
      :textcolor="valuecolor"
      :fontsize="valuefontsize"
      :fontweight="valuefontweight"></PlainText>
  </div>
</template>

<script>
import { BLACK, GRAY } from '@/const'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'LabelValueText',
  components: {
    PlainText
  },
  props: {
    h: {},
    // label
    labeltext: { type: String },
    labelwidth: {},
    labelcolor: { type: String, default: GRAY },
    labelfontsize: {},
    labelfontweight: {},
    // value
    valuetext: {},
    valuewidth: {},
    valuecolor: { type: String, default: BLACK },
    valuefontsize: {},
    valuefontweight: {}
  }
}
</script>

<style lang="scss" scoped>
.label-value-text {
  @include prefix('display', 'flex');
}
</style>
