<template>
  <div id="model-deploy-button">
    <button class="deploy-button" @click="deployModel">
        Deploy Model
    </button>
  </div>
</template>

<script>
export default {
  name: 'ModelDeployButton',
  props: {
    'model_id': {
      type: Number,
      required: true
    }
  },
  methods: {
    deployModel: function () {
      this.$store.dispatch('deployAndUpdate', {'model_id': this.model_id})
    }
  }
}
</script>

<style lang="scss" scoped>
#model-deploy-button {
  $button-bg-color: #7F9DB5;
  $button-bg-color-hover: #7590A5;

  .deploy-button {
    padding: 4px 16px;
    background-color: $button-bg-color;
    color: #ffffff;
    text-align: center;
    border-radius: 4px;
    cursor: pointer;
  }
  .deploy-button:hover {
    background-color: $button-bg-color-hover;
  }
}
</style>
