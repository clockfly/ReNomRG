<template>
  <div id="page">
    <div class="dataset-list">
      <div class="panel">
        <div class="panel-title panel-with-button">
          Dataset List
          <div class="setting-button" @click="show_modal = true">
            > Setting of Dataset
          </div>
        </div>

        <div class="panel-content dataset-list-content">
          <div class="content-left">
            <div class="table-header">
              <div class="table-row">
                <div class="table-item">Dataset Name</div>
                <div class="table-item">Train ratio</div>
                <div class="table-item">Create Date</div>
              </div>
            </div>
            <div class="table-content">
              <div class="table-row" v-for="(dataset, index) in $store.state.dataset_list" :key="index" @click="selectDataset(dataset)">
                <div class="table-item">{{ dataset.name }}</div>
                <div class="table-item">{{ dataset.train_ratio }}</div>
                <div class="table-item">{{ dataset.created }}</div>
              </div>
            </div>
          </div> <!-- content-left dataset list -->

          <div class="content-right" v-if="selected_dataset">
            <div class="dataset-name">
              {{selected_dataset.name}}
            </div>
            <div class="dataset-detail">
              <div class="column">

                <div class="dataset-description-area">
                  <div class="label">Description</div>
                  <textarea class="description-text" :placeholder="selected_dataset.description" disabled></textarea>
                </div> <!-- dataset description area -->

                <div class="train-ratio-area">
                  <div class="sub-block">
                    <div class="label">Number of data size</div>
                    <div class="values">
                      <div class="train-number">Train {{selected_dataset.train_index.length}}</div>
                      <div class="valid-number">Validation {{selected_dataset.valid_index.length}}</div>
                    </div>
                  </div>

                  <div class="sub-block">
                    <div class="label">All {{selected_dataset.train_index.length+selected_dataset.valid_index.length}}</div>
                    <div class="values">
                      <div class="train-ratio-bar">
                        <div class="bar-item train"
                          v-bind:style="{ 'flex-grow': selected_dataset.train_index.length }"></div>
                        <div class="bar-item validation"
                          v-bind:style="{ 'flex-grow': selected_dataset.valid_index.length }"></div>
                      </div>
                    </div>
                  </div>
                </div> <!-- dataset train valid ratio area -->
              </div> <!-- dataset detail column -->

              <div class="column">
                <div class="label">Histogram</div>
                <div id="train-test-histogram"></div>
              </div>
            </div>
          </div> <!-- content-right dataset detail -->
        </div>
      </div>
    </div>

    <ModalDataset v-if="show_modal" @hide="show_modal = false"></ModalDataset>
  </div>
</template>

<script>
import { mapState } from 'vuex'
// import * as d3 from 'd3'
// import { max, min } from '@/utils'
import ModalDataset from '@/components/common/modal_dataset'

// const train_color = '#0762ad'
// const valid_color = '#ef8200'
// const width = 150
// const height = 150

export default {
  name: 'DatasetPage',
  components: {
    ModalDataset
  },
  data: function () {
    return {
      'show_modal': false
    }
  },
  computed: mapState(['selected_dataset']),
  watch: {
    selected_dataset: function () {
      this.drawHistogram()
    }
  },
  created: function () {
    this.$store.dispatch('loadDatasets')
    this.$store.dispatch('loadLabels')
  },
  methods: {
    selectDataset: function (dataset) {
      this.$store.dispatch('loadSelectedDataset', { 'dataset_id': dataset.dataset_id })
    },
    drawHistogram: function () {
      console.log('draw')
      // if (!selected_dataset) return
      // this.removeHistogram()

      // const target_train = selected_dataset.target_train
      // const target_valid = selected_dataset.target_valid
      // const train_max = max(target_train)
      // const train_min = min(target_train)
      // const valid_max = max(target_valid)
      // const valid_min = min(target_valid)
    },
    removeHistogram: function () {
      d3.select('#train-test-histogram').selectAll('svg').remove()
    }
  }
}
</script>

<style lang="scss" scoped>
#page {
  $table-width: 90%;
  $table-item-height: 32px;
  width: 100%;
  height: calc(100vh - #{$footer-height} - #{$header-height});

  .dataset-list {
    width: 100%;
    height: 100%;
  }

  .panel-with-button {
    @include prefix("display", "flex");
    .setting-button {
      margin-left: auto;
      padding: 0 $panel-content-padding;
      background: $blue;
      color: $white;
    }
  }

  .dataset-list-content {
    @include prefix('display', 'flex');
    padding: $panel-content-padding;
  }
  .content-left {
    width: 30%;
    height: 100%;
    padding-right: $panel-content-padding;
    border-right: 1px solid $light-gray;

    .table-header {
      padding-right: 10px; // margin of table-content scrollbar size
    }
    .table-content {
      width: 100%;
      height: calc(100% - #{$table-item-height});
      overflow-y: scroll;
    }
    .table-row {
      @include prefix('display', 'flex');
      width: $table-width;
      margin: 0 auto;
      border-bottom: 1px solid $light-gray;
    }
    .table-row:hover .table-item {
      color: $light-gray;
    }
    .table-item {
      width: 33%;
      height: $table-item-height;
      line-height: $table-item-height;
      text-align: center;
      font-size: $fs-small;
      color: $gray;
    }
  }

  .content-right {
    width: 70%;
    height: 100%;
    padding: 32px;

    .dataset-name {
      color: $blue;
    }
    .dataset-detail {
      @include prefix('display', 'flex');
      width: 100%;
      .column {
        width: 50%;
        padding: 16px;
      }
      .train-ratio-area {
        margin-top: 32px;
      }
      .label, .train-number, .valid-number {
        color: $gray;
      }
      .description-text {
        width: 100%;
        margin-top: 8px;
      }
      .sub-block {
        @include prefix("display", "flex");
        margin-top: 16px;
        .label, .values {
          width: 50%;
        }
        .values {
          @include prefix("display", "flex");
          .valid-number {
            margin-left: auto;
          }
        }
      }
      .train-ratio-bar {
        @include prefix("display", "flex");
        width: 100%;
        .bar-item {
          height: 8px;
        }
      }
    }
  }
}
</style>
