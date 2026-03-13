<template>
  <div class="metric-card" :class="statusClass">
    <div class="metric-card__header">
      <span class="metric-card__icon">{{ icon }}</span>
      <span class="metric-card__label">{{ label }}</span>
    </div>
    <div class="metric-card__value">
      {{ formattedValue }}<span class="metric-card__unit">{{ unit }}</span>
    </div>
    <div class="metric-card__bar">
      <div class="metric-card__fill" :style="{ width: barWidth + '%' }" :class="fillClass" />
    </div>
    <div class="metric-card__sub">{{ subtitle }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label:    { type: String, required: true },
  value:    { type: Number, default: 0 },
  unit:     { type: String, default: '%' },
  icon:     { type: String, default: '📊' },
  subtitle: { type: String, default: '' },
  /** If true, uses value directly as bar percentage. Otherwise uses value as bar %. */
  maxValue: { type: Number, default: 100 },
})

const barWidth    = computed(() => Math.min(100, (props.value / props.maxValue) * 100))
const formattedValue = computed(() => Number.isInteger(props.value) ? props.value : props.value?.toFixed(1) ?? '—')

const fillClass = computed(() => {
  if (props.unit !== '%') return 'fill--blue'
  if (props.value >= 85) return 'fill--red'
  if (props.value >= 70) return 'fill--yellow'
  return 'fill--green'
})

const statusClass = computed(() => {
  if (props.unit !== '%') return ''
  if (props.value >= 85) return 'metric-card--critical'
  if (props.value >= 70) return 'metric-card--warning'
  return ''
})
</script>

<style scoped>
.metric-card {
  background: var(--card-bg, #1e2533);
  border: 1px solid var(--border, #2d3748);
  border-radius: 12px;
  padding: 1.2rem;
  transition: border-color 0.3s;
}
.metric-card--warning  { border-color: #f59e0b; }
.metric-card--critical { border-color: #ef4444; box-shadow: 0 0 12px rgba(239,68,68,0.2); }

.metric-card__header {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.8rem; color: #9ca3af; margin-bottom: 8px;
}
.metric-card__icon { font-size: 1rem; }
.metric-card__value {
  font-size: 2rem; font-weight: 700; color: #f1f5f9; line-height: 1;
}
.metric-card__unit { font-size: 0.9rem; font-weight: 400; color: #9ca3af; margin-left: 2px; }

.metric-card__bar {
  height: 6px; background: #374151; border-radius: 9999px;
  margin: 10px 0 6px; overflow: hidden;
}
.metric-card__fill {
  height: 100%; border-radius: 9999px; transition: width 0.5s ease, background-color 0.3s;
}
.fill--green  { background: #22c55e; }
.fill--yellow { background: #f59e0b; }
.fill--red    { background: #ef4444; }
.fill--blue   { background: #3b82f6; }

.metric-card__sub { font-size: 0.75rem; color: #6b7280; }
</style>
