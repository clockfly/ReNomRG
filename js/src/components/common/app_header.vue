<template>
<header>
  <div class="header-top">
    <div class="menu-button" @click="toggleMenu">
      <i class="fa fa-bars icon" aria-hidden="true"></i>
    </div>

    <div class="title">
      ReNomRG > {{$store.state.page_name}}
    </div>
  </div>
</header>
</template>

<script>
export default {
  name: 'AppHeader',
  data: function () {
    return {
      'tab': 'training'
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
  position: fixed;
  top: 0px;
  left: 0px;
  width: $full-screen-width;
  height: $header-height;
  margin: 0;
  padding: 0;
  z-index: 3;

  .header-top {
    @include prefix('display', 'flex');
    height: $header-height;
    background-color: $dark-blue;
    .menu-button, .title, .icon {
      height: $header-height;
      line-height: $header-height;
      color: $white;
    }
    .menu-button {
      margin-left: $margin-middle;
      margin-right: $margin-middle;
      cursor:pointer;
    }
  }
}
</style>
