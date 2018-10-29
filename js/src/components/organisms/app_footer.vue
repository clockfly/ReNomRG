<template lang="html">
<footer>
  <img class="margin-16" :src="url">
  <PlainText
    class="margin-left-16"
    :text="'ReNom RG '+version"
    :h="'24px'"
    :textcolor="white"
    :fontsize="'0.8rem'"
    :fontweight="'light'">
  </PlainText>
  <PlainText
    class="margin-left-16"
    :text="'&copy; 2018 GRID INC. ALL rights reserved.'"
    :h="'24px'"
    :textcolor="white"
    :fontsize="'0.8rem'"
    :fontweight="'light'">
  </PlainText>
</footer>
</template>

<script>
import { WHITE } from '@/const'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'AppFooter',
  components: {
    PlainText
  },
  data () {
    return {
      'white': WHITE,
      'version': 'beta',
      'url': require('../../../static/img/renomlogo.png')
    }
  }
}
</script>

<style lang="scss" scoped>
footer {
  display: block;
  width: $full-screen-width;
  background: $dark-blue;
  z-index: 99999;
}
</style>
