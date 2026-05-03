"use client";

import { useCallback, useEffect, useState } from "react";
import { Loader2 } from "lucide-react";
import api from "@/lib/api";
import type { ApprovalDecisionRecord, Clause } from "@/types";
import DecisionButtons from "./decision-buttons";
import AuditTimeline from "./audit-timeline";
import { categoryLabel, statusLabel } from "@/lib/utils";
import RiskBadge from "@/components/contract/risk-badge";

interface ApprovalPanelProps {
  clause: Clause;
  riskLevel?: string;
  onStatusChange?: (clauseId: string, newStatus: string) => void;
}

export default function ApprovalPanel({
  clause,
  riskLevel,
  onStatusChange,
}: ApprovalPanelProps) {
  const [decisions, setDecisions] = useState<ApprovalDecisionRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const loadDecisions = useCallback(async () => {
    try {
      const { data } = await api.get<ApprovalDecisionRecord[]>(
        `/clauses/${clause.id}/decisions`,
      );
      setDecisions(data);
    } catch {
      setDecisions([]);
    } finally {
      setLoading(false);
    }
  }, [clause.id]);

  useEffect(() => { loadDecisions(); }, [loadDecisions]);

  function handleDecided(record: ApprovalDecisionRecord) {
    setDecisions((prev) => [...prev, record]);
    const newStatus =
      record.decision === "approved"
        ? "approved"
        : record.decision === "rejected"
        ? "rejected"
        : "in_review";
    onStatusChange?.(clause.id, newStatus);
  }

  return (
    <div className="space-y-4 p-4">
      {/* Clause info */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-sm font-semibold text-gray-700">
          Madde #{clause.sequence_no}
        </span>
        <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
          {categoryLabel(clause.category)}
        </span>
        {riskLevel && <RiskBadge level={riskLevel} size="sm" />}
        <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs text-blue-700 border border-blue-200">
          {statusLabel(clause.status)}
        </span>
      </div>

      {/* Decision buttons */}
      <DecisionButtons
        clauseId={clause.id}
        currentStatus={clause.status}
        onDecided={handleDecided}
      />

      {/* History */}
      {loading ? (
        <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
      ) : (
        <AuditTimeline decisions={decisions} />
      )}
    </div>
  );
}
