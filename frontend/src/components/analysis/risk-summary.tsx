"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertCircle, Loader2 } from "lucide-react";
import api from "@/lib/api";
import type {
  Clause,
  MissingProvision,
  RiskAssessmentDetail,
} from "@/types";
import RiskBadge from "@/components/contract/risk-badge";
import RiskChart from "./risk-chart";
import { cn } from "@/lib/utils";

interface Props {
  contractId: string;
  clauses: Clause[];
  onFocusClause?: (clauseId: string) => void;
}

export default function RiskSummary({ contractId, clauses, onFocusClause }: Props) {
  const [risks, setRisks] = useState<RiskAssessmentDetail[]>([]);
  const [missing, setMissing] = useState<MissingProvision[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      try {
        const [riskRes, missingRes] = await Promise.all([
          api.get<RiskAssessmentDetail[]>(`/contracts/${contractId}/risks`),
          api.get<MissingProvision[]>(
            `/contracts/${contractId}/missing-provisions`,
          ),
        ]);
        if (cancelled) return;
        setRisks(riskRes.data);
        setMissing(missingRes.data);
      } catch {
        // endpoints may return empty / 404 if analysis not yet run
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [contractId]);

  const counts = useMemo(() => {
    const base = { low: 0, medium: 0, high: 0 };
    risks.forEach((r) => {
      if (r.risk_level === "low") base.low += 1;
      else if (r.risk_level === "medium") base.medium += 1;
      else if (r.risk_level === "high") base.high += 1;
    });
    return base;
  }, [risks]);

  const highRisks = useMemo(
    () => risks.filter((r) => r.risk_level === "high"),
    [risks],
  );

  const clauseBySeq = useMemo(() => {
    const map = new Map<string, Clause>();
    clauses.forEach((c) => map.set(c.id, c));
    return map;
  }, [clauses]);

  if (loading) {
    return (
      <div className="flex items-center justify-center rounded-xl border bg-white py-10">
        <Loader2 className="h-6 w-6 animate-spin text-brand-500" />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <RiskChart counts={counts} title="Risk Dağılımı" />

      {highRisks.length > 0 && (
        <div className="rounded-xl border bg-white p-5 space-y-3">
          <h3 className="text-sm font-semibold text-gray-700">
            Yüksek Riskli Maddeler ({highRisks.length})
          </h3>
          <ul className="space-y-2">
            {highRisks.map((r) => {
              const clause = clauseBySeq.get(r.clause_id);
              return (
                <li
                  key={r.id}
                  className={cn(
                    "rounded-lg border border-red-200 bg-red-50/60 p-3 text-sm",
                    onFocusClause && "cursor-pointer hover:bg-red-50",
                  )}
                  onClick={() => onFocusClause?.(r.clause_id)}
                >
                  <div className="flex items-center gap-2">
                    <RiskBadge level={r.risk_level} />
                    {clause && (
                      <span className="text-xs text-gray-500">
                        Madde #{clause.sequence_no}
                      </span>
                    )}
                  </div>
                  <p className="mt-1 line-clamp-2 text-gray-700">
                    {clause?.original_text ?? "—"}
                  </p>
                  <p className="mt-1 text-xs italic text-gray-500">
                    {r.rationale}
                  </p>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {missing.length > 0 && (
        <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-5 space-y-3">
          <h3 className="flex items-center gap-2 text-sm font-semibold text-amber-800">
            <AlertCircle className="h-4 w-4" />
            Eksik Hükümler ({missing.length})
          </h3>
          <ul className="space-y-2">
            {missing.map((m) => (
              <li
                key={m.id}
                className="rounded-lg bg-white/70 p-3 text-sm text-gray-700"
              >
                {m.description}
              </li>
            ))}
          </ul>
        </div>
      )}

      {risks.length === 0 && (
        <div className="rounded-xl border bg-white p-6 text-center text-sm text-gray-400">
          Bu sözleşme için risk değerlendirmesi bulunamadı.
        </div>
      )}
    </div>
  );
}
