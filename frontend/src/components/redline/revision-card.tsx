"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Check, Loader2, Pencil, X } from "lucide-react";
import api from "@/lib/api";
import type { Clause, RevisionDetail } from "@/types";
import DiffViewer from "./diff-viewer";
import { categoryLabel, cn, extractApiError } from "@/lib/utils";
import RiskBadge from "@/components/contract/risk-badge";

interface RevisionCardProps {
  revision: RevisionDetail;
  clause: Clause;
  riskLevel?: string;
  onUpdated: (updated: RevisionDetail) => void;
}

export default function RevisionCard({
  revision,
  clause,
  riskLevel,
  onUpdated,
}: RevisionCardProps) {
  const [editing, setEditing] = useState(false);
  const [editedText, setEditedText] = useState(
    revision.edited_text ?? revision.suggested_text,
  );
  const [busy, setBusy] = useState(false);

  const isPending = revision.status === "pending";

  async function act(
    action: "accept" | "reject" | "edit",
    body?: object,
  ) {
    setBusy(true);
    try {
      const { data } = await api.post<RevisionDetail>(
        `/revisions/${revision.id}/${action}`,
        body ?? {},
      );
      onUpdated(data);
      setEditing(false);
      toast.success(
        action === "accept"
          ? "Revizyon kabul edildi."
          : action === "reject"
          ? "Revizyon reddedildi."
          : "Düzenleme kaydedildi.",
      );
    } catch (err: any) {
      toast.error(extractApiError(err, "İşlem başarısız."));
    } finally {
      setBusy(false);
    }
  }

  const statusBadge: Record<string, string> = {
    pending: "bg-amber-50 text-amber-700 border-amber-200",
    accepted: "bg-green-50 text-green-700 border-green-200",
    rejected: "bg-red-50 text-red-700 border-red-200",
    edited: "bg-blue-50 text-blue-700 border-blue-200",
  };
  const statusLabel: Record<string, string> = {
    pending: "Beklemede",
    accepted: "Kabul Edildi",
    rejected: "Reddedildi",
    edited: "Düzenlendi",
  };

  return (
    <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
      {/* Clause header */}
      <div className="flex items-center justify-between gap-2 border-b bg-gray-50 px-4 py-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-gray-500">
            Madde #{clause.sequence_no}
          </span>
          <span className="rounded-full bg-gray-200 px-2 py-0.5 text-xs text-gray-600">
            {categoryLabel(clause.category)}
          </span>
          {riskLevel && <RiskBadge level={riskLevel} size="sm" />}
        </div>
        <span
          className={cn(
            "rounded-full border px-2 py-0.5 text-[11px] font-semibold",
            statusBadge[revision.status] ?? "bg-gray-50 text-gray-600",
          )}
        >
          {statusLabel[revision.status] ?? revision.status}
        </span>
      </div>

      <div className="p-4 space-y-4">
        {/* Original */}
        <div>
          <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-gray-400">
            Orijinal
          </p>
          <p className="rounded-lg bg-red-50/60 px-3 py-2 text-sm text-gray-700 leading-relaxed">
            {clause.original_text}
          </p>
        </div>

        {/* Diff / suggested */}
        {!editing && (
          <div>
            <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-gray-400">
              {revision.status === "edited" ? "Düzenlenmiş Metin" : "Önerilen"}
            </p>
            {revision.diff_html ? (
              <div className="rounded-lg bg-gray-50 px-3 py-2">
                <DiffViewer diffHtml={revision.diff_html} />
              </div>
            ) : (
              <p className="rounded-lg bg-green-50 px-3 py-2 text-sm text-green-900 leading-relaxed">
                {revision.edited_text ?? revision.suggested_text}
              </p>
            )}
            {revision.context_used && (
              <p className="mt-1 text-xs italic text-gray-400">
                {revision.context_used}
              </p>
            )}
          </div>
        )}

        {/* Inline editor */}
        {editing && (
          <div>
            <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-gray-400">
              Metni Düzenle
            </p>
            <textarea
              value={editedText}
              onChange={(e) => setEditedText(e.target.value)}
              rows={5}
              className="w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            />
          </div>
        )}

        {/* Actions */}
        {isPending && (
          <div className="flex flex-wrap items-center gap-2 pt-1">
            {!editing ? (
              <>
                <button
                  disabled={busy}
                  onClick={() => act("accept")}
                  className="flex items-center gap-1.5 rounded-lg bg-green-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-green-700 disabled:opacity-50"
                >
                  {busy ? <Loader2 className="h-3 w-3 animate-spin" /> : <Check className="h-3 w-3" />}
                  Kabul Et
                </button>
                <button
                  disabled={busy}
                  onClick={() => act("reject")}
                  className="flex items-center gap-1.5 rounded-lg bg-red-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-700 disabled:opacity-50"
                >
                  <X className="h-3 w-3" /> Reddet
                </button>
                <button
                  disabled={busy}
                  onClick={() => { setEditedText(revision.suggested_text); setEditing(true); }}
                  className="flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-semibold text-gray-600 hover:bg-gray-50 disabled:opacity-50"
                >
                  <Pencil className="h-3 w-3" /> Düzenle
                </button>
              </>
            ) : (
              <>
                <button
                  disabled={busy}
                  onClick={() => act("edit", { edited_text: editedText })}
                  className="flex items-center gap-1.5 rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
                >
                  {busy ? <Loader2 className="h-3 w-3 animate-spin" /> : <Check className="h-3 w-3" />}
                  Kaydet
                </button>
                <button
                  disabled={busy}
                  onClick={() => setEditing(false)}
                  className="rounded-lg border px-3 py-1.5 text-xs font-semibold text-gray-600 hover:bg-gray-50"
                >
                  İptal
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
