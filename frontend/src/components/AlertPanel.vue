<template>
  <div class="alert-panel">
    <div class="alert-panel__header">
      <span>🔔 Alerts</span>
      <div style="display:flex; gap:8px; align-items:center">
        <span class="alert-badge" v-if="criticalCount > 0">{{ criticalCount }} critical</span>
        <button class="btn-clear" @click="store.clearAlerts()" v-if="store.alerts.length">Clear</button>
      </div>
    </div>

    <div class="alert-panel__list">
      <transition-group name="alert-slide">
        <div
          v-for="alert in store.alerts.slice(0, 20)"
          :key="alert.id"
          class="alert-item"
          :class="`alert-item--${alert.severity}`"
        >
          <span class="alert-item__icon">{{ severityIcon(alert.severity) }}</span>
          <div class="alert-item__body">
            <div class="alert-item__msg">{{ alert.message }}</div>
            <div class="alert-item__meta">
              {{ alert.server_id }} · {{ alert.metric }} · {{ formatTime(alert.timestamp) }}
            </div>
          </div>
          <button class="alert-item__dismiss" @click="store.dismissAlert(alert.id)">✕</button>
        </div>
      </transition-group>

      <div v-if="!store.alerts.length" class="alert-panel__empty">
        ✅ No alerts — all systems normal
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMetricStore } from '@/stores/metricStore'

const store = useMetricStore()
const criticalCount = computed(() => store.alerts.filter(a => a.severity === 'critical').length)

function severityIcon(severity) {
  return { critical: '🔴', warning: '🟡', info: '🔵' }[severity] ?? '⚪'
}

function formatTime(ts) {
  return new Date(ts).toLocaleTimeString()
}
</script>

<style scoped>
.alert-panel {
  background: #1e2533; border: 1px solid #2d3748;
  border-radius: 12px; overflow: hidden;
}
.alert-panel__header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.8rem 1rem; font-size: 0.85rem; font-weight: 600;
  color: #e2e8f0; border-bottom: 1px solid #2d3748;
}
.alert-badge {
  background: #ef4444; color: white; font-size: 0.7rem;
  padding: 2px 8px; border-radius: 9999px; font-weight: 600;
}
.btn-clear {
  background: transparent; border: 1px solid #4b5563; color: #9ca3af;
  font-size: 0.7rem; padding: 2px 8px; border-radius: 6px; cursor: pointer;
}
.btn-clear:hover { border-color: #6b7280; color: #e2e8f0; }

.alert-panel__list { max-height: 340px; overflow-y: auto; }
.alert-panel__empty { padding: 1.5rem; text-align: center; color: #6b7280; font-size: 0.85rem; }

.alert-item {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 0.7rem 1rem; border-bottom: 1px solid #1a2030;
  transition: background 0.2s;
}
.alert-item--critical { background: rgba(239,68,68,0.08); }
.alert-item--warning  { background: rgba(245,158,11,0.08); }

.alert-item__icon  { font-size: 0.9rem; margin-top: 2px; flex-shrink: 0; }
.alert-item__body  { flex: 1; min-width: 0; }
.alert-item__msg   { font-size: 0.82rem; color: #e2e8f0; }
.alert-item__meta  { font-size: 0.72rem; color: #6b7280; margin-top: 2px; }
.alert-item__dismiss {
  background: transparent; border: none; color: #4b5563;
  cursor: pointer; font-size: 0.75rem; flex-shrink: 0;
}
.alert-item__dismiss:hover { color: #9ca3af; }

/* Transition */
.alert-slide-enter-active { transition: all 0.3s ease; }
.alert-slide-enter-from   { opacity: 0; transform: translateY(-8px); }
</style>
