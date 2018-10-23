<template>
  <div class="dashboard-ratio-bar">
    <LabelValueText
      :labeltext="'Total Models:'"
      :valuetext="model_list.length"></LabelValueText>

    <div class="bar-legends">
      <div class="legend-item"
        v-for="(color, index) in bar_colors">
        <div class="legend-color-box"
          v-bind:style="{ 'background': color }"></div>
        <PlainText :text="index"></PlainText>
      </div>
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

export default {
  name: 'DashboardRatioBar',
  components: {
    PlainText,
    LabelValueText
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
    .legend-item {
      @include prefix("display", "flex");
      .legend-color-box {
        width: 8px;
        height: 8px;
      }
    }
  }

  .horizontal-bar {
    @include prefix("display", "flex");
    .bar-item {
      height: 8px;
    }
  }
}
</style>
