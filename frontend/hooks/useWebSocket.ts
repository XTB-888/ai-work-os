"use client";
import { useEffect, useRef, useCallback, useState } from "react";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export function useWebSocket(projectId: string | undefined) {
  const wsRef = useRef<WebSocket | null>(null);
  const [lastEvent, setLastEvent] = useState<any>(null);

  const connect = useCallback(() => {
    if (!projectId) return;
    const ws = new WebSocket(`${WS_URL}/ws/projects/${projectId}`);
    ws.onmessage = (e) => {
      try {
        setLastEvent(JSON.parse(e.data));
      } catch {}
    };
    ws.onclose = () => {
      // reconnect after 3s
      setTimeout(connect, 3000);
    };
    wsRef.current = ws;
  }, [projectId]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  return { lastEvent };
}
