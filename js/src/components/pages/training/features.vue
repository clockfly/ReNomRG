<template>
  <div id="features">
    <div class="panel">
      <div class="panel-title">
        Features
      </div>

      <div class="panel-content features-content">
        <div class="target-feature-list">
          <div class="feature-type">Target Features</div>

          <div class="feature-item">
            {{ $store.state.labels[$store.state.labels.length - 1] }}
          </div>
        </div>

        <div class="explanatory-feature-list">
          <div class="feature-type">Explanatory Features</div>

          <div class="feature-list">
            <div class="feature-item" v-for="(l,index) in $store.state.labels">
              {{ l }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Features'
}
</script>

<style lang="scss" scoped>
#features {
  $feature-item-height: 24px;
  width: 100%;
  height: $features-height;

  .features-content {
    @include prefix('display', 'flex');
    width: 100%;
    padding: $panel-content-padding;
    overflow-y: scroll;

    .target-feature-list {
      width: 20%;
      .feature-item {
        width: 100%;
      }
    }
    .explanatory-feature-list {
      width: 80%;
      .feature-list {
        @include prefix('display', 'flex');
        flex-wrap: wrap;
        align-items: flex-start;
        .feature-item {
          width: 20%;
        }
      }
    }
    .feature-type {
      height: $feature-item-height;
      margin-bottom: 8px;
      line-height: $feature-item-height;
    }
    .feature-item {
      height: $feature-item-height;
      margin-bottom: 8px;
      padding-left: 8px;
      border-left: 1px solid "#ccc";
      font-size: $fs-small;
      line-height: $feature-item-height;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}
</style>
