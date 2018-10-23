<template>
  <div class="dataset-list">
    <Panel
      :banner_text="'Dataset List'">
      <div slot="pannel_content">
        <div class="content-columns">
          <div class="dataset-table">
            <DatasetListTable></DatasetListTable>
          </div>

          <div class="dataset-detail">
            <DatasetListDetail></DatasetListDetail>
          </div>
        </div>
      </div>
    </Panel>
  </div>
</template>

<script>
import Panel from '@/components/organisms/panel'
import DatasetListDetail from '@/components/organisms/dataset/dataset_list_detail'
import DatasetListTable from '@/components/organisms/dataset/dataset_list_table'

export default {
  name: 'DatasetList',
  components: {
    Panel,
    DatasetListDetail,
    DatasetListTable
  }
}
</script>

<style lang="scss" scoped>
.dataset-list {
  width: $full-parent-width;

  .content-columns {
    @include prefix('display', 'flex');
    width: $full-parent-width;

    .dataset-table {
      width: 30%;
    }
    .dataset-detail {
      width: 70%;
    }
  }
}
</style>
