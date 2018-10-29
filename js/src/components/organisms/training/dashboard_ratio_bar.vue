<template>
  <div class="dashboard-ratio-bar">
    <LabelValueText
      :labeltext="'Total Models:'"
      :h="'40px'"
      :labelwidth="'120px'"
      :valuetext="model_list.length"></LabelValueText>

    <div class="bar-legends">
      <Legend
        class="margin-right-8"
        v-for="(color, index) in bar_colors"
        :key="index" :text="index" :legendcolor="color"></Legend>
    </div>

    <div class="horizontal-bar">
      <div class="bar-item"
        v-for="(model_count, index) in model_counts_per_algorith"
        v-bind:style="{ 'background': bar_colors[index], 'flex-grow': model_count }">
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { BAR_COLORS } from '@/const'
import PlainText from '@/components/atoms/plain_text'
import LabelValueText from '@/components/molecules/label_value_text'
import Legend from '@/components/molecules/legend'

export default {
  name: 'DashboardRatioBar',
  components: {
    PlainText,
    LabelValueText,
    Legend
  },
  data: function () {
    return {
      'bar_colors': BAR_COLORS
    }
  },
  computed: mapState(['model_list', 'model_counts_per_algorith'])
}
</script>

<style lang="scss" scoped>
.dashboard-ratio-bar {
  width: $full-parent-width;

  .bar-legends {
    @include prefix("display", "flex");
  }

  .horizontal-bar {
    @include prefix("display", "flex");
    .bar-item {
      height: 8px;
    }
  }
}
</style>
