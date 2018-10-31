<template>
  <div id="features">
    <div class="panel">
      <div class="panel-title">
        Features
      </div>

      <div class="panel-content">
        <div class="feature-list">
          <div class="feature-item" v-for="(l,index) in $store.state.labels">
            {{ l }}
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
  .feature-list {
    @include prefix('display', 'flex');
    flex-wrap: wrap;
    padding: 8px;

    .feature-item {
      margin-right: 8px;
      padding-left: 4px;
      border-left: 2px solid "#ccc";
    }
  }
}
</style>
