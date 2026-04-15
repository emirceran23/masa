import type { AnalysisProgress } from "@/types";

const WS_BASE = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export function connectAnalysisWS(
  contractId: string,
  onProgress: (data: AnalysisProgress) => void,
  onClose?: () => void
): WebSocket {
  const ws = new WebSocket(`${WS_BASE}/api/v1/ws/${contractId}`);

  ws.onmessage = (event) => {
    try {
      const data: AnalysisProgress = JSON.parse(event.data);
      onProgress(data);
    } catch {
      console.warn("Invalid WS message:", event.data);
    }
  };

  ws.onclose = () => onClose?.();
  ws.onerror = (err) => console.error("WS error:", err);

  return ws;
}
