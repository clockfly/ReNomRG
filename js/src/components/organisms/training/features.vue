<template>
  <div id="features">
    <Panel
      :banner_text="'Features'">
      <div slot="pannel_content">
        <div class="feature-list">
          <div v-for="(l,index) in $store.state.labels">
            <PlainText
              :text="l"></PlainText>
          </div>
        </div>
      </div>
    </Panel>
  </div>
</template>

<script>
import PlainText from '@/components/atoms/plain_text'
import Panel from '@/components/organisms/panel'

export default {
  name: 'Features',
  components: {
    PlainText,
    Panel
  }
}
</script>

<style lang="scss" scoped>
#features {
  .feature-list {
    @include prefix('display', 'flex');
  }
}
</style>
