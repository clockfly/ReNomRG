<template>
  <div class="banner-text"
    v-bind:style="{ 'background': bgcolor,
                    'color': textcolor }">
    <PlainText
      :text="text"
      :textcolor="textcolor"></PlainText>
  </div>
</template>

<script>
import { WHITE, DARK_BLUE } from '@/const'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'BannerText',
  components: {
    PlainText
  },
  props: {
    text: {},
    textcolor: { type: String, default: WHITE },
    bgcolor: { type: String, default: DARK_BLUE }
  }
}
</script>

<style lang="scss" scoped>
.banner-text {
}
</style>
