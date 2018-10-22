<template>
  <div id="result">
    <div class="title">
      Validation Result
    </div>

    <div class="content">
      <result-plot></result-plot>
    </div>
  </div>
</template>

<script>
import ResultPlot from './result_plot.vue'

export default {
  name: 'Result',
  components: {
    'result-plot': ResultPlot
  }
}
</script>

<style lang="scss" scoped>
#result {
  $component-margin-top: 32px;

  $border-width: 2px;
  $border-color: #006699;

  $title-height: 44px;
  $title-font-size: 15pt;
  $font-weight-medium: 500;

  $content-padding-top: 24px;
  $content-padding-horizontal: 24px;
  $content-padding-bottom: 16px;

  $content-bg-color: #ffffff;
  $content-border-color: #cccccc;

  height: 100%;
  margin: 0;
  margin-top: $component-margin-top;
  border-top: $border-width solid $border-color;

  .title {
    line-height: $title-height;
    font-size: $title-font-size;
    font-weight: $font-weight-medium;
  }

  .content {
    display: flex;
    display: -webkit-flex;

    height: calc(100% - #{$title-height});
    padding: $content-padding-top $content-padding-horizontal $content-padding-bottom;

    background-color: $content-bg-color;
    border: 1px solid $content-border-color;
    border-radius: 4px;
  }
}
</style>
