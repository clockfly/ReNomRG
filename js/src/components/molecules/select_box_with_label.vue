<template>
  <div class="select-box-with-label">
    <PlainText
      :text="labeltext"
      :textcolor="labelcolor"></PlainText>
    <SelectBox
      :options="options"
      @change="$emit('change', $event)"></SelectBox>
  </div>
</template>

<script>
import { GRAY, LABEL_WIDTH, LABEL_HEIGHT } from '@/const'
import PlainText from '@/components/atoms/plain_text'
import SelectBox from '@/components/atoms/select_box'

export default {
  name: 'SelectBoxWithLabel',
  components: {
    PlainText,
    SelectBox
  },
  props: {
    options: {
      type: Array
    },
    labeltext: {
      type: String
    },
    labelcolor: {
      type: String,
      default: GRAY
    },
    placeholder: {
      type: String
    },
    w: {
      type: String,
      default: LABEL_WIDTH
    },
    h: {
      type: String,
      default: LABEL_HEIGHT
    }
  }
}
</script>

<style lang="scss" scoped>
.select-box-with-label {
  @include prefix("display", "flex");
}
</style>
