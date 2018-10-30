export function max (array) {
  return Math.max.apply(null, array)
}

export function min (array) {
  return Math.min.apply(null, array)
}

export function round (v, round_off) {
  return Math.round(v * round_off) / round_off
}
