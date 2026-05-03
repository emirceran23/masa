"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { toast } from "sonner";
import { ArrowLeft, FileEdit, FileText, Loader2 } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";
import type {
  ContractDetail,
  Clause,
  ClauseDetail,
  ClauseListResponse,
  RiskAssessmentDetail,
} from "@/types";
import { statusLabel, formatDate, formatFileSize } from "@/lib/utils";
import ClauseList from "@/components/contracts/clause-list";
import ClauseDetailPanel from "@/components/contracts/clause-detail-panel";
import AnalysisProgressBar from "@/components/contracts/analysis-progress";
import RiskSummary from "@/components/analysis/risk-summary";

export default function ContractDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [contract, setContract] = useState<ContractDetail | null>(null);
  const [clauses, setClauses] = useState<Clause[]>([]);
  const [selectedClause, setSelectedClause] = useState<ClauseDetail | null>(
    null
  );
  const [riskLevels, setRiskLevels] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  const fetchContract = useCallback(async () => {
    try {
      const { data } = await api.get<ContractDetail>(`/contracts/${id}`);
      setContract(data);
    } catch {
      toast.error("Sözleşme yüklenemedi.");
    }
  }, [id]);

  const fetchClauses = useCallback(async () => {
    try {
      const { data } = await api.get<ClauseListResponse>(
        `/clauses/by-contract/${id}`
      );
      setClauses(data.items);
    } catch {
      // Clauses might not exist yet
    }
  }, [id]);

  const fetchRiskLevels = useCallback(async () => {
    try {
      const { data } = await api.get<RiskAssessmentDetail[]>(
        `/contracts/${id}/risks`,
      );
      const map: Record<string, string> = {};
      data.forEach((r) => {
        map[r.clause_id] = r.risk_level;
      });
      setRiskLevels(map);
    } catch {
      setRiskLevels({});
    }
  }, [id]);

  useEffect(() => {
    Promise.all([fetchContract(), fetchClauses(), fetchRiskLevels()]).finally(
      () => setLoading(false),
    );
  }, [fetchContract, fetchClauses, fetchRiskLevels]);

  // Poll contract status while processing so the progress bar appears.
  useEffect(() => {
    if (contract?.status !== "processing") return;
    const interval = setInterval(fetchContract, 3000);
    return () => clearInterval(interval);
  }, [contract?.status, fetchContract]);

  async function handleSelectClause(clause: Clause) {
    try {
      const { data } = await api.get<ClauseDetail>(`/clauses/${clause.id}`);
      setSelectedClause(data);
    } catch {
      toast.error("Madde detayı yüklenemedi.");
    }
  }

  function handleAnalysisComplete() {
    fetchContract();
    fetchClauses();
    fetchRiskLevels();
    toast.success("Analiz tamamlandı!");
  }

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-brand-500" />
      </div>
    );
  }

  if (!contract) {
    return (
      <div className="text-center py-20 text-gray-400">
        Sözleşme bulunamadı.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link
          href="/contracts"
          className="rounded-lg p-2 hover:bg-gray-100 transition"
        >
          <ArrowLeft className="h-5 w-5 text-gray-500" />
        </Link>
        <div className="flex-1">
          <h1 className="text-xl font-bold text-gray-800">
            {contract.file_name}
          </h1>
          <p className="text-xs text-gray-400">
            {formatFileSize(contract.file_size)} •{" "}
            {formatDate(contract.uploaded_at)} • {statusLabel(contract.status)}
          </p>
        </div>
        {contract.status === "analyzed" && (
          <>
            <Link
              href={`/contracts/${contract.id}/redline`}
              className="flex items-center gap-2 rounded-lg border border-brand-300 bg-brand-50 px-3 py-2 text-sm font-semibold text-brand-700 hover:bg-brand-100 transition"
            >
              <FileEdit className="h-4 w-4" />
              Redline
            </Link>
            <Link
              href={`/contracts/${contract.id}/report`}
              className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition"
            >
              <FileText className="h-4 w-4" />
              Rapor
            </Link>
          </>
        )}
      </div>

      {/* Analysis progress (only when processing) */}
      {contract.status === "processing" && (
        <AnalysisProgressBar
          contractId={contract.id}
          onComplete={handleAnalysisComplete}
        />
      )}

      {/* Risk summary (shown when analysis has produced clauses) */}
      {clauses.length > 0 && contract.status !== "processing" && (
        <RiskSummary
          contractId={contract.id}
          clauses={clauses}
          onFocusClause={async (clauseId) => {
            const target = clauses.find((c) => c.id === clauseId);
            if (target) await handleSelectClause(target);
          }}
        />
      )}

      {/* Two-panel layout: clauses list + detail */}
      {clauses.length > 0 ? (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
          {/* Left: clause list */}
          <div className="lg:col-span-2 rounded-xl border bg-white overflow-hidden">
            <div className="border-b px-4 py-3">
              <h3 className="text-sm font-semibold text-gray-700">
                Maddeler ({clauses.length})
              </h3>
            </div>
            <div className="max-h-[600px] overflow-y-auto">
              <ClauseList
                clauses={clauses}
                selectedId={selectedClause?.id}
                onSelect={handleSelectClause}
                riskLevels={riskLevels}
              />
            </div>
          </div>

          {/* Right: clause detail */}
          <div className="lg:col-span-3 rounded-xl border bg-white overflow-hidden">
            {selectedClause ? (
              <ClauseDetailPanel clause={selectedClause} />
            ) : (
              <div className="flex items-center justify-center h-full min-h-[300px] text-sm text-gray-400">
                Detayını görmek için bir madde seçin.
              </div>
            )}
          </div>
        </div>
      ) : (
        contract.status !== "processing" && (
          <div className="rounded-xl border bg-white p-10 text-center text-sm text-gray-400">
            Bu sözleşme henüz analiz edilmemiş. Sözleşmeler sayfasından &quot;Analiz
            Et&quot; butonunu kullanın.
          </div>
        )
      )}
    </div>
  );
}
