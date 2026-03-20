<template>
  <div class="login-screen">
    <div class="login-card">
      <h1>Live Dashboard Login</h1>
      <form @submit.prevent="submit">
        <label>
          Username
          <input v-model="username" placeholder="admin" required />
        </label>
        <label>
          Password
          <input type="password" v-model="password" placeholder="admin123" required />
        </label>
        <button type="submit" :disabled="loading">{{ loading ? 'Signing in...' : 'Sign In' }}</button>
      </form>
      <p class="error" v-if="error">{{ error }}</p>
      <p class="hint">Use admin/admin123 (created automatically on first run).</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const router = useRouter()

async function submit() {
  error.value = ''
  loading.value = true

  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 10000)

  try {
    const res = await fetch('http://localhost:8000/api/v1/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: username.value, password: password.value }),
      signal: controller.signal,
    })

    clearTimeout(timeout)

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      const detail = text || res.statusText || 'Invalid credentials'
      throw new Error(detail)
    }

    const data = await res.json()
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('token_type', data.token_type)
    router.replace('/')
  } catch (err) {
    console.error('Login error', err)
    if (err.name === 'AbortError') {
      error.value = 'Login timed out. Kiểm tra backend server đang chạy và CORS.'
    } else {
      error.value = err.message || 'Login failed'
    }
  } finally {
    clearTimeout(timeout)
    loading.value = false
  }
}
</script>

<style scoped>
.login-screen {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
}
.login-card {
  width: min(420px, 90vw);
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.5);
}
.login-card h1 { margin-bottom: 1.1rem; font-size: 1.3rem; }
label { display: block; margin-bottom: 0.8rem; font-weight: 500; }
input { width: 100%; padding: 0.62rem; margin-top: 0.3rem; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: #e2e8f0; }
button { width: 100%; margin-top: 0.8rem; padding: 0.75rem; background: #3b82f6; border: none; border-radius: 8px; color: white; font-weight: 700; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
.error { margin-top: 0.8rem; color: #f87171; }
.hint { margin-top: 1rem; color: #94a3b8; font-size: 0.8rem; }
</style>
