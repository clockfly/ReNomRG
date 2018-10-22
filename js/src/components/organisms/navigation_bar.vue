<template>
<div id="navigation">
  <transition name="mask">
    <div id='mask' v-if="$store.state.navigation_bar_shown_flag" @click='hideMenu'></div>
  </transition>

  <transition name="nav">
    <div id="navigation-bar" v-if="$store.state.navigation_bar_shown_flag">
      <ClickableText
        :text="'Training'"
        :textcolor="white"
        @click="goTraining()">
        <FaIcon slot="icon"
          :textcolor="white"
          :cls="'fa fa-home'"></FaIcon>
      </ClickableText>

      <ClickableText
        :text="'Dataset'"
        :textcolor="white"
        @click="goDataset()">
        <FaIcon slot="icon"
          :textcolor="white"
          :cls="'fa fa-home'"></FaIcon>
      </ClickableText>

      <ClickableText
        :text="'Prediction'"
        :textcolor="white"
        @click="goPrediction()">
        <FaIcon slot="icon"
          :textcolor="white"
          :cls="'fa fa-home'"></FaIcon>
      </ClickableText>
    </div>
  </transition>
</div>
</template>

<script>
import { WHITE } from '@/const'
import FaIcon from '@/components/atoms/fa_icon'
import ClickableText from '@/components/molecules/clickable_text'

export default {
  name: 'NavigationBar',
  components: {
    FaIcon,
    ClickableText
  },
  data: function () {
    return {
      'white': WHITE
    }
  },
  methods: {
    goTraining: function () {
      console.log('go training')
      // this.$store.commit('setPageName', {'page_name': 'Training'})
      // this.$router.push({path: '/'})
      this.hideMenu()
    },
    goPrediction: function () {
      console.log('go prediction')
      // this.$store.commit('setPageName', {'page_name': 'Prediction'})
      // this.$router.push({path: '/prediction'})
      this.hideMenu()
    },
    goDataset: function () {
      console.log('go dataset')
      // this.$store.commit('setPageName', {'page_name': 'Prediction'})
      // this.$router.push({path: '/prediction'})
      this.hideMenu()
    },
    hideMenu: function () {
      this.$store.commit('setNavigationBarShowFlag', {flag: false})
    }
  }
}
</script>

<style lang="scss" scoped>
#navigation {
  position: fixed;
  z-index: 999;

  #mask {
    position: fixed;
    top: $header-height;
    left: 0;
    width: $full-screen-width;
    height: $full-screen-height;
    z-index: 1;
    background-color: rgba(0, 0, 0, 0.4);
  }

  #navigation-bar {
    position: fixed;
    top: $header-height;
    height: $full-screen-height;

    background-color: #262a4e;
    z-index: 2;
  }

  // transition of navigation menu
  .nav-enter-active {
    animation: slide-in 0.4s ease;
  }
  .nav-leave-active {
    animation: slide-in 0.2s ease reverse;
  }
  @keyframes slide-in {
    0% {
      left: -180px;
    }
    100% {
      left: 0;
    }
  }

  // transition of mask
  .mask-enter-active, .mask-leave-active {
    transition: all 0.3s;
  }
  .mask-enter-to, .mask-leave {
    opacity: 1;
  }
  .mask-enter, .mask-leave-to {
    opacity: 0;
  }
}
</style>
