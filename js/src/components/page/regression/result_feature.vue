<template>
  <div id="result-feature">
    <div class="title">
      Feature Importances
    </div>

    <div class="content">
      <div v-if="selected_model">
        <div v-for="(h,index) in $store.getters.headerWithoutTarget" :key="index" class="name-importance">
          <div class="column-name">
            {{h}}
          </div>
          <div class="importance-value">
            {{Math.round(importances[index]*1000) / 1000}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'ResultFeature',
  computed: mapState(['selected_model', 'importances'])
}
</script>

<style lang="scss" scoped>
#result-feature {
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

  $item-font-size: 16px;
  $content-margin: 8px;

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
    height: calc(100% - #{$title-height});
    padding: $content-padding-top $content-padding-horizontal $content-padding-bottom;

    background-color: $content-bg-color;
    border: 1px solid $content-border-color;
    border-radius: 4px;

    .name-importance {
      display: flex;
      margin: 4px;
      border-bottom: 1px solid $content-border-color;

      .column-name {
        font-size: $item-font-size;
        margin-right: $content-margin;
        color: #999999;
      }

      .importance-value {
        margin-left: auto;
        font-size: $item-font-size;
      }
    }
  }
}
</style>
