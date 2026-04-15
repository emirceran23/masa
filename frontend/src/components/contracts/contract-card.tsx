"use client";

import Link from "next/link";
import type { Contract } from "@/types";
import { cn, formatDate, formatFileSize, statusLabel } from "@/lib/utils";
import { FileText, Trash2, Play, Loader2 } from "lucide-react";

interface ContractCardProps {
  contract: Contract;
  onDelete: (id: string) => void;
  onAnalyze: (id: string) => void;
}

export default function ContractCard({
  contract,
  onDelete,
  onAnalyze,
}: ContractCardProps) {
  const statusColor: Record<string, string> = {
    uploaded: "bg-blue-100 text-blue-700",
    processing: "bg-yellow-100 text-yellow-700",
    analyzed: "bg-green-100 text-green-700",
    error: "bg-red-100 text-red-700",
  };

  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm transition hover:shadow-md">
      <div className="flex items-start justify-between">
        <Link
          href={`/contracts/${contract.id}`}
          className="flex items-center gap-3 group"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50">
            <FileText className="h-5 w-5 text-brand-600" />
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-800 group-hover:text-brand-600 transition">
              {contract.file_name}
            </p>
            <p className="text-xs text-gray-400">
              {formatFileSize(contract.file_size)} •{" "}
              {formatDate(contract.created_at)}
            </p>
          </div>
        </Link>

        <span
          className={cn(
            "rounded-full px-2.5 py-0.5 text-xs font-medium",
            statusColor[contract.status] ?? "bg-gray-100 text-gray-600"
          )}
        >
          {statusLabel(contract.status)}
        </span>
      </div>

      {/* Actions */}
      <div className="mt-4 flex items-center justify-between border-t pt-3">
        <span className="text-xs text-gray-400">
          {contract.total_clauses > 0
            ? `${contract.total_clauses} madde`
            : "Henüz analiz edilmedi"}
        </span>

        <div className="flex gap-2">
          {contract.status === "uploaded" && (
            <button
              onClick={() => onAnalyze(contract.id)}
              className="flex items-center gap-1 rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-brand-700 transition"
            >
              <Play className="h-3.5 w-3.5" />
              Analiz Et
            </button>
          )}
          {contract.status === "processing" && (
            <span className="flex items-center gap-1 text-xs text-yellow-600">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              İşleniyor…
            </span>
          )}
          <button
            onClick={() => onDelete(contract.id)}
            className="rounded-lg p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-500 transition"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
