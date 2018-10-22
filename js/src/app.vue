<template>
<div id="app">
  <AppHeader></AppHeader>
  <NavigationBar></NavigationBar>

  <div class="container">
    <router-view></router-view>
  </div>

  <AppFooter></AppFooter>

  <!-- <alert-modal v-if="$store.state.alert_modal_flag"></alert-modal> -->
</div>
</template>

<script>
import AppHeader from '@/components/organisms/app_header.vue'
import AppFooter from '@/components/organisms/app_footer.vue'
import NavigationBar from '@/components/organisms/navigation_bar.vue'
// import AlertModal from '@/components/common/alert_modal.vue'

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
    // 'alert-modal': AlertModal
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
    @include horizon-center();
    width: $full-screen-width;
    max-width: $max-width;
  }
}
</style>
