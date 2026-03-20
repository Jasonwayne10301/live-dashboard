<template>
  <section class="alert-rule-box">
    <h4>Alert Rule Builder</h4>
    <div class="rule-grid">
      <label>CPU &ge;<input type="number" v-model.number="rules.cpu" /></label>
      <label>Memory &ge;<input type="number" v-model.number="rules.memory" /></label>
      <label>Disk &ge;<input type="number" v-model.number="rules.disk" /></label>
    </div>
    <button @click="save" :disabled="loading">{{ loading ? 'Updating...' : 'Save rules' }}</button>
    <p class="success" v-if="message">{{ message }}</p>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({ value: Object, authHeader: Function })
const emit = defineEmits(['update:value'])

const rules = ref({ cpu: 85, memory: 80, disk: 90 })
const loading = ref(false)
const message = ref('')

watch(() => props.value, val => {
  if (val) rules.value = { ...val }
}, { immediate: true })

async function save() {
  loading.value = true
  try {
    const res = await fetch(`http://localhost:8000/api/v1/metrics/alerts/threshold?cpu=${rules.value.cpu}&memory=${rules.value.memory}&disk=${rules.value.disk}`, {
      method: 'PUT', headers: { ...props.authHeader() }
    })
    if (!res.ok) throw new Error('Could not update alert rules')
    message.value = 'Rules updated'
    emit('update:value', { ...rules.value })
  } catch (err) {
    message.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.alert-rule-box { background: #111a2e; border: 1px solid #273248; border-radius: 10px; padding: 1rem; }
.rule-grid { display:flex; gap:0.8rem; margin-bottom:0.6rem; }
.rule-grid label { display:flex; flex-direction:column; font-size:0.9rem; }
.rule-grid input { margin-top:0.3rem; padding:0.45rem; border-radius:6px; border:1px solid #334155; background:#0f172a; color:#e2e8f0; }
.success { color:#34d399; margin-top:0.5rem; }
button { padding:.55rem .95rem; border-radius:6px; border:none; background:#3b82f6; color:#fff; font-weight:700; }
</style>
