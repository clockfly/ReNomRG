<template lang="html">
<footer>
  <div class="footer-content">
    <img class="logo-img" src="/static/img/renomlogo.png">
    <div class="version">ReNom RG beta</div>
  </div>
  <div class="copyright-bar">
    <div class="copyright">©︎2018 GRID INC. ALL rights reserved.</div>
  </div>
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

  .footer-content {
    max-width: $max-width;
    margin: 0 auto;

    .logo-img {
      margin: 24px 8px 8px 8px;
    }
    .version {
      line-height: 32px;
      color: $white;
    }
  }
  .copyright-bar {
    background: #02294C;
    .copyright {
      max-width: $max-width;
      margin: 0 auto;
      line-height: 32px;
      color: $white;
    }
  }
}
</style>
