<template>
  <span ref="countRef">{{ displayValue }}</span>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

/**
 * 数字滚动动画组件
 * 提供平滑的数字增长动画效果
 */
interface Props {
  /** 目标数值 */
  endValue: number
  /** 起始数值 */
  startValue?: number
  /** 动画持续时间（毫秒） */
  duration?: number
  /** 是否使用缓动函数 */
  useEasing?: boolean
  /** 数字格式化函数 */
  formatter?: (value: number) => string
}

const props = withDefaults(defineProps<Props>(), {
  startValue: 0,
  duration: 2000,
  useEasing: true,
  formatter: (value: number) => Math.floor(value).toString()
})

const countRef = ref<HTMLElement>()
const displayValue = ref(props.formatter(props.startValue))
let animationId: number | null = null

/**
 * 缓动函数 - easeOutQuart
 * @param t 当前时间
 * @param b 起始值
 * @param c 变化量
 * @param d 持续时间
 */
const easeOutQuart = (t: number, b: number, c: number, d: number): number => {
  t /= d
  t--
  return -c * (t * t * t * t - 1) + b
}

/**
 * 启动数字滚动动画
 */
const startAnimation = () => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }

  const startTime = Date.now()
  const startVal = props.startValue
  const endVal = props.endValue
  const duration = props.duration

  const animate = () => {
    const now = Date.now()
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)

    let currentValue: number
    if (props.useEasing) {
      currentValue = easeOutQuart(elapsed, startVal, endVal - startVal, duration)
    } else {
      currentValue = startVal + (endVal - startVal) * progress
    }

    displayValue.value = props.formatter(currentValue)

    if (progress < 1) {
      animationId = requestAnimationFrame(animate)
    } else {
      displayValue.value = props.formatter(endVal)
      animationId = null
    }
  }

  animationId = requestAnimationFrame(animate)
}

// 监听目标值变化
watch(
  () => props.endValue,
  () => {
    startAnimation()
  }
)

// 组件挂载时启动动画
onMounted(() => {
  startAnimation()
})
</script>

<style scoped>
span {
  display: inline-block;
  font-variant-numeric: tabular-nums;
}
</style>