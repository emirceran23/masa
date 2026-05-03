"use client";

import type { ClauseDetail } from "@/types";
import { cn, categoryLabel, riskColor } from "@/lib/utils";
import { ShieldAlert, CheckCircle2, XCircle } from "lucide-react";
import ApprovalPanel from "@/components/approval/approval-panel";

interface ClauseDetailPanelProps {
  clause: ClauseDetail;
}

export default function ClauseDetailPanel({ clause }: ClauseDetailPanelProps) {
  const risk = clause.risk_assessment;

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs font-semibold text-gray-500">
            Madde #{clause.sequence_no}
          </span>
          <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
            {categoryLabel(clause.category)}
          </span>
        </div>
        <p className="text-sm leading-relaxed text-gray-800">
          {clause.original_text}
        </p>
      </div>

      {/* Risk Assessment */}
      {risk && (
        <div className="rounded-xl border p-4 space-y-3">
          <h4 className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <ShieldAlert className="h-4 w-4" />
            Risk Değerlendirmesi
          </h4>

          <div className="flex gap-3">
            <span
              className={cn(
                "rounded-full px-3 py-1 text-xs font-semibold capitalize",
                riskColor(risk.risk_level)
              )}
            >
              {risk.risk_level}
            </span>
            <span className="text-xs text-gray-500">
              Ticari: {(risk.commercial_score * 100).toFixed(0)}% | Hukuki:{" "}
              {(risk.legal_score * 100).toFixed(0)}%
            </span>
          </div>

          {risk.rationale && (
            <p className="text-sm text-gray-600">{risk.rationale}</p>
          )}

          <div className="flex items-center gap-4 text-xs">
            <span className="flex items-center gap-1">
              {risk.policy_compliance ? (
                <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
              ) : (
                <XCircle className="h-3.5 w-3.5 text-red-500" />
              )}
              Politika Uyumu
            </span>
            <span className="flex items-center gap-1">
              {risk.cross_validated ? (
                <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />
              ) : (
                <XCircle className="h-3.5 w-3.5 text-gray-400" />
              )}
              Çapraz Doğrulama
            </span>
          </div>
        </div>
      )}

      {/* Approval panel — shown when clause needs a decision */}
      {(clause.status === "in_review" || clause.status === "draft") && (
        <div className="rounded-xl border">
          <div className="border-b px-4 py-2 bg-gray-50">
            <h4 className="text-sm font-semibold text-gray-700">Onay Akışı</h4>
          </div>
          <ApprovalPanel
            clause={clause}
            riskLevel={clause.risk_assessment?.risk_level}
          />
        </div>
      )}

      {/* Revisions */}
      {clause.revisions.length > 0 && (
        <div className="rounded-xl border p-4 space-y-3">
          <h4 className="text-sm font-semibold text-gray-700">
            Revizyon Önerileri
          </h4>
          {clause.revisions.map((rev) => (
            <div key={rev.id} className="rounded-lg bg-gray-50 p-3 text-sm">
              <p className="text-gray-700">{rev.suggested_text}</p>
              {rev.diff_html && (
                <div
                  className="mt-2 text-xs"
                  dangerouslySetInnerHTML={{ __html: rev.diff_html }}
                />
              )}
              <span className="mt-2 inline-block rounded-full bg-gray-200 px-2 py-0.5 text-xs text-gray-600">
                {rev.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
