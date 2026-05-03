"use client";

import type { ApprovalDecisionRecord } from "@/types";
import { formatDate } from "@/lib/utils";
import { Check, RefreshCw, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface AuditTimelineProps {
  decisions: ApprovalDecisionRecord[];
}

const DECISION_META: Record<
  string,
  { icon: typeof Check; color: string; label: string }
> = {
  approved: { icon: Check, color: "text-green-600 bg-green-50 border-green-200", label: "Onaylandı" },
  rejected: { icon: X, color: "text-red-600 bg-red-50 border-red-200", label: "Reddedildi" },
  revise: { icon: RefreshCw, color: "text-amber-600 bg-amber-50 border-amber-200", label: "Revize" },
};

export default function AuditTimeline({ decisions }: AuditTimelineProps) {
  if (decisions.length === 0) return null;

  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold uppercase tracking-wide text-gray-400">
        Karar Geçmişi
      </p>
      <ol className="relative border-l border-gray-200 ml-2 space-y-4">
        {decisions.map((d) => {
          const meta = DECISION_META[d.decision] ?? DECISION_META.approved;
          const { icon: Icon } = meta;
          return (
            <li key={d.id} className="ml-4">
              <span
                className={cn(
                  "absolute -left-3 flex h-6 w-6 items-center justify-center rounded-full border",
                  meta.color,
                )}
              >
                <Icon className="h-3 w-3" />
              </span>
              <div className="rounded-lg border bg-white px-3 py-2 shadow-sm">
                <div className="flex items-center justify-between">
                  <span
                    className={cn(
                      "rounded-full border px-2 py-0.5 text-[11px] font-semibold",
                      meta.color,
                    )}
                  >
                    {meta.label}
                  </span>
                  <time className="text-[11px] text-gray-400">
                    {formatDate(d.decided_at)}
                  </time>
                </div>
                {d.comment && (
                  <p className="mt-1 text-xs text-gray-600">{d.comment}</p>
                )}
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
