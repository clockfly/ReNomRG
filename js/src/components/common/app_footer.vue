/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template lang="html">
  <footer>
    <div class="footer-content">
      <div class="logo-and-version">
        <img
          class="logo-img"
          src="/static/img/renomlogo.png"
        >
        <div class="version">
          {{ version }}
        </div>
      </div>
    </div>
    <div class="copyright-bar">
      <div class="copyright">
        ©︎2019 GRID INC. ALL rights reserved.
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data: function () { return { 'version': '0.3.2 beta' } }
}
</script>

<style lang="scss" scoped>
footer {
  position: relative;
  width: $full-screen-width;
  height: $footer-height;
  background: $dark-blue;
  z-index: 1;

  .footer-content {
    max-width: $max-width;
    margin: 0 auto;

    .logo-and-version {
      @include prefix('display', 'flex');
      position: relative;
      .logo-img {
        height: $logo-height;
        margin: $margin-middle;
        margin-left: 0;
      }
      .version {
        height: $copyright-height;
        line-height: $copyright-height;
        margin-top: $logo-height;
        color: $white;
        font-size: $fs-small;
      }
    }
  }
  .copyright-bar {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: $copyright-height;
    background: $copyright-blue;
    .copyright {
      max-width: $max-width;
      height: $copyright-height;
      margin: 0 auto;
      line-height: $copyright-height;
      color: $white;
      font-size: $fs-micro;
    }
  }
}
</style>
