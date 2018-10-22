<template>
  <div id="model-list">
    <div class="add-button-area">
      <Button
        :text="'Add new model'"
        :w="'100%'">
        <FaIcon slot="icon"
          :cls="'fa fa-plus'"
          :textcolor="white"></FaIcon>
      </Button>
    </div>

    <Panel
      :banner_text="'Model List'">
      <div slot="pannel_content">
        <div class="model-list-item"
          v-for="(model,index) in $store.state.model_list">
          <LabelValueText v-for="(item, index) in model"
            :key="index"
            :labeltext="index+':'"
            :valuetext="item"></LabelValueText>
        </div>
      </div>
    </Panel>
  </div>
</template>

<script>
import { WHITE } from '@/const'
import Button from '@/components/atoms/button'
import FaIcon from '@/components/atoms/fa_icon'
import LabelValueText from '@/components/molecules/label_value_text'
import Panel from '@/components/organisms/panel'

export default {
  name: 'ModelList',
  components: {
    Button,
    FaIcon,
    LabelValueText,
    Panel
  },
  data: function () {
    return {
      'white': WHITE
    }
  }
}
</script>

<style lang="scss" scoped>
#model-list {
  .add-button-area {
    padding: 8px;
  }
  .model-list-item {
    border-bottom: 8px solid $background-gray;
  }
}
</style>
