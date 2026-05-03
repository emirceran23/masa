"use client";

import type { Report } from "@/types";
import { formatDate } from "@/lib/utils";
import { Download, FileText } from "lucide-react";
import { cn } from "@/lib/utils";

interface ReportSummaryCardProps {
  report: Report;
  onDownload: (report: Report) => void;
}

const RISK_COLORS: Record<string, string> = {
  high:       "bg-red-500",
  medium:     "bg-orange-500",
  low:        "bg-green-500",
  unassessed: "bg-gray-400",
};

const RISK_LABELS: Record<string, string> = {
  high:       "Yüksek",
  medium:     "Orta",
  low:        "Düşük",
  unassessed: "Değerlendirilmedi",
};

const TYPE_LABELS: Record<string, string> = {
  summary:  "Özet Rapor",
  detailed: "Detaylı Rapor",
};

export default function ReportSummaryCard({
  report,
  onDownload,
}: ReportSummaryCardProps) {
  const sd = report.summary_data;
  const isDocx = report.storage_path?.endsWith(".docx");
  const fmt = isDocx ? "DOCX" : "PDF";

  return (
    <div className="rounded-xl border bg-white p-4 space-y-3">
      {/* Header row */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-brand-500 shrink-0" />
          <div>
            <p className="text-sm font-semibold text-gray-800">
              {TYPE_LABELS[report.report_type] ?? report.report_type} — {fmt}
            </p>
            <p className="text-xs text-gray-400">{formatDate(report.created_at)}</p>
          </div>
        </div>
        <button
          onClick={() => onDownload(report)}
          className="flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-semibold text-gray-600 hover:bg-gray-50 transition shrink-0"
        >
          <Download className="h-3.5 w-3.5" />
          İndir
        </button>
      </div>

      {/* Summary stats */}
      {sd && (
        <>
          {/* Risk mini-bar */}
          {report.total_clauses != null && report.total_clauses > 0 && (
            <div className="space-y-1">
              <p className="text-xs text-gray-500">
                Risk Dağılımı — {report.total_clauses} madde
              </p>
              <div className="flex h-2 w-full overflow-hidden rounded-full bg-gray-100">
                {(["high", "medium", "low", "unassessed"] as const).map((level) => {
                  const count = sd.risk_counts[level] ?? 0;
                  const pct = (count / report.total_clauses!) * 100;
                  if (pct === 0) return null;
                  return (
                    <div
                      key={level}
                      title={`${RISK_LABELS[level]}: ${count}`}
                      className={cn("h-full", RISK_COLORS[level])}
                      style={{ width: `${pct}%` }}
                    />
                  );
                })}
              </div>
              <div className="flex flex-wrap gap-x-3 gap-y-0.5">
                {(["high", "medium", "low"] as const).map((level) => {
                  const count = sd.risk_counts[level] ?? 0;
                  if (count === 0) return null;
                  return (
                    <span key={level} className="text-[11px] text-gray-500">
                      <span
                        className={cn(
                          "inline-block h-2 w-2 rounded-full mr-1",
                          RISK_COLORS[level]
                        )}
                      />
                      {RISK_LABELS[level]}: {count}
                    </span>
                  );
                })}
              </div>
            </div>
          )}

          {/* Highlights */}
          <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-500">
            {sd.missing_provisions_count > 0 && (
              <span className="text-amber-600 font-medium">
                ⚠ {sd.missing_provisions_count} eksik hüküm
              </span>
            )}
            {(sd.revision_counts?.accepted ?? 0) > 0 && (
              <span className="text-green-600">
                ✓ {sd.revision_counts.accepted} revizyon kabul edildi
              </span>
            )}
            {(sd.revision_counts?.pending ?? 0) > 0 && (
              <span>
                ⏳ {sd.revision_counts.pending} revizyon bekliyor
              </span>
            )}
          </div>
        </>
      )}
    </div>
  );
}
