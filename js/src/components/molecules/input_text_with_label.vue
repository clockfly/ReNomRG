<template>
  <div class="input-text-with-label">
    <PlainText
      :text="labeltext"
      :w="labelwidth"
      :h="h"
      :textcolor="labelcolor"
      :fontsize="labelfontsize"
      :fontweight="labelfontweight"></PlainText>
    <InputText
      :value="value"
      :placeholder="placeholder"
      :w="inputwidth"
      :h="h"
      :padding="inputpadding"
      :borderwidth="inputborderwidth"
      :bordertype="inputbordertype"
      :bordercolor="inputbordercolor"
      :backgroundcolor="inputbackgroundcolor"
      :textcolor="inputtextcolor"
      :fontsize="inputfontsize"
      @input="$emit('input', $event)"></InputText>
  </div>
</template>

<script>
import { GRAY, WHITE, BLACK, INPUT_FONT_SIZE, LABEL_WIDTH, LABEL_HEIGHT } from '@/const'
import InputText from '@/components/atoms/input_text'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'InputTextWithLabel',
  components: {
    InputText,
    PlainText
  },
  props: {
    h: { type: String, default: LABEL_HEIGHT },
    // label
    labeltext: { type: String },
    labelwidth: { type: String, default: LABEL_WIDTH },
    labelcolor: { type: String, default: GRAY },
    labelfontsize: {},
    labelfontweight: {},
    // input
    value: {},
    placeholder: { type: String },
    inputwidth: {},
    inputpadding: {},
    inputborderwidth: { type: String, default: '1px' },
    inputbordertype: { type: String, default: 'solid' },
    inputbordercolor: { type: String, default: GRAY },
    inputbackgroundcolor: { type: String, default: WHITE },
    inputtextcolor: { type: String, default: BLACK },
    inputfontsize: { type: String, default: INPUT_FONT_SIZE }
  }
}
</script>

<style lang="scss" scoped>
.input-text-with-label {
  @include prefix("display", "flex");
}
</style>
