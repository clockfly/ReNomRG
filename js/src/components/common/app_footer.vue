<template lang="html">
<footer>
  <img class="logo-img" :src="url">

  <div class="version">ReNom RG {{version}}</div>
  <div class="copyright">&copy; 2018 GRID INC. ALL rights reserved.</div>
</footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data () {
    return {
      'version': 'beta',
      'url': require('../../../static/img/renomlogo.png')
    }
  }
}
</script>

<style lang="scss" scoped>
footer {
  display: block;
  width: $full-screen-width;
  background: $dark-blue;
  z-index: 99999;

  .logo-img {
    margin: 16px;
  }

  .version, .copyright {
    line-height: 32px;
    color: $white;
  }
  .copyright {
    background: $dark-blue;
  }
}
</style>
