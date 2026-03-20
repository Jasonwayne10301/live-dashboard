<template>
  <section class="server-admin">
    <div class="admin-header">
      <h3>Server Management</h3>
      <button class="logout-btn" @click="$emit('logout')">Logout</button>
    </div>

    <div class="admin-grid">
      <div class="admin-box">
        <h4>Existing servers</h4>
        <ul>
          <li v-for="sv in servers" :key="sv.id">
            <strong>{{ sv.name }}</strong> ({{ sv.protocol }}://{{ sv.host }}:{{ sv.port }})
            <button @click="edit(sv)">Edit</button>
          </li>
        </ul>
      </div>
      <div class="admin-box">
        <h4>{{ form.id ? 'Edit server' : 'Add server' }}</h4>
        <div class="server-form">
          <input v-model="form.name" placeholder="Name" />
          <input v-model="form.host" placeholder="Host" />
          <input v-model.number="form.port" type="number" placeholder="Port" />
          <select v-model="form.protocol"><option value="http">http</option><option value="ssh">ssh</option></select>
          <input v-model="form.user" placeholder="SSH user" />
          <input v-model="form.password" placeholder="SSH password" />
          <input v-model="form.key" placeholder="SSH key path" />
          <label><input type="checkbox" v-model="form.is_active" /> Active</label>
          <button @click="submit" :disabled="loading">{{ loading ? 'Saving...' : 'Save' }}</button>
          <p class="error" v-if="formError">{{ formError }}</p>
          <p class="success" v-if="successMessage">{{ successMessage }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'
import { toRefs } from 'vue'

const props = defineProps({ servers: Array, authHeader: Function })
const emit = defineEmits(['refresh', 'logout'])

const form = ref({ id: null, name: '', host: '', port: 8000, protocol: 'http', user: '', password: '', key: '', is_active: true })
const formError = ref('')
const successMessage = ref('')
const loading = ref(false)

watch(() => props.servers, () => {
  // keep current edit view if necessary
})

function edit(server) {
  form.value = { ...server }
  successMessage.value = ''
  formError.value = ''
}

async function submit() {
  formError.value = ''
  successMessage.value = ''
  loading.value = true
  try {
    const isEdit = !!form.value.id
    const url = isEdit ? `http://localhost:8000/api/v1/servers/${form.value.id}` : 'http://localhost:8000/api/v1/servers/'
    const method = isEdit ? 'PUT' : 'POST'
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json', ...props.authHeader() },
      body: JSON.stringify(form.value)
    })
    if (!res.ok) {
      const detail = (await res.json().catch(() => ({}))).detail || 'Could not save'
      throw new Error(detail)
    }
    successMessage.value = isEdit ? 'Server updated' : 'Server added'
    form.value = { id: null, name: '', host: '', port: 8000, protocol: 'http', user: '', password: '', key: '', is_active: true }
    emit('refresh')
  } catch (err) {
    formError.value = err.message || 'Save failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.success { color: #34d399; margin-top: 0.35rem; font-size: 0.85rem; }
</style>
