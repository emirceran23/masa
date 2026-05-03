"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useContractStore } from "@/stores/contract-store";
import UploadDropzone from "@/components/contracts/upload-dropzone";
import ContractCard from "@/components/contracts/contract-card";
import { extractApiError } from "@/lib/utils";
import { Loader2, Plus } from "lucide-react";

export default function ContractsPage() {
  const router = useRouter();
  const {
    contracts,
    total,
    page,
    loading,
    fetchContracts,
    uploadContract,
    deleteContract,
    startAnalysis,
  } = useContractStore();

  const [showUpload, setShowUpload] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchContracts();
  }, [fetchContracts]);

  async function handleUpload(file: File) {
    setUploading(true);
    try {
      await uploadContract(file);
      toast.success("Sözleşme başarıyla yüklendi!");
      setShowUpload(false);
    } catch (err: any) {
      toast.error(extractApiError(err, "Yükleme başarısız."));
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Bu sözleşmeyi silmek istediğinize emin misiniz?")) return;
    try {
      await deleteContract(id);
      toast.success("Sözleşme silindi.");
    } catch {
      toast.error("Silme işlemi başarısız.");
    }
  }

  async function handleAnalyze(id: string) {
    try {
      await startAnalysis(id);
      router.push(`/contracts/${id}`);
    } catch (err: any) {
      toast.error(extractApiError(err, "Analiz başlatılamadı."));
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Sözleşmeler</h1>
          <p className="text-sm text-gray-500">
            Toplam {total} sözleşme
          </p>
        </div>
        <button
          onClick={() => setShowUpload(!showUpload)}
          className="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 transition"
        >
          <Plus className="h-4 w-4" />
          Yeni Yükle
        </button>
      </div>

      {/* Upload area */}
      {showUpload && (
        <UploadDropzone onFileSelect={handleUpload} uploading={uploading} />
      )}

      {/* Contract list */}
      {loading ? (
        <div className="flex justify-center py-10">
          <Loader2 className="h-8 w-8 animate-spin text-brand-500" />
        </div>
      ) : contracts.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-400">
          <p className="text-sm">Henüz sözleşme yüklenmemiş.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {contracts.map((c) => (
            <ContractCard
              key={c.id}
              contract={c}
              onDelete={handleDelete}
              onAnalyze={handleAnalyze}
            />
          ))}
        </div>
      )}

      {/* Simple pagination */}
      {total > 10 && (
        <div className="flex justify-center gap-2">
          <button
            disabled={page <= 1}
            onClick={() => fetchContracts(page - 1)}
            className="rounded-lg border px-4 py-2 text-sm disabled:opacity-40"
          >
            Önceki
          </button>
          <span className="flex items-center text-sm text-gray-500">
            Sayfa {page}
          </span>
          <button
            disabled={contracts.length < 10}
            onClick={() => fetchContracts(page + 1)}
            className="rounded-lg border px-4 py-2 text-sm disabled:opacity-40"
          >
            Sonraki
          </button>
        </div>
      )}
    </div>
  );
}
