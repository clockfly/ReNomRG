import Vue from 'vue'
import Router from 'vue-router'
import Training from '@/components/pages/training.vue'
// import PredictionPage from '@/components/page/prediction/page.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    { path: '/', name: 'Training', component: Training }
    // { path: '/prediction', name: 'Prediction', component: PredictionPage }
  ]
})

export default router
