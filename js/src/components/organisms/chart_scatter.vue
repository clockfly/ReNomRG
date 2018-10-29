<template>
  <svg :width="w" :height="h" :viewbox="'0 0 '+w+' '+h">
    <g>
      <circle v-for="(x,index) in x_values"
        :cx="x * scaleX + margin.left"
        :cy="scaleY * (maxY - y_values[index]) + margin.top"
        :r="r"/>
    </g>
  </svg>
</template>

<script>
import { max } from '@/utils'

export default {
  name: 'ChartScatter',
  props: {
    w: { type: Number, default: 100 },
    h: { type: Number, default: 100 },
    x_values: { type: Array },
    y_values: { type: Array },
    r: { type: Number, default: 1 }
  },
  data: function () {
    return {
      margin: { 'top': 10, 'bottom': 10, 'right': 10, 'left': 10 }
    }
  },
  computed: {
    maxY: function () {
      return max(this.y_values)
    },
    scaleX: function () {
      return (this.w - this.margin.right - this.margin.left) / max(this.x_values)
    },
    scaleY: function () {
      return (this.h - this.margin.top - this.margin.bottom) / max(this.y_values)
    }
  }
}
</script>

<style lang="scss" scoped>
svg {
}
</style>
