<template lang="html">
<footer>
  <img class="logo-img" src="/static/img/renomlogo.png">

  <div class="version">ReNom RG beta</div>
  <div class="copyright">©︎2018 GRID INC. ALL rights reserved.</div>
</footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style lang="scss" scoped>
footer {
  position: relative;
  width: $full-screen-width;
  background: $dark-blue;
  z-index: 1;

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
