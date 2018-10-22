<template lang="html">
<footer>
  <img :src="url">
  <PlainText
    :text="'ReNom RG '+version"
    :textcolor="white">
  </PlainText>
  <PlainText
    :text="'&copy; 2018 GRID INC. ALL rights reserved.'"
    :textcolor="white">
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
  width: $full-width;
  background: $footer-color;
  margin-top: $component-margin-top;
  z-index: 99999;
}
</style>
