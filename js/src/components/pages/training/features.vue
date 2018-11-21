<template>
  <div id="features">
    <div class="panel">
      <div class="panel-title">
        Features
      </div>

      <div class="panel-content features-content flex">
        <div class="target-feature-list" v-if="selectedDataset">
          <div class="feature-type">Target Features</div>

          <div class="feature-item"
            v-for="(l,index) in selectedDataset.labels"
            v-if="selectedDataset.target_column_ids.indexOf(index) !== -1">
            {{ l }}
          </div>
        </div>

        <div class="explanatory-feature-list">
          <div class="feature-type">Explanatory Features</div>

          <div class="feature-list flex">
            <div class="feature-item"
              v-for="(l,index) in selectedDataset.labels"
              v-if="selectedDataset.target_column_ids.indexOf(index) === -1">
              {{ l }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Features',
  computed: mapGetters(['selectedDataset'])
}
</script>

<style lang="scss" scoped>
#features {
  width: 100%;
  height: $features-height;

  .features-content {
    width: 100%;
    padding: $padding-large;
    overflow-y: scroll;

    .target-feature-list {
      width: 18%;
      margin-right: 2%;
      border-right: $border-width-regular solid $gray;
      .feature-item {
        width: 100%;
      }
    }
    .explanatory-feature-list {
      width: 80%;
      .feature-list {
        flex-wrap: wrap;
        align-items: flex-start;
        .feature-item {
          width: 20%;
        }
      }
    }
    .feature-type {
      height: $text-height-small;
      margin-bottom: $margin-small;
      line-height: $text-height-small;
      color: $gray;
    }
    .feature-item {
      height: $text-height-small;
      margin-bottom: $margin-small;
      padding-left: $padding-small;
      border-left: $border-width-regular solid $gray;
      line-height: $text-height-small;
      font-size: $fs-small;
      color: $gray;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}
</style>
