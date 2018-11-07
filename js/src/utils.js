import * as d3 from 'd3'
import { inner_axis_color, outer_axis_color } from '@/const'

export function max (array) {
  return Math.max.apply(null, array)
}

export function min (array) {
  return Math.min.apply(null, array)
}

export function round (v, round_off) {
  return Math.round(v * round_off) / round_off
}

/**
* d3
*/
export function getScale (domain, range) {
  return d3.scaleLinear()
    .domain(domain)
    .range(range)
}

export function removeSvg (id) {
  d3.select(id).selectAll('svg').remove()
}

export function styleAxis (axis) {
  axis.selectAll('path')
    .style('stroke', outer_axis_color)
  axis.selectAll('line')
    .style('stroke', inner_axis_color)
    .style('stroke-dasharray', '2,2')
  axis.selectAll('.tick').selectAll('text')
    .style('fill', outer_axis_color)
    .style('font-size', '0.60em')
}
