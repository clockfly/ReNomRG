<template>
<div id="navigation">
  <transition name="mask">
    <div id='mask' v-if="$store.state.navigation_bar_shown_flag" @click='hideMenu'></div>
  </transition>

  <transition name="nav">
    <div id="navigation-bar" v-if="$store.state.navigation_bar_shown_flag">
      <div class="menu-item" @click="goTraining()">
        <i class="fa fa-home icon" aria-hidden="true"></i>
        <div class="menu-name">Training</div>
      </div>

      <div class="menu-item" @click="goDataset()">
        <i class="fas fa-database icon"></i>
        <div class="menu-name">Dataset</div>
      </div>

      <div class="menu-item" @click="goPrediction()">
        <i class="fas fa-chart-area icon"></i>
        <div class="menu-name">Prediction</div>
      </div>
    </div>
  </transition>
</div>
</template>

<script>
export default {
  name: 'NavigationBar',
  methods: {
    goTraining: function () {
      this.$store.commit('setPageName', {'page_name': 'Training'})
      this.$router.push({path: '/'})
      this.hideMenu()
    },
    goPrediction: function () {
      this.$store.commit('setPageName', {'page_name': 'Prediction'})
      this.$router.push({path: '/prediction'})
      this.hideMenu()
    },
    goDataset: function () {
      this.$store.commit('setPageName', {'page_name': 'Dataset'})
      this.$router.push({path: '/dataset'})
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
  $nav-item-height: 32px;

  position: fixed;
  z-index: 2;

  #mask {
    position: fixed;
    top: $header-height;
    left: 0;
    width: $full-screen-width;
    height: $full-screen-height;
    z-index: 1;
    background-color: $black;
    opacity: $modal-opacity;
  }

  #navigation-bar {
    position: fixed;
    top: $header-height;
    width: 10%;
    height: $full-screen-height;
    background-color: $dark-blue;
    z-index: 2;

    .menu-item {
      @include prefix('display', 'flex');
      height: $nav-item-height;
      line-height: $nav-item-height;

      .icon, .menu-name {
        height: $nav-item-height;
        line-height: $nav-item-height;
        color: $white;
      }
      .icon {
        margin: 0px 8px;
      }
    }
    .menu-item:hover {
      background-color: $blue;
    }
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
