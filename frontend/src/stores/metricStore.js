import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'

const WS_METRICS_URL = 'ws://localhost:8000/ws/metrics'
const WS_ALERTS_URL  = 'ws://localhost:8000/ws/alerts'
const MAX_HISTORY    = 30   // data points per chart
const MAX_ALERTS     = 50   // keep last N alerts

export const useMetricStore = defineStore('metrics', () => {
  // ── State ─────────────────────────────────────────────
  const servers = ref({})       // { 'server-01': MetricSnapshot, ... }
  const history = ref({})       // { 'server-01': { cpu: [...], memory: [...], ... } }
  const alerts  = ref([])       // AlertEvent[]
  const selectedServer = ref('server-01')

  // ── WebSocket: Metrics ────────────────────────────────
  const { status: metricsStatus, connect: connectMetrics } = useWebSocket(WS_METRICS_URL, {
    onMessage(data) {
      if (data.type !== 'metric') return
      const sid = data.server_id

      // Update latest snapshot (create plain copy to avoid reactivity issues)
      servers.value[sid] = structuredClone(data)

      // Append to history ring-buffer
      if (!history.value[sid]) {
        history.value[sid] = { cpu: [], memory: [], disk: [], response_time: [], request_rate: [], timestamps: [] }
      }
      const h = history.value[sid]
      const keys = ['cpu', 'memory', 'disk', 'response_time', 'request_rate']
      keys.forEach(k => {
        h[k] = [...h[k], data[k]].slice(-MAX_HISTORY)
      })
      const ts = new Date(data.timestamp).toLocaleTimeString()
      h.timestamps = [...h.timestamps, ts].slice(-MAX_HISTORY)
    }
  })

  // ── WebSocket: Alerts ─────────────────────────────────
  const { status: alertsStatus, connect: connectAlerts } = useWebSocket(WS_ALERTS_URL, {
    onMessage(data) {
      if (data.type !== 'alert') return
      alerts.value.unshift({ ...structuredClone(data), id: Date.now() })
      if (alerts.value.length > MAX_ALERTS) alerts.value.pop()
    }
  })

  // ── Actions ───────────────────────────────────────────
  function startStreaming() {
    connectMetrics()
    connectAlerts()
  }

  function dismissAlert(id) {
    alerts.value = alerts.value.filter(a => a.id !== id)
  }

  function clearAlerts() {
    alerts.value = []
  }

  // ── Getters ───────────────────────────────────────────
  const currentServer = computed(() => servers.value[selectedServer.value] || null)
  const currentHistory = computed(() => history.value[selectedServer.value] || null)
  const unreadAlerts = computed(() => alerts.value.filter(a => a.severity === 'critical').length)
  const serverList = computed(() => Object.keys(servers.value))

  return {
    servers, history, alerts, selectedServer,
    metricsStatus, alertsStatus,
    currentServer, currentHistory, unreadAlerts, serverList,
    startStreaming, dismissAlert, clearAlerts,
  }
})
