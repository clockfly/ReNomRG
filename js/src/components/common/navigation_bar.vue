/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="navigation">
    <transition name="mask">
      <div
        v-if="$store.state.navigation_bar_shown_flag"
        id="mask"
        @click="hideMenu"
      />
    </transition>

    <transition name="nav">
      <div
        v-if="$store.state.navigation_bar_shown_flag"
        id="navigation-bar"
      >
        <div
          class="menu-item flex"
          @click="goTraining()"
        >
          <i class="fa fa-home icon" />
          <div class="menu-name">
            Training
          </div>
        </div>

        <div
          class="menu-item flex"
          @click="goDataset()"
        >
          <i class="fas fa-database icon" />
          <div class="menu-name">
            Dataset
          </div>
        </div>

        <div
          class="menu-item flex"
          @click="goPrediction()"
        >
          <i class="fas fa-chart-area icon" />
          <div class="menu-name">
            Prediction
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'NavigationBar',
  data: function () {
    return {
      'nav_open': 'regression'
    }
  },
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
  z-index: 999;

  #mask {
    position: fixed;
    top: $header-height;
    left: 0;
    width: $full-screen-width;
    height: $full-screen-height;
    z-index: 998;
    background-color: $black;
    opacity: $modal-opacity;
  }

  #navigation-bar {
    position: fixed;
    top: $header-height;
    width: 12%;
    height: $full-screen-height;
    background-color: $blue;
    z-index: 999;

    .task-name, .menu-item {
      height: $nav-item-height;
      padding: 0 $padding-middle;
      line-height: $nav-item-height;
      color: $white;
    }
    .menu-item {
      cursor:pointer;
    }
    .menu-item:hover {
      background-color: $gray;
    }
    .menu-item {
      .icon, .menu-name {
        height: $nav-item-height;
        line-height: $nav-item-height;
        color: $white;
      }
      .icon {
        margin: 0px $margin-small 0px $margin-middle;
      }
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
