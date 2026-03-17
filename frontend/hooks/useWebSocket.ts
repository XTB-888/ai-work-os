import { useEffect, useRef, useState, useCallback } from 'react'

interface UseWebSocketOptions {
  onOpen?: (event: Event) => void
  onMessage?: (event: MessageEvent) => void
  onClose?: (event: CloseEvent) => void
  onError?: (event: Event) => void
  reconnect?: boolean
  reconnectInterval?: number
  reconnectAttempts?: number
  heartbeatInterval?: number
  heartbeatMessage?: string
}

interface UseWebSocketReturn {
  sendMessage: (message: string) => void
  disconnect: () => void
  reconnect: () => void
  readyState: number
  isConnected: boolean
}

/**
 * Enhanced WebSocket hook with reconnection and heartbeat
 */
export function useWebSocket(
  url: string | null,
  options: UseWebSocketOptions = {}
): UseWebSocketReturn {
  const {
    onOpen,
    onMessage,
    onClose,
    onError,
    reconnect = true,
    reconnectInterval = 3000,
    reconnectAttempts = 5,
    heartbeatInterval = 30000,
    heartbeatMessage = 'ping',
  } = options

  const [readyState, setReadyState] = useState<number>(WebSocket.CONNECTING)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectCountRef = useRef(0)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  const heartbeatTimeoutRef = useRef<NodeJS.Timeout>()
  const shouldReconnectRef = useRef(true)

  const isConnected = readyState === WebSocket.OPEN

  // Send heartbeat
  const sendHeartbeat = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(heartbeatMessage)
      
      heartbeatTimeoutRef.current = setTimeout(() => {
        sendHeartbeat()
      }, heartbeatInterval)
    }
  }, [heartbeatMessage, heartbeatInterval])

  // Connect to WebSocket
  const connect = useCallback(() => {
    if (!url || wsRef.current?.readyState === WebSocket.OPEN) {
      return
    }

    try {
      const ws = new WebSocket(url)

      ws.onopen = (event) => {
        console.log('WebSocket connected')
        setReadyState(WebSocket.OPEN)
        reconnectCountRef.current = 0
        
        // Start heartbeat
        sendHeartbeat()
        
        onOpen?.(event)
      }

      ws.onmessage = (event) => {
        // Ignore pong messages
        if (event.data === 'pong') {
          return
        }
        
        onMessage?.(event)
      }

      ws.onclose = (event) => {
        console.log('WebSocket disconnected')
        setReadyState(WebSocket.CLOSED)
        
        // Clear heartbeat
        if (heartbeatTimeoutRef.current) {
          clearTimeout(heartbeatTimeoutRef.current)
        }
        
        onClose?.(event)

        // Attempt reconnection
        if (
          shouldReconnectRef.current &&
          reconnect &&
          reconnectCountRef.current < reconnectAttempts
        ) {
          reconnectCountRef.current++
          console.log(
            `Reconnecting... (${reconnectCountRef.current}/${reconnectAttempts})`
          )
          
          reconnectTimeoutRef.current = setTimeout(() => {
            connect()
          }, reconnectInterval)
        }
      }

      ws.onerror = (event) => {
        console.error('WebSocket error:', event)
        onError?.(event)
      }

      wsRef.current = ws
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
    }
  }, [url, onOpen, onMessage, onClose, onError, reconnect, reconnectInterval, reconnectAttempts, sendHeartbeat])

  // Send message
  const sendMessage = useCallback((message: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(message)
    } else {
      console.warn('WebSocket is not connected')
    }
  }, [])

  // Disconnect
  const disconnect = useCallback(() => {
    shouldReconnectRef.current = false
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    
    if (heartbeatTimeoutRef.current) {
      clearTimeout(heartbeatTimeoutRef.current)
    }
    
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }, [])

  // Manual reconnect
  const reconnectManually = useCallback(() => {
    disconnect()
    shouldReconnectRef.current = true
    reconnectCountRef.current = 0
    connect()
  }, [disconnect, connect])

  // Connect on mount
  useEffect(() => {
    if (url) {
      connect()
    }

    return () => {
      disconnect()
    }
  }, [url])

  return {
    sendMessage,
    disconnect,
    reconnect: reconnectManually,
    readyState,
    isConnected,
  }
}
