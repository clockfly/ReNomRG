<template>
  <svg :width="w" :height="h" :viewbox="'0 0 '+w+' '+h"
    style="background: #eee">
    <g :transform="'scale('+w/max(x_values)+','+h/max(y_values)+')'">
      <circle v-for="(x,index) in x_values"
        :cx="x"
        :cy="y_values[index]"
        :r="r"/>
    </g>
  </svg>
</template>

<script>
export default {
  name: 'ScatterPlot',
  props: {
    w: { type: Number, default: 100 },
    h: { type: Number, default: 100 },
    x_values: { type: Array },
    y_values: { type: Array },
    r: { type: Number, default: 1 }
  },
  methods: {
    max: function (v) {
      return Math.max.apply(null, v)
    }
  }
}
</script>

<style lang="scss" scoped>
svg {
}
</style>
