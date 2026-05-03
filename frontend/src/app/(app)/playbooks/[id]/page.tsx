"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Loader2 } from "lucide-react";
import { toast } from "sonner";
import PlaybookForm from "@/components/playbook/playbook-form";
import { usePlaybookStore } from "@/stores/playbook-store";
import type { PlaybookDetail } from "@/types";
import { extractApiError } from "@/lib/utils";

export default function PlaybookEditPage() {
  const { id } = useParams<{ id: string }>();
  const { get } = usePlaybookStore();
  const [pb, setPb] = useState<PlaybookDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    get(id)
      .then(setPb)
      .catch((err) =>
        toast.error(extractApiError(err, "Playbook yüklenemedi.")),
      )
      .finally(() => setLoading(false));
  }, [id, get]);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="h-8 w-8 animate-spin text-brand-500" />
      </div>
    );
  }

  if (!pb) {
    return (
      <div className="text-center py-20 text-gray-400">
        Playbook bulunamadı.
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <Link
          href="/playbooks"
          className="rounded-lg p-2 hover:bg-gray-100 transition"
          aria-label="Geri"
        >
          <ArrowLeft className="h-5 w-5 text-gray-500" />
        </Link>
        <h1 className="text-xl font-bold text-gray-800">{pb.name}</h1>
      </div>

      <PlaybookForm initial={pb} />
    </div>
  );
}
