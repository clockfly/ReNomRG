<template>
<header class="padding-left-8">
  <ClickableText
    :h="header_height"
    @click="toggleMenu">
    <FaIcon slot="icon"
      :h="header_height"
      :textcolor="white"
      :cls="'fa fa-bars margin-right-8'"></FaIcon>
  </ClickableText>

  <PlainText
    :text="'ReNom RG > '+$store.state.page_name"
    :h="header_height"
    :textcolor="white"
    :fontsize="'1.25rem'">
  </PlainText>
</header>
</template>

<script>
import { WHITE, HEADER_HEIGHT } from '@/const'
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
      'white': WHITE,
      'header_height': HEADER_HEIGHT
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
  width: $full-screen-width;
  height: $header-height;
  margin: 0;
  padding: 0;
  background-color: $dark-blue;
  z-index: 999;

}
</style>
