<template>
  <div id="dashboard">
    <div class="title">
      Dashboard
    </div>

    <div class="content">
      <!-- <div class="dashboard-model-summary">
        <dashboard-count-bar></dashboard-count-bar>
      </div>

      <div class="dashboard-model-plot">
        <dashbpard-plot></dashbpard-plot>
      </div> -->
    </div>
  </div>
</template>

<script>
import DashboardCountBar from './dashboard_count_bar.vue'
import DashboardPlot from './dashboard_plot.vue'

export default {
  name: 'DashBoard',
  components: {
    'dashboard-count-bar': DashboardCountBar,
    'dashbpard-plot': DashboardPlot
  }
}
</script>

<style lang="scss" scoped>
#dashboard {
  height: $content-dashboard-height;
  margin: 0;
  margin-top: $content-parts-margin;

  .title {
    height:$content-top-header-hight;
    font-size: $content-top-header-font-size;
    font-family: $content-top-header-font-family;
    background:$header-color;
    color:$font-color;
    margin-top: $component-margin-top;
    .title-text{
      line-height: $content-top-header-hight;
      margin-left: $content-top-heder-horizonral-margin;
    }
    .panel{
      background-color: $panel-bg-color;
      text-align: center;
      line-height: $content-top-header-hight;
      &:hover{
        cursor:pointer;
        background-color: $panel-bg-color-hover;
      }
    }
  }

  .content {
    display: flex;
    display: -webkit-flex;

    // height: calc(100% - #{$title-height});
    // padding: $content-padding-top $content-padding-horizontal $content-padding-bottom;
    //
    // background-color: $content-bg-color;
    // border: 1px solid $content-border-color;
    // border-radius: 4px;
    //
    // .dashboard-model-summary {
    //   width: 50%;
    //   #model-ratio-bar {
    //     height: 40%;
    //   }
    //   #running-models {
    //     height: 60%;
    //   }
    // }
    //
    // .dashboard-model-plot {
    //   width: 50%;
    //   height: 100%;
    //   margin-left: 24px;
    // }
  }
}
</style>
