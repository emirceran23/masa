"use client";

import { Plus, Trash2 } from "lucide-react";
import type { PlaybookRuleInput, PlaybookRuleType } from "@/types";
import { cn } from "@/lib/utils";

interface RuleEditorProps {
  rules: PlaybookRuleInput[];
  onChange: (rules: PlaybookRuleInput[]) => void;
  disabled?: boolean;
}

const RULE_TYPES: { value: PlaybookRuleType; label: string; tone: string }[] = [
  { value: "acceptable", label: "Kabul Edilebilir", tone: "text-green-700 bg-green-50 border-green-200" },
  { value: "required", label: "Zorunlu", tone: "text-blue-700 bg-blue-50 border-blue-200" },
  { value: "rejected", label: "Yasaklı", tone: "text-red-700 bg-red-50 border-red-200" },
  { value: "threshold", label: "Eşik Değer", tone: "text-amber-700 bg-amber-50 border-amber-200" },
];

export default function RuleEditor({ rules, onChange, disabled }: RuleEditorProps) {
  function update(index: number, patch: Partial<PlaybookRuleInput>) {
    const next = rules.map((r, i) => (i === index ? { ...r, ...patch } : r));
    onChange(next);
  }

  function remove(index: number) {
    onChange(rules.filter((_, i) => i !== index));
  }

  function add() {
    onChange([
      ...rules,
      { rule_type: "acceptable", content: "", threshold_value: null },
    ]);
  }

  return (
    <div className="space-y-3">
      {rules.length === 0 && (
        <div className="rounded-lg border border-dashed bg-gray-50 py-8 text-center text-sm text-gray-400">
          Henüz kural eklenmemiş.
        </div>
      )}

      {rules.map((rule, idx) => {
        const tone = RULE_TYPES.find((t) => t.value === rule.rule_type)?.tone;
        return (
          <div
            key={idx}
            className={cn(
              "rounded-xl border bg-white p-4 space-y-3 shadow-sm",
              tone?.split(" ").find((c) => c.startsWith("border-")),
            )}
          >
            <div className="flex items-center justify-between gap-2">
              <select
                value={rule.rule_type}
                disabled={disabled}
                onChange={(e) =>
                  update(idx, {
                    rule_type: e.target.value as PlaybookRuleType,
                    threshold_value:
                      e.target.value === "threshold" ? rule.threshold_value ?? 0 : null,
                  })
                }
                className={cn(
                  "rounded-lg border px-2 py-1 text-xs font-semibold",
                  tone,
                )}
              >
                {RULE_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
              <button
                type="button"
                disabled={disabled}
                onClick={() => remove(idx)}
                className="rounded-md p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-600 disabled:opacity-30"
                aria-label="Kuralı sil"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>

            <textarea
              value={rule.content}
              disabled={disabled}
              onChange={(e) => update(idx, { content: e.target.value })}
              rows={2}
              placeholder="Kural açıklaması — ne beklenir, ne yasaktır?"
              className="w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            />

            {rule.rule_type === "threshold" && (
              <div className="flex items-center gap-2 text-sm">
                <label className="text-xs text-gray-500">Eşik değer (%):</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  value={rule.threshold_value ?? 0}
                  disabled={disabled}
                  onChange={(e) =>
                    update(idx, { threshold_value: Number(e.target.value) })
                  }
                  className="w-24 rounded-lg border px-2 py-1 text-sm focus:border-brand-500 focus:outline-none"
                />
              </div>
            )}
          </div>
        );
      })}

      <button
        type="button"
        disabled={disabled}
        onClick={add}
        className="flex w-full items-center justify-center gap-2 rounded-lg border border-dashed border-brand-300 bg-brand-50/50 px-3 py-2.5 text-sm font-medium text-brand-700 hover:bg-brand-50 disabled:opacity-40"
      >
        <Plus className="h-4 w-4" />
        Kural Ekle
      </button>
    </div>
  );
}
