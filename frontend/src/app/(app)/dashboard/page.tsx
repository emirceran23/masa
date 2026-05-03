"use client";

import { useEffect, useState } from "react";
import { useContractStore } from "@/stores/contract-store";
import { useAuthStore } from "@/stores/auth-store";
import { FileText, Upload, BarChart3 } from "lucide-react";
import Link from "next/link";
import api from "@/lib/api";
import type { RiskAssessmentDetail } from "@/types";
import RiskChart from "@/components/analysis/risk-chart";

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { contracts, total, fetchContracts } = useContractStore();

  const [riskCounts, setRiskCounts] = useState({ low: 0, medium: 0, high: 0 });

  useEffect(() => {
    fetchContracts();
  }, [fetchContracts]);

  useEffect(() => {
    // Aggregate risk levels across the user's analyzed contracts.
    const analyzedIds = contracts
      .filter((c) => c.status === "analyzed")
      .map((c) => c.id);
    if (analyzedIds.length === 0) {
      setRiskCounts({ low: 0, medium: 0, high: 0 });
      return;
    }

    let cancelled = false;
    (async () => {
      const totals = { low: 0, medium: 0, high: 0 };
      const responses = await Promise.allSettled(
        analyzedIds.map((cid) =>
          api.get<RiskAssessmentDetail[]>(`/contracts/${cid}/risks`),
        ),
      );
      responses.forEach((res) => {
        if (res.status !== "fulfilled") return;
        res.value.data.forEach((r) => {
          if (r.risk_level === "low") totals.low += 1;
          else if (r.risk_level === "medium") totals.medium += 1;
          else if (r.risk_level === "high") totals.high += 1;
        });
      });
      if (!cancelled) setRiskCounts(totals);
    })();

    return () => {
      cancelled = true;
    };
  }, [contracts]);

  const analyzed = contracts.filter((c) => c.status === "analyzed").length;
  const processing = contracts.filter((c) => c.status === "processing").length;

  const stats = [
    {
      label: "Toplam Sözleşme",
      value: total,
      icon: FileText,
      color: "text-blue-600 bg-blue-50",
    },
    {
      label: "Analiz Edilmiş",
      value: analyzed,
      icon: BarChart3,
      color: "text-green-600 bg-green-50",
    },
    {
      label: "İşleniyor",
      value: processing,
      icon: Upload,
      color: "text-yellow-600 bg-yellow-50",
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">
          Hoş geldiniz, {user?.full_name} 👋
        </h1>
        <p className="text-sm text-gray-500 mt-1">
          Lagent kontrol panelinize genel bakış.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        {stats.map((s) => (
          <div
            key={s.label}
            className="flex items-center gap-4 rounded-xl border bg-white p-5"
          >
            <div
              className={`flex h-12 w-12 items-center justify-center rounded-lg ${s.color}`}
            >
              <s.icon className="h-6 w-6" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800">{s.value}</p>
              <p className="text-sm text-gray-500">{s.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Aggregate risk chart */}
      <RiskChart counts={riskCounts} title="Tüm Sözleşmelerde Risk Dağılımı" />

      {/* Quick actions */}
      <div className="flex gap-4">
        <Link
          href="/contracts"
          className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 transition"
        >
          Sözleşmeleri Görüntüle
        </Link>
      </div>

      {/* Recent contracts */}
      {contracts.length > 0 && (
        <div>
          <h2 className="mb-3 text-lg font-semibold text-gray-800">
            Son Sözleşmeler
          </h2>
          <div className="rounded-xl border bg-white divide-y">
            {contracts.slice(0, 5).map((c) => (
              <Link
                key={c.id}
                href={`/contracts/${c.id}`}
                className="flex items-center justify-between px-5 py-3 hover:bg-gray-50 transition"
              >
                <div className="flex items-center gap-3">
                  <FileText className="h-5 w-5 text-gray-400" />
                  <span className="text-sm font-medium text-gray-700">
                    {c.file_name}
                  </span>
                </div>
                <span className="text-xs text-gray-400">
                  {c.total_clauses} madde
                </span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
