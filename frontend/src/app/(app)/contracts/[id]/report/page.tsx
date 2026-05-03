"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import {
  ArrowLeft,
  FileDown,
  FileText,
  Loader2,
  RefreshCw,
} from "lucide-react";
import api from "@/lib/api";
import type { ContractDetail, Report } from "@/types";
import ReportSummaryCard from "@/components/reports/report-summary-card";

export default function ContractReportPage() {
  const { id } = useParams<{ id: string }>();
  const [contract, setContract] = useState<ContractDetail | null>(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [exporting, setExporting] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [contractRes, reportsRes] = await Promise.all([
        api.get<ContractDetail>(`/contracts/${id}`),
        api.get<Report[]>(`/contracts/${id}/reports`),
      ]);
      setContract(contractRes.data);
      setReports(reportsRes.data);
    } catch {
      toast.error("Veri yüklenemedi.");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  async function handleGenerate(report_type: "summary" | "detailed", fmt: "pdf" | "docx") {
    setGenerating(true);
    try {
      const { data } = await api.post<Report>(`/contracts/${id}/reports`, {
        report_type,
        fmt,
      });
      setReports((prev) => [data, ...prev]);
      toast.success(
        `${report_type === "summary" ? "Özet" : "Detaylı"} rapor oluşturuldu.`
      );
    } catch {
      toast.error("Rapor oluşturulamadı.");
    } finally {
      setGenerating(false);
    }
  }

  async function handleDownload(report: Report) {
    try {
      const response = await api.get(`/reports/${report.id}/download`, {
        responseType: "blob",
      });
      const ext = report.storage_path?.endsWith(".pdf") ? "pdf" : "docx";
      const url = URL.createObjectURL(response.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = `rapor_${report.report_type}_${report.id.slice(0, 8)}.${ext}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error("Rapor indirilemedi.");
    }
  }

  async function handleExport() {
    setExporting(true);
    try {
      const response = await api.get(`/contracts/${id}/export`, {
        responseType: "blob",
      });
      const url = URL.createObjectURL(response.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = `revize_sozlesme_${id.slice(0, 8)}.docx`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Revize edilmiş sözleşme indirildi.");
    } catch {
      toast.error("Sözleşme dışa aktarılamadı.");
    } finally {
      setExporting(false);
    }
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
      <div className="text-center py-20 text-gray-400">Sözleşme bulunamadı.</div>
    );
  }

  const isAnalyzed = contract.status === "analyzed";

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link
          href={`/contracts/${id}`}
          className="rounded-lg p-2 hover:bg-gray-100 transition"
        >
          <ArrowLeft className="h-5 w-5 text-gray-500" />
        </Link>
        <div className="flex-1">
          <h1 className="text-xl font-bold text-gray-800">{contract.file_name}</h1>
          <p className="text-xs text-gray-400">Raporlama & Dışa Aktarım</p>
        </div>
      </div>

      {!isAnalyzed && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
          Rapor oluşturmak için sözleşmenin önce analiz edilmesi gerekir.
        </div>
      )}

      {/* Generate new report */}
      {isAnalyzed && (
        <div className="rounded-xl border bg-white p-6 space-y-4">
          <h2 className="text-base font-semibold text-gray-800">Yeni Rapor Oluştur</h2>
          <p className="text-sm text-gray-500">
            Rapor türü ve formatını seçerek sözleşme analiz sonuçlarını dışa aktarın.
          </p>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {(
              [
                { type: "summary", fmt: "pdf", label: "Özet PDF" },
                { type: "summary", fmt: "docx", label: "Özet DOCX" },
                { type: "detailed", fmt: "pdf", label: "Detaylı PDF" },
                { type: "detailed", fmt: "docx", label: "Detaylı DOCX" },
              ] as const
            ).map(({ type, fmt, label }) => (
              <button
                key={`${type}-${fmt}`}
                disabled={generating}
                onClick={() => handleGenerate(type, fmt)}
                className="flex items-center justify-center gap-2 rounded-lg border px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 transition"
              >
                {generating ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <FileText className="h-4 w-4 text-brand-500" />
                )}
                {label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Export revised contract */}
      {isAnalyzed && (
        <div className="rounded-xl border bg-white p-6 space-y-3">
          <h2 className="text-base font-semibold text-gray-800">Revize Edilmiş Sözleşme</h2>
          <p className="text-sm text-gray-500">
            Kabul edilen revizyonlar orijinal metne uygulanarak DOCX olarak dışa
            aktarılır. Onaylanmamış maddeler orijinal halleriyle kalır.
          </p>
          <button
            disabled={exporting}
            onClick={handleExport}
            className="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50 transition"
          >
            {exporting ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <FileDown className="h-4 w-4" />
            )}
            Revize DOCX İndir
          </button>
        </div>
      )}

      {/* Past reports */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-semibold text-gray-800">
            Geçmiş Raporlar ({reports.length})
          </h2>
          <button
            onClick={loadData}
            className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-600"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Yenile
          </button>
        </div>

        {reports.length === 0 ? (
          <div className="rounded-xl border bg-white p-8 text-center text-sm text-gray-400">
            Henüz rapor oluşturulmadı.
          </div>
        ) : (
          <div className="space-y-3">
            {reports.map((report) => (
              <ReportSummaryCard
                key={report.id}
                report={report}
                onDownload={handleDownload}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
