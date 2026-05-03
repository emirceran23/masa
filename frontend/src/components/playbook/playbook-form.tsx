"use client";

import { useState } from "react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { Loader2, Save } from "lucide-react";
import RuleEditor from "./rule-editor";
import type { PlaybookDetail, PlaybookRuleInput } from "@/types";
import { extractApiError } from "@/lib/utils";
import { usePlaybookStore } from "@/stores/playbook-store";

interface Props {
  initial?: PlaybookDetail | null;
}

export default function PlaybookForm({ initial }: Props) {
  const router = useRouter();
  const { create, update } = usePlaybookStore();

  const [name, setName] = useState(initial?.name ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [rules, setRules] = useState<PlaybookRuleInput[]>(
    (initial?.rules ?? []).map((r) => ({
      rule_type: r.rule_type,
      content: r.content,
      threshold_value: r.threshold_value,
    })),
  );
  const [saving, setSaving] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) {
      toast.error("Playbook adı boş olamaz.");
      return;
    }
    if (rules.some((r) => !r.content.trim())) {
      toast.error("Boş kural içeriği olamaz.");
      return;
    }
    if (
      rules.some(
        (r) =>
          r.rule_type === "threshold" &&
          (r.threshold_value === null || Number.isNaN(r.threshold_value)),
      )
    ) {
      toast.error("Eşik tipli kurallar için eşik değeri zorunludur.");
      return;
    }

    setSaving(true);
    try {
      if (initial) {
        await update(initial.id, { name, description, rules });
        toast.success("Playbook güncellendi.");
      } else {
        await create({ name, description, rules });
        toast.success("Playbook oluşturuldu.");
      }
      router.push("/playbooks");
    } catch (err: any) {
      toast.error(extractApiError(err, "Kaydetme başarısız."));
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="rounded-xl border bg-white p-5 space-y-4">
        <div>
          <label className="block text-xs font-semibold text-gray-600 mb-1">
            Ad
          </label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Örn: Satış Sözleşmesi Playbook'u"
            className="w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold text-gray-600 mb-1">
            Açıklama
          </label>
          <textarea
            value={description ?? ""}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
            placeholder="Bu playbook hangi tür sözleşmeler için kullanılacak?"
            className="w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          />
        </div>
      </div>

      <div>
        <h3 className="mb-3 text-sm font-semibold text-gray-700">
          Kurallar ({rules.length})
        </h3>
        <RuleEditor rules={rules} onChange={setRules} disabled={saving} />
      </div>

      <div className="flex justify-end gap-3">
        <button
          type="button"
          onClick={() => router.back()}
          className="rounded-lg border px-4 py-2 text-sm text-gray-600 hover:bg-gray-50"
        >
          İptal
        </button>
        <button
          type="submit"
          disabled={saving}
          className="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
        >
          {saving ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Save className="h-4 w-4" />
          )}
          {initial ? "Güncelle" : "Oluştur"}
        </button>
      </div>
    </form>
  );
}
