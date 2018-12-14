<template>
  <div id="page">
    <div class="page-content">

      <div class="main-content">
        <div class="panel-columns">
          <div class="panel-left">
            <Dashboard></Dashboard>
          </div>
          <div class="panel-right">
            <ModelMap></ModelMap>
          </div>
        </div>

        <div class="panel-columns">
          <div class="panel-left">
            <ModelDetail></ModelDetail>
          </div>
          <div class="panel-right">
            <LearningCurve></LearningCurve>
          </div>
        </div>

        <PredictionSample></PredictionSample>
        <Features></Features>
      </div>

      <div class="list-area">
        <ModelList></ModelList>
      </div>
    </div>

    <ModalAdd v-if="$store.state.add_model_modal_shown_flag"
      @run="watchStart">
    </ModalAdd>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import ModalAdd from '@/components/common/modal_add_model'
import Dashboard from '@/components/pages/training/dashboard'
import Features from '@/components/pages/training/features'
import LearningCurve from '@/components/pages/training/learning_curve'
import ModelDetail from '@/components/pages/training/model_detail'
import ModelList from '@/components/pages/training/model_list'
import ModelMap from '@/components/pages/training/model_map'
import PredictionSample from '@/components/pages/training/prediction_sample'

export default {
  name: 'TrainingPage',
  components: {
    Dashboard,
    Features,
    LearningCurve,
    ModalAdd,
    ModelDetail,
    ModelList,
    ModelMap,
    PredictionSample
  },
  computed: mapState(['running_models']),
  created: function () {
    this.$store.dispatch('loadLabels')
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadModels')
    this.watchStart()
  },
  methods: {
    watchStart: function () {
      const url = '/api/renom_rg/models/wait_model_update'
      axios.get(url).then(ret => {
        if (ret.data.updated === true) {
          this.$store.dispatch('loadRunningModels').then(ret => {
            setTimeout(this.watchStart, 1000)
          })
        } else {
          setTimeout(this.watchStart, 1000)
        }
      }).catch(err => {
        setTimeout(this.watchStart, 60000)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
#page {
  width: 100%;

  .page-content {
    @include prefix('display', 'flex');
    position: relative;
    width: 100%;

    .main-content {
      width: $content-width;
      .panel-columns {
        @include prefix('display', 'flex');
        width: 100%;

        .panel-left {
          width: $panel-left-width;
        }
        .panel-right {
          width: $panel-right-width;
        }
      }
    }
    .list-area {
      position: absolute;
      right: 0px;
      top: 0px;
      width: $list-width;
      height: 100%;
    }
  }
}
</style>
