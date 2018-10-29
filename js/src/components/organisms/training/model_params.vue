<template>
  <div id="model-params">
    <Panel
      :banner_text="'Model Detail'">
      <div slot="pannel_content" class="detail">
        <div class="column" v-if="model">
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
            :labeltext="'Total Epoch:'"
            :labelwidth="label_width"
            :valuetext="model.epoch"></LabelValueText>

          <LabelValueText
            class="margin-bottom-8"
            :labeltext="'Batch Size:'"
            :labelwidth="label_width"
            :valuetext="model.batch_size"></LabelValueText>

          <LabelValueText
            class="margin-bottom-8"
            :labeltext="'Number of Neighbors:'"
            :labelwidth="label_width"
            :valuetext="model.algorithm_params.num_neighbors"></LabelValueText>
        </div>

        <div class="column" v-if="model">
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

          <LabelValueText
            class="margin-bottom-8"
            :labeltext="'R2 Score:'"
            :labelwidth="label_width"
            :valuetext="round(model.best_epoch_r2)"></LabelValueText>
        </div>
      </div>
    </Panel>
  </div>
</template>

<script>
import { round } from '@/utils'
import LabelValueText from '@/components/molecules/label_value_text'
import Panel from '@/components/organisms/panel'

export default {
  name: 'ModelParams',
  components: {
    LabelValueText,
    Panel
  },
  data: function () {
    return {
      'label_width': '120px'
    }
  },
  computed: {
    model: function () {
      return this.$store.state.selected_model
    }
  },
  methods: {
    round: function (v) {
      return round(v, 1000)
    }
  }
}
</script>

<style lang="scss" scoped>
#model-params {
  .detail {
    @include prefix("display", "flex");
    width: 100%;
    height: 100%;

    .column {
      width: 50%;
      height: 100%;
    }
  }
}
</style>
