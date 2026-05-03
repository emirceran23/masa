"use client";

import { useEffect } from "react";
import Link from "next/link";
import { toast } from "sonner";
import { BookOpen, Loader2, Plus, Star, Trash2 } from "lucide-react";
import { usePlaybookStore } from "@/stores/playbook-store";
import { extractApiError, formatDate } from "@/lib/utils";

export default function PlaybooksPage() {
  const { items, loading, fetchAll, remove } = usePlaybookStore();

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  async function handleDelete(id: string, name: string) {
    if (!confirm(`"${name}" playbook'unu silmek istediğinize emin misiniz?`)) return;
    try {
      await remove(id);
      toast.success("Playbook silindi.");
    } catch (err: any) {
      toast.error(extractApiError(err, "Silme işlemi başarısız."));
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Playbook'lar</h1>
          <p className="text-sm text-gray-500">
            Sözleşme inceleme kurallarınızı yönetin. Toplam {items.length} playbook.
          </p>
        </div>
        <Link
          href="/playbooks/new"
          className="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 transition"
        >
          <Plus className="h-4 w-4" />
          Yeni Playbook
        </Link>
      </div>

      {loading ? (
        <div className="flex justify-center py-10">
          <Loader2 className="h-8 w-8 animate-spin text-brand-500" />
        </div>
      ) : items.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-400">
          <BookOpen className="mb-2 h-10 w-10" />
          <p className="text-sm">Henüz playbook oluşturulmamış.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {items.map((pb) => (
            <div
              key={pb.id}
              className="rounded-xl border bg-white p-5 shadow-sm hover:shadow-md transition"
            >
              <div className="flex items-start justify-between">
                <Link
                  href={`/playbooks/${pb.id}`}
                  className="block flex-1"
                >
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-gray-800 hover:text-brand-700">
                      {pb.name}
                    </h3>
                    {pb.is_default && (
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    )}
                  </div>
                  {pb.description && (
                    <p className="mt-1 line-clamp-2 text-xs text-gray-500">
                      {pb.description}
                    </p>
                  )}
                  <p className="mt-3 text-[11px] text-gray-400">
                    {formatDate(pb.updated_at)}
                  </p>
                </Link>

                <button
                  onClick={() => handleDelete(pb.id, pb.name)}
                  className="ml-2 rounded-md p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-600"
                  aria-label="Sil"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
