/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

import Vue from 'vue'
import store from '@/store/store'
import router from '@/router/router'
import App from '@/app'

new Vue({
  el: '#app',
  router: router,
  store: store,
  render: h => h(App)
})
