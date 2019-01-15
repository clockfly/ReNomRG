<template>
  <div id="app">
    <AppHeader />
    <NavigationBar />

    <div class="paging-area">
      <router-view />
    </div>

    <AppFooter />
    <ModalError v-if="$store.state.error_msg" />
  </div>
</template>

<script>
import AppHeader from '@/components/common/app_header.vue'
import AppFooter from '@/components/common/app_footer.vue'
import ModalError from '@/components/common/modal_error'
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
    ModalError,
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
  width: $full-screen-width;
  background-color: $background-gray;

  .paging-area {
    width: 100%;
    max-width: $max-width;
    margin: 0 auto;
    padding-top: $header-height;
  }
}
</style>
