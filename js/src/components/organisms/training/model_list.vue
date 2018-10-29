<template>
  <div id="model-list">
    <div class="add-button-area padding-8">
      <Button
        :text="'Add new model'"
        :w="'100%'"
        @click="showModal">
        <FaIcon slot="icon"
          :cls="'fa fa-plus margin-right-8'"
          :textcolor="white"></FaIcon>
      </Button>
    </div>

    <div class="list-area padding-8">
      <BannerText
        :text="'Model List'"
        :h="'32px'"></BannerText>

      <div class="model-list-item margin-top-8"
        v-for="(model,index) in $store.state.model_list"
        @click="selectModel(model)">
        <LabelValueText
          class="margin-bottom-8"
          :labeltext="'Model ID:'"
          :labelwidth="label_width"
          :valuetext="model.model_id"></LabelValueText>

        <LabelValueText
          class="margin-bottom-8"
          :labeltext="'Algorithm:'"
          :labelwidth="label_width"
          :valuetext="model.algorithm"></LabelValueText>

        <LabelValueText
          class="margin-bottom-8"
          :labeltext="'Validation Loss:'"
          :labelwidth="label_width"
          :valuetext="round(model.best_epoch_valid_loss)"></LabelValueText>

        <LabelValueText
          class="margin-bottom-8"
          :labeltext="'RMSE:'"
          :labelwidth="label_width"
          :valuetext="round(model.best_epoch_rmse)"></LabelValueText>

        <LabelValueText
          class="margin-bottom-8"
          :labeltext="'Max Absolute Error:'"
          :labelwidth="label_width"
          :valuetext="round(model.best_epoch_max_abs_error)"></LabelValueText>
      </div>
    </div>
  </div>
</template>

<script>
import { WHITE } from '@/const'
import { round } from '@/utils'
import Button from '@/components/atoms/button'
import FaIcon from '@/components/atoms/fa_icon'
import LabelValueText from '@/components/molecules/label_value_text'
import BannerText from '@/components/molecules/banner_text'
import Panel from '@/components/organisms/panel'

export default {
  name: 'ModelList',
  components: {
    Button,
    FaIcon,
    LabelValueText,
    BannerText,
    Panel
  },
  data: function () {
    return {
      'white': WHITE,
      'label_width': '120px'
    }
  },
  methods: {
    round: function (v) {
      return round(v, 1000)
    },
    selectModel: function (m) {
      this.$store.commit('setSelectedModelId', {'model_id': m['model_id']})
      this.$store.dispatch('loadModel', {'model_id': m['model_id']})
    },
    showModal: function () {
      this.$store.commit('setAddModelModalShowFlag', {'flag': true})
    }
  },
  created: function () {
    this.$store.dispatch('loadModels')
  }
}
</script>

<style lang="scss" scoped>
#model-list {
  .model-list-item {
    background-color: $white;
  }
}
</style>
