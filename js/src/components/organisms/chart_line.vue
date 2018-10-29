<template>
  <svg :width="w" :height="h" :viewbox="'0 0 '+w+' '+h">
    <g>
      <polyline v-for="(line, index) in line_values"
        :points="linePoints(line)"
        stroke="black" fill="none"
        :stroke-width="1"></polyline>
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
    line_values: { type: Array },
    r: { type: Number, default: 1 }
  },
  data: function () {
    return {
      margin: { 'top': 10, 'bottom': 10, 'right': 10, 'left': 10 }
    }
  },
  computed: {
    scale: function () {
      let scale_x
      let scale_y
      for (let line of this.line_values) {
        let sx = (this.w - this.margin.right - this.margin.left) / line.length
        let sy = (this.h - this.margin.top - this.margin.bottom) / max(line)
        if (!scale_x || sx < scale_x) {
          scale_x = sx
        }
        if (!scale_y || sy < scale_y) {
          scale_y = sy
        }
      }
      return {
        'scale_x': scale_x,
        'scale_y': scale_y
      }
    }
  },
  methods: {
    linePoints: function (line) {
      let points = ''
      for (let i in line) {
        points += this.scale.scale_x * i + this.margin.left
        points += ' '
        points += this.scale.scale_y * (max(line) - line[i]) + this.margin.top
        points += ' '
      }
      return points
    }
  }
}
</script>

<style lang="scss" scoped>
svg {
}
</style>
