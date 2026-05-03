"use client";

import { cn } from "@/lib/utils";

interface RiskChartProps {
  counts: { low: number; medium: number; high: number };
  title?: string;
  className?: string;
}

const SEGMENTS = [
  { key: "high" as const, label: "Yüksek", color: "bg-red-500" },
  { key: "medium" as const, label: "Orta", color: "bg-amber-400" },
  { key: "low" as const, label: "Düşük", color: "bg-green-500" },
];

export default function RiskChart({ counts, title, className }: RiskChartProps) {
  const total = counts.low + counts.medium + counts.high;

  return (
    <div className={cn("rounded-xl border bg-white p-5 space-y-4", className)}>
      {title && <h3 className="text-sm font-semibold text-gray-700">{title}</h3>}

      {total === 0 ? (
        <div className="py-6 text-center text-sm text-gray-400">
          Henüz risk değerlendirmesi yok.
        </div>
      ) : (
        <>
          <div className="flex h-3 overflow-hidden rounded-full bg-gray-100">
            {SEGMENTS.map((s) => {
              const pct = total > 0 ? (counts[s.key] / total) * 100 : 0;
              if (pct === 0) return null;
              return (
                <div
                  key={s.key}
                  className={s.color}
                  style={{ width: `${pct}%` }}
                  title={`${s.label}: ${counts[s.key]} (${pct.toFixed(1)}%)`}
                />
              );
            })}
          </div>

          <div className="grid grid-cols-3 gap-3">
            {SEGMENTS.map((s) => {
              const pct = total > 0 ? (counts[s.key] / total) * 100 : 0;
              return (
                <div
                  key={s.key}
                  className="rounded-lg border bg-gray-50 px-3 py-2"
                >
                  <div className="flex items-center gap-2">
                    <span className={cn("h-2 w-2 rounded-full", s.color)} />
                    <span className="text-xs text-gray-600">{s.label}</span>
                  </div>
                  <div className="mt-1 flex items-baseline gap-1">
                    <span className="text-lg font-bold text-gray-800">
                      {counts[s.key]}
                    </span>
                    <span className="text-[11px] text-gray-500">
                      %{pct.toFixed(0)}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
