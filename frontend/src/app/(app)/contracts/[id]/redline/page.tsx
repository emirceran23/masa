"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Loader2 } from "lucide-react";
import { toast } from "sonner";
import api from "@/lib/api";
import type { Clause, ClauseListResponse, ContractDetail, RevisionDetail, RiskAssessmentDetail } from "@/types";
import RevisionCard from "@/components/redline/revision-card";
import { extractApiError } from "@/lib/utils";

export default function RedlinePage() {
  const { id } = useParams<{ id: string }>();

  const [contract, setContract] = useState<ContractDetail | null>(null);
  const [clauses, setClauses] = useState<Clause[]>([]);
  const [revisions, setRevisions] = useState<RevisionDetail[]>([]);
  const [riskLevels, setRiskLevels] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  const fetchAll = useCallback(async () => {
    try {
      const [contractRes, clausesRes, revisionsRes, risksRes] =
        await Promise.all([
          api.get<ContractDetail>(`/contracts/${id}`),
          api.get<ClauseListResponse>(`/clauses/by-contract/${id}`),
          api.get<RevisionDetail[]>(`/contracts/${id}/revisions`),
          api.get<RiskAssessmentDetail[]>(`/contracts/${id}/risks`),
        ]);
      setContract(contractRes.data);
      setClauses(clausesRes.data.items);
      setRevisions(revisionsRes.data);
      const lvls: Record<string, string> = {};
      risksRes.data.forEach((r) => { lvls[r.clause_id] = r.risk_level; });
      setRiskLevels(lvls);
    } catch (err: any) {
      toast.error(extractApiError(err, "Veriler yüklenemedi."));
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  const clauseMap = useMemo(() => {
    const m = new Map<string, Clause>();
    clauses.forEach((c) => m.set(c.id, c));
    return m;
  }, [clauses]);

  function handleRevisionUpdated(updated: RevisionDetail) {
    setRevisions((prev) =>
      prev.map((r) => (r.id === updated.id ? updated : r)),
    );
  }

  const pendingCount = revisions.filter((r) => r.status === "pending").length;

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-brand-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link
          href={`/contracts/${id}`}
          className="rounded-lg p-2 hover:bg-gray-100 transition"
        >
          <ArrowLeft className="h-5 w-5 text-gray-500" />
        </Link>
        <div>
          <h1 className="text-xl font-bold text-gray-800">
            Redline — {contract?.file_name ?? "Sözleşme"}
          </h1>
          <p className="text-xs text-gray-400">
            {revisions.length} revizyon önerisi · {pendingCount} beklemede
          </p>
        </div>
      </div>

      {revisions.length === 0 ? (
        <div className="rounded-xl border bg-white p-10 text-center text-sm text-gray-400">
          Bu sözleşme için henüz revizyon önerisi oluşturulmamış.
          <br />
          Analizi çalıştırın veya tüm maddeler düşük risk olabilir.
        </div>
      ) : (
        <div className="space-y-4">
          {revisions.map((rev) => {
            const clause = clauseMap.get(rev.clause_id);
            if (!clause) return null;
            return (
              <RevisionCard
                key={rev.id}
                revision={rev}
                clause={clause}
                riskLevel={riskLevels[rev.clause_id]}
                onUpdated={handleRevisionUpdated}
              />
            );
          })}
        </div>
      )}
    </div>
  );
}
