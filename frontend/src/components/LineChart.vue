<template>
  <div class="chart-wrapper">
    <div class="chart-wrapper__header">
      <span>{{ title }}</span>
      <span class="chart-wrapper__current">{{ currentValue }}</span>
    </div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale,
  PointElement, LineElement, Filler, Tooltip,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip)

const props = defineProps({
  title:      { type: String, required: true },
  labels:     { type: Array, default: () => [] },
  data:       { type: Array, default: () => [] },
  color:      { type: String, default: '#3b82f6' },
  unit:       { type: String, default: '%' },
  maxY:       { type: Number, default: 100 },
})

const currentValue = computed(() => {
  const last = props.data.at(-1)
  return last != null ? `${Number(last).toFixed(1)}${props.unit}` : '—'
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [{
    data: props.data,
    borderColor: props.color,
    backgroundColor: props.color + '22',
    borderWidth: 2,
    fill: true,
    tension: 0.4,
    pointRadius: 0,
    pointHoverRadius: 4,
  }],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: 300 },
  scales: {
    x: {
      ticks: { color: '#6b7280', maxTicksLimit: 6, font: { size: 10 } },
      grid:  { color: '#1f2937' },
    },
    y: {
      min: 0,
      max: props.maxY,
      ticks: { color: '#6b7280', font: { size: 10 } },
      grid:  { color: '#1f2937' },
    },
  },
  plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } },
}
</script>

<style scoped>
.chart-wrapper {
  background: var(--card-bg, #1e2533);
  border: 1px solid var(--border, #2d3748);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  height: 180px;
}
.chart-wrapper__header {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 0.8rem; color: #9ca3af; margin-bottom: 8px;
}
.chart-wrapper__current { font-weight: 700; color: #f1f5f9; font-size: 0.9rem; }
.chart-wrapper canvas { height: 130px !important; }
</style>
