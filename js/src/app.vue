<template>
<div id="app">
  <AppHeader></AppHeader>
  <NavigationBar></NavigationBar>

  <div class="container">
    <router-view></router-view>
  </div>

  <AppFooter></AppFooter>
</div>
</template>

<script>
import AppHeader from '@/components/common/app_header.vue'
import AppFooter from '@/components/common/app_footer.vue'
import NavigationBar from '@/components/common/navigation_bar.vue'

require('@fortawesome/fontawesome')
require('@fortawesome/fontawesome-free-solid')
require('@fortawesome/fontawesome-free-regular')
require('@fortawesome/fontawesome-free-brands')

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    NavigationBar
  },
  created: function () {
    this.$store.commit('setPageName', {
      'page_name': this.$router.currentRoute.name
    })
  }
}
</script>

<style lang="scss" scoped>
#app {
  position: relative;
  width: $full-screen-width;
  padding-top: $header-height;
  background-color: $background-gray;

  .container {
    width: $full-screen-width;
    max-width: $max-width;
    margin: 0 auto;
  }
}
</style>
