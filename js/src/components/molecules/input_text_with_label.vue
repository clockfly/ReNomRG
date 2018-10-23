<template>
  <div class="input-text-with-label">
    <PlainText
      :text="labeltext"
      :textcolor="labelcolor"></PlainText>
    <InputText :placeholder="placeholder"
      @change="$emit('change', $event)"></InputText>
  </div>
</template>

<script>
import { GRAY, LABEL_WIDTH, LABEL_HEIGHT } from '@/const'
import InputText from '@/components/atoms/input_text'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'InputTextWithLabel',
  components: {
    InputText,
    PlainText
  },
  props: {
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
.input-text-with-label {
  @include prefix("display", "flex");
}
</style>
