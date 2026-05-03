"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Check, Loader2, RefreshCw, X } from "lucide-react";
import api from "@/lib/api";
import type { ApprovalDecisionRecord } from "@/types";
import { extractApiError } from "@/lib/utils";

interface DecisionButtonsProps {
  clauseId: string;
  currentStatus: string;
  onDecided: (record: ApprovalDecisionRecord) => void;
}

export default function DecisionButtons({
  clauseId,
  currentStatus,
  onDecided,
}: DecisionButtonsProps) {
  const [busy, setBusy] = useState(false);
  const [comment, setComment] = useState("");
  const [showComment, setShowComment] = useState(false);
  const [pendingDecision, setPendingDecision] = useState<string | null>(null);

  const canDecide = currentStatus === "in_review" || currentStatus === "draft";

  async function decide(decision: string) {
    setBusy(true);
    try {
      const { data } = await api.post<ApprovalDecisionRecord>(
        `/clauses/${clauseId}/decide`,
        { decision, comment: comment || null },
      );
      onDecided(data);
      setComment("");
      setShowComment(false);
      setPendingDecision(null);
      const label = { approved: "Onaylandı", rejected: "Reddedildi", revise: "Revize işaretlendi" }[decision];
      toast.success(label ?? "Karar kaydedildi.");
    } catch (err: any) {
      toast.error(extractApiError(err, "Karar kaydedilemedi."));
    } finally {
      setBusy(false);
    }
  }

  function startDecision(d: string) {
    setPendingDecision(d);
    setShowComment(true);
  }

  if (!canDecide) return null;

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap gap-2">
        <button
          disabled={busy}
          onClick={() => startDecision("approved")}
          className="flex items-center gap-1.5 rounded-lg bg-green-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-green-700 disabled:opacity-50"
        >
          <Check className="h-3.5 w-3.5" /> Onayla
        </button>
        <button
          disabled={busy}
          onClick={() => startDecision("rejected")}
          className="flex items-center gap-1.5 rounded-lg bg-red-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-700 disabled:opacity-50"
        >
          <X className="h-3.5 w-3.5" /> Reddet
        </button>
        <button
          disabled={busy}
          onClick={() => startDecision("revise")}
          className="flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-semibold text-gray-600 hover:bg-gray-50 disabled:opacity-50"
        >
          <RefreshCw className="h-3.5 w-3.5" /> Revize
        </button>
      </div>

      {showComment && (
        <div className="space-y-2">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Yorum (isteğe bağlı)..."
            rows={2}
            className="w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          />
          <div className="flex gap-2">
            <button
              disabled={busy}
              onClick={() => pendingDecision && decide(pendingDecision)}
              className="flex items-center gap-1.5 rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
            >
              {busy ? <Loader2 className="h-3 w-3 animate-spin" /> : <Check className="h-3 w-3" />}
              Onayla
            </button>
            <button
              onClick={() => { setShowComment(false); setPendingDecision(null); }}
              className="rounded-lg border px-3 py-1.5 text-xs font-semibold text-gray-600 hover:bg-gray-50"
            >
              İptal
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
