<template>
<header>
  <div class="menu-button" @click="toggleMenu">
    <i class="fa fa-bars icon" aria-hidden="true"></i>
  </div>

  <div class="title">
    ReNomRG > {{$store.state.page_name}}
  </div>
</header>
</template>

<script>
export default {
  name: 'AppHeader',
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

  .menu-button, .title, .icon {
    height: $header-height;
    line-height: $header-height;
    color: $white;
  }
  .menu-button {
    margin-left: 16px;
    margin-right: 16px;
  }
}
</style>
