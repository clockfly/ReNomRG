<template>
<header>
  <ClickableText
    @click="toggleMenu">
    <FaIcon slot="icon"
      :textcolor="white"
      :cls="'fa fa-bars'"></FaIcon>
  </ClickableText>

  <PlainText
    :text="'ReNom RG > '+$store.state.page_name"
    :textcolor="white">
  </PlainText>
</header>
</template>

<script>
import { WHITE } from '@/const'
import FaIcon from '@/components/atoms/fa_icon'
import PlainText from '@/components/atoms/plain_text'
import ClickableText from '@/components/molecules/clickable_text.vue'

export default {
  name: 'AppHeader',
  components: {
    FaIcon,
    PlainText,
    ClickableText
  },
  data: function () {
    return {
      'white': WHITE
    }
  },
  methods: {
    toggleMenu: function () {
      this.$store.commit('setNavigationBarShowFlag', {
        flag: !this.$store.state.navigation_bar_shown_flag
      })
    }
  }
}
</script>


<style lang="scss" scoped>
header {
  @include prefix('display', 'flex');
  position: fixed;
  top: 0px;
  left: 0px;
  width: $full-width;
  height: $header-height;
  margin: 0;
  padding: 0;
  background-color: $header-color;
  z-index: 999;

}
</style>
