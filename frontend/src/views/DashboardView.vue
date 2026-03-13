<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="dashboard__header">
      <div class="dashboard__title">
        <span class="dashboard__logo">⚡</span>
        <span>Live System Dashboard</span>
      </div>
      <div class="dashboard__status-bar">
        <span class="status-dot" :class="wsStatusClass" />
        <span class="status-text">{{ wsStatusText }}</span>
        <span class="status-sep">|</span>
        <span class="status-text">{{ serverList.length }} servers</span>
        <span class="status-sep" v-if="store.unreadAlerts > 0">|</span>
        <span class="alert-badge" v-if="store.unreadAlerts > 0">
          🔴 {{ store.unreadAlerts }} critical
        </span>
      </div>
    </header>

    <!-- Server Tabs -->
    <div class="server-tabs">
      <button
        v-for="sid in MetricSimulator.SERVERS"
        :key="sid"
        class="server-tab"
        :class="{ 'server-tab--active': store.selectedServer === sid }"
        @click="store.selectedServer = sid"
      >
        🖥️ {{ sid }}
        <span
          v-if="store.servers[sid]"
          class="server-tab__cpu"
          :class="cpuBadgeClass(store.servers[sid].cpu)"
        >
          {{ store.servers[sid].cpu.toFixed(0) }}%
        </span>
      </button>
    </div>

    <!-- Main Content -->
    <main class="dashboard__body">
      <!-- No data yet -->
      <div v-if="!current" class="dashboard__loading">
        <div class="spinner" />
        <p>Connecting to server stream...</p>
      </div>

      <template v-else>
        <!-- Metric Cards -->
        <section class="metrics-grid">
          <MetricCard label="CPU Usage"     :value="current.cpu"             unit="%" icon="🔥" :subtitle="`${current.active_connections} connections`" />
          <MetricCard label="Memory"        :value="current.memory"          unit="%" icon="💾" subtitle="RAM utilization" />
          <MetricCard label="Disk"          :value="current.disk"            unit="%" icon="💿" subtitle="Storage used" />
          <MetricCard label="Response Time" :value="current.response_time"   unit="ms" icon="⚡" :maxValue="500" :subtitle="`${current.request_rate} req/s`" />
          <MetricCard label="Network In"   :value="current.network_in"      unit=" Mbps" icon="⬇️" :maxValue="200" subtitle="Inbound traffic" />
          <MetricCard label="Network Out"  :value="current.network_out"     unit=" Mbps" icon="⬆️" :maxValue="200" subtitle="Outbound traffic" />
        </section>

        <!-- Charts + Alerts -->
        <section class="dashboard__charts-alerts">
          <div class="charts-grid">
            <LineChart title="CPU"          :labels="hist.timestamps" :data="hist.cpu"           color="#ef4444" unit="%" />
            <LineChart title="Memory"       :labels="hist.timestamps" :data="hist.memory"        color="#8b5cf6" unit="%" />
            <LineChart title="Disk"         :labels="hist.timestamps" :data="hist.disk"          color="#f59e0b" unit="%" />
            <LineChart title="Response Time":labels="hist.timestamps" :data="hist.response_time" color="#3b82f6" unit="ms" :maxY="600" />
          </div>
          <AlertPanel />
        </section>
      </template>
    </main>

    <!-- Footer -->
    <footer class="dashboard__footer">
      Built with FastAPI · WebSocket · Vue.js · Chart.js
      &nbsp;|&nbsp; Last update: {{ lastUpdate }}
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useMetricStore } from '@/stores/metricStore'
import MetricCard from '@/components/MetricCard.vue'
import LineChart  from '@/components/LineChart.vue'
import AlertPanel from '@/components/AlertPanel.vue'

// Expose SERVERS constant for the template
const MetricSimulator = { SERVERS: ['server-01', 'server-02', 'server-03'] }

const store = useMetricStore()
const lastUpdate = ref('—')

onMounted(() => store.startStreaming())

const current = computed(() => store.currentServer)
const hist    = computed(() => store.currentHistory || {})
const serverList = computed(() => store.serverList)

watch(current, () => {
  lastUpdate.value = new Date().toLocaleTimeString()
})

const wsStatusClass = computed(() => ({
  'status-dot--green':  store.metricsStatus === 'connected',
  'status-dot--yellow': store.metricsStatus === 'connecting',
  'status-dot--red':    ['disconnected', 'error'].includes(store.metricsStatus),
}))

const wsStatusText = computed(() => ({
  connected:    'Live',
  connecting:   'Connecting...',
  disconnected: 'Disconnected',
  error:        'Error',
}[store.metricsStatus] ?? 'Unknown'))

function cpuBadgeClass(cpu) {
  if (cpu >= 85) return 'badge--red'
  if (cpu >= 70) return 'badge--yellow'
  return 'badge--green'
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #0f1624;
  color: #e2e8f0;
  font-family: 'Inter', system-ui, sans-serif;
  display: flex; flex-direction: column;
}

/* Header */
.dashboard__header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.9rem 1.5rem;
  background: #131c2e;
  border-bottom: 1px solid #1e2d45;
}
.dashboard__title  { display: flex; align-items: center; gap: 8px; font-size: 1.1rem; font-weight: 700; }
.dashboard__logo   { font-size: 1.3rem; }
.dashboard__status-bar { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; }

.status-dot        { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.status-dot--green  { background: #22c55e; box-shadow: 0 0 6px #22c55e; animation: pulse 2s infinite; }
.status-dot--yellow { background: #f59e0b; }
.status-dot--red    { background: #ef4444; }
.status-text        { color: #9ca3af; }
.status-sep         { color: #374151; }
.alert-badge        { font-size: 0.75rem; color: #fca5a5; font-weight: 600; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

/* Server tabs */
.server-tabs {
  display: flex; gap: 6px; padding: 0.7rem 1.5rem;
  background: #0f1624; border-bottom: 1px solid #1e2d45;
}
.server-tab {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 14px; border-radius: 8px; border: 1px solid #2d3748;
  background: transparent; color: #9ca3af; font-size: 0.82rem; cursor: pointer;
  transition: all 0.2s;
}
.server-tab:hover        { border-color: #4b6282; color: #e2e8f0; }
.server-tab--active      { background: #1e2d45; border-color: #3b82f6; color: #e2e8f0; }
.server-tab__cpu         { font-size: 0.72rem; padding: 1px 6px; border-radius: 9999px; font-weight: 700; }
.badge--green  { background: #14532d; color: #4ade80; }
.badge--yellow { background: #451a03; color: #fbbf24; }
.badge--red    { background: #450a0a; color: #f87171; }

/* Body */
.dashboard__body {
  flex: 1; padding: 1.2rem 1.5rem; display: flex; flex-direction: column; gap: 1.2rem;
}

/* Loading */
.dashboard__loading {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 1rem; height: 300px; color: #6b7280;
}
.spinner {
  width: 36px; height: 36px; border: 3px solid #2d3748;
  border-top-color: #3b82f6; border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Metric Cards */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

/* Charts + Alerts layout */
.dashboard__charts-alerts {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 1.2rem;
  align-items: start;
}
.charts-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;
}

/* Footer */
.dashboard__footer {
  padding: 0.6rem 1.5rem; text-align: center;
  font-size: 0.72rem; color: #374151;
  border-top: 1px solid #1e2d45;
}

@media (max-width: 900px) {
  .dashboard__charts-alerts { grid-template-columns: 1fr; }
  .charts-grid { grid-template-columns: 1fr; }
  .metrics-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
