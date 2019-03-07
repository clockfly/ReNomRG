/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

import Vue from 'vue'
import Router from 'vue-router'
import Dataset from '@/components/pages/dataset'
import Prediction from '@/components/pages/prediction'
import Training from '@/components/pages/training'

Vue.use(Router)

const router = new Router({
  routes: [
    { path: '/', name: 'Training', component: Training },
    { path: '/dataset', name: 'Dataset', component: Dataset },
    { path: '/prediction', name: 'Prediction', component: Prediction }
  ]
})

export default router
