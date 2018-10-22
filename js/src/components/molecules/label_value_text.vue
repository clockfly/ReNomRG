<template>
  <div class="label-value-text">
    <PlainText
      :text="labeltext"
      :textcolor="labelcolor"></PlainText>

    <PlainText
      :text="valuetext"
      :textcolor="valuecolor"></PlainText>
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
    labeltext: {
      type: String
    },
    valuetext: {
    },
    labelcolor: {
      type: String,
      default: GRAY
    },
    valuecolor: {
      type: String,
      default: BLACK
    }
  }
}
</script>

<style lang="scss" scoped>
.label-value-text {
  @include prefix('display', 'flex');
}
</style>
