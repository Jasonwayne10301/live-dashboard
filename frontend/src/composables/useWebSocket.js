import { ref, onUnmounted } from 'vue'

/**
 * useWebSocket — composable for managing a WebSocket connection.
 * Handles auto-reconnect, connection state, and message parsing.
 *
 * @param {string} url - WebSocket URL, e.g. 'ws://localhost:8000/ws/metrics'
 * @param {object} options
 * @param {Function} options.onMessage - Called with parsed JSON message
 * @param {number}   options.reconnectDelay - ms before reconnect attempt (default 3000)
 */
export function useWebSocket(url, { onMessage, reconnectDelay = 3000 } = {}) {
  const status = ref('disconnected')   // 'connecting' | 'connected' | 'disconnected' | 'error'
  const error = ref(null)

  let ws = null
  let reconnectTimer = null
  let shouldReconnect = true

  function connect() {
    if (ws && ws.readyState === WebSocket.OPEN) return

    status.value = 'connecting'
    ws = new WebSocket(url)

    ws.onopen = () => {
      status.value = 'connected'
      error.value = null
      console.log(`[WS] Connected: ${url}`)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (onMessage) {
          try {
            onMessage(data)
          } catch (e) {
            console.error('[WS] Error in onMessage callback:', e)
          }
        }
      } catch (e) {
        console.warn('[WS] Failed to parse message:', event.data)
      }
    }

    ws.onerror = (e) => {
      status.value = 'error'
      error.value = 'Connection error'
      console.error('[WS] Error:', e)
    }

    ws.onclose = () => {
      status.value = 'disconnected'
      if (shouldReconnect) {
        console.log(`[WS] Disconnected. Reconnecting in ${reconnectDelay}ms...`)
        reconnectTimer = setTimeout(connect, reconnectDelay)
      }
    }
  }

  function disconnect() {
    shouldReconnect = false
    clearTimeout(reconnectTimer)
    ws?.close()
  }

  function send(data) {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(data))
    }
  }

  // Auto-cleanup when component unmounts
  onUnmounted(disconnect)

  return { status, error, connect, disconnect, send }
}
