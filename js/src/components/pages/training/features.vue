/*
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
*/

<template>
  <div id="features">
    <div class="panel">
      <div class="panel-title">
        Features
      </div>

      <div class="panel-content features-content flex">
        <div
          v-if="selectedDataset"
          class="target-feature-list"
        >
          <div class="feature-type">
            Target Features
          </div>

          <div
            v-for="(l,index) in target_labels"
            :key="index"
            class="feature-item"
          >
            {{ l }}
          </div>
        </div>

        <div class="explanatory-feature-list">
          <div class="feature-type">
            Explanatory Features (Feature Importance)
          </div>

          <div class="feature-list flex">
            <div
              v-for="(l,index) in explanatory_labels"
              :key="index"
              class="feature-item"
            >
              {{ l }}
              <span
                v-if="selectedModel && selectedModel.importances"
                class="feature-importances"
              >
                ({{ selectedModel.importances[index] }})
              </span>
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
  computed: {
    ...mapGetters(['selectedDataset', 'selectedModel']),
    target_labels: function () {
      let filtered = []
      if (this.selectedDataset && this.selectedDataset.labels) {
        const target_column_ids = this.selectedDataset.target_column_ids
        filtered = this.selectedDataset.labels.filter(function (element, index, array) {
          return target_column_ids.indexOf(index) !== -1
        })
      }
      return filtered
    },
    explanatory_labels: function () {
      let filtered = []
      if (this.selectedDataset && this.selectedDataset.labels) {
        const explanatory_column_ids = this.selectedDataset.explanatory_column_ids
        filtered = this.selectedDataset.labels.filter(function (element, index, array) {
          return explanatory_column_ids.indexOf(index) !== -1
        })
      }
      return filtered
    }
  }
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
          .feature-importances{
            font-size: $fs-small;
            color: $gray;
          }
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
