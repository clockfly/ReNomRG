<template>
  <div class="select-box-with-label">
    <PlainText
      :text="labeltext"
      :w="labelwidth"
      :h="h"
      :textcolor="labelcolor"
      :fontsize="labelfontsize"
      :fontweight="labelfontweight"></PlainText>
    <SelectBox
      :options="options"
      :value="value"
      :w="selectwidth"
      :h="h"
      :padding="selectpadding"
      :backgroundcolor="selectbackgroundcolor"
      :textcolor="selecttextcolor"
      :fontsize="selectfontsize"
      @input="$emit('input', $event)"></SelectBox>
  </div>
</template>

<script>
import { GRAY, WHITE, BLACK, LABEL_WIDTH, LABEL_HEIGHT, INPUT_WIDTH, INPUT_FONT_SIZE } from '@/const'
import PlainText from '@/components/atoms/plain_text'
import SelectBox from '@/components/atoms/select_box'

export default {
  name: 'SelectBoxWithLabel',
  components: {
    PlainText,
    SelectBox
  },
  props: {
    h: { type: String, default: LABEL_HEIGHT },
    // label
    labeltext: { type: String },
    labelwidth: { type: String, default: LABEL_WIDTH },
    labelcolor: { type: String, default: GRAY },
    labelfontsize: {},
    labelfontweight: {},
    // selectbox
    value: {},
    options: { type: Array },
    selectwidth: { type: String, default: INPUT_WIDTH },
    selectpadding: { type: String, default: '0' },
    selectbackgroundcolor: { type: String, default: WHITE },
    selecttextcolor: { type: String, default: BLACK },
    selectfontsize: { type: String, default: INPUT_FONT_SIZE }
  }
}
</script>

<style lang="scss" scoped>
.select-box-with-label {
  @include prefix("display", "flex");
}
</style>
