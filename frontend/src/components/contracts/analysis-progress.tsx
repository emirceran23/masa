"use client";

import { useState, useEffect } from "react";
import { Loader2 } from "lucide-react";
import { connectAnalysisWS } from "@/lib/websocket";
import type { AnalysisProgress } from "@/types";

interface AnalysisProgressBarProps {
  contractId: string;
  onComplete?: () => void;
}

export default function AnalysisProgressBar({
  contractId,
  onComplete,
}: AnalysisProgressBarProps) {
  const [progress, setProgress] = useState<AnalysisProgress | null>(null);

  useEffect(() => {
    const ws = connectAnalysisWS(
      contractId,
      (data) => {
        setProgress(data);
        if (data.status === "completed") {
          onComplete?.();
        }
      },
      () => setProgress(null)
    );

    return () => ws.close();
  }, [contractId, onComplete]);

  if (!progress) return null;

  const pct = Math.round(progress.progress * 100);

  return (
    <div className="rounded-xl border bg-white p-4 space-y-2">
      <div className="flex items-center gap-2 text-sm text-gray-700">
        <Loader2 className="h-4 w-4 animate-spin text-brand-600" />
        <span>{progress.message || "Analiz ediliyor…"}</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
        <div
          className="h-full rounded-full bg-brand-500 transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-xs text-gray-400">{pct}%</span>
    </div>
  );
}
