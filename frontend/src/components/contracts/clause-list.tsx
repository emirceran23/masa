"use client";

import type { Clause } from "@/types";
import { cn, categoryLabel } from "@/lib/utils";
import { ChevronRight } from "lucide-react";
import RiskBadge from "@/components/contract/risk-badge";

interface ClauseListProps {
  clauses: Clause[];
  selectedId?: string;
  onSelect: (clause: Clause) => void;
  riskLevels?: Record<string, string>;
}

export default function ClauseList({
  clauses,
  selectedId,
  onSelect,
  riskLevels,
}: ClauseListProps) {
  if (clauses.length === 0) {
    return (
      <div className="flex items-center justify-center p-10 text-sm text-gray-400">
        Henüz madde bulunamadı.
      </div>
    );
  }

  return (
    <div className="divide-y">
      {clauses.map((clause) => (
        <button
          key={clause.id}
          onClick={() => onSelect(clause)}
          className={cn(
            "flex w-full items-center justify-between px-4 py-3 text-left transition hover:bg-gray-50",
            selectedId === clause.id && "bg-brand-50"
          )}
        >
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-semibold text-gray-500">
                #{clause.sequence_no}
              </span>
              <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
                {categoryLabel(clause.category)}
              </span>
              <span className="text-xs text-gray-400">
                {(clause.confidence_score * 100).toFixed(0)}%
              </span>
              {riskLevels?.[clause.id] && (
                <RiskBadge level={riskLevels[clause.id]} size="sm" withIcon={false} />
              )}
            </div>
            <p className="truncate text-sm text-gray-700">
              {clause.original_text}
            </p>
          </div>
          <ChevronRight className="ml-2 h-4 w-4 flex-shrink-0 text-gray-300" />
        </button>
      ))}
    </div>
  );
}
