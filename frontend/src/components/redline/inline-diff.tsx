"use client";

import { useState } from "react";
import DiffViewer from "./diff-viewer";
import type { RevisionDetail } from "@/types";
import { cn } from "@/lib/utils";
import { ChevronDown, ChevronUp } from "lucide-react";

interface InlineDiffProps {
  revision: RevisionDetail;
  sequenceNo: number;
}

/**
 * InlineDiff — shows original vs. suggested text side by side,
 * with an expandable diff highlight and optional edited-text override.
 */
export default function InlineDiff({ revision, sequenceNo }: InlineDiffProps) {
  const [expanded, setExpanded] = useState(false);

  const effectiveText =
    revision.status === "edited" && revision.edited_text
      ? revision.edited_text
      : revision.suggested_text;

  return (
    <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setExpanded((p) => !p)}
        className="flex w-full items-center justify-between px-4 py-3 text-left hover:bg-gray-50 transition"
      >
        <span className="text-sm font-semibold text-gray-700">
          Madde #{sequenceNo} — Revizyon Önerisi
        </span>
        {expanded ? (
          <ChevronUp className="h-4 w-4 text-gray-400" />
        ) : (
          <ChevronDown className="h-4 w-4 text-gray-400" />
        )}
      </button>

      {expanded && (
        <div className="border-t p-4 space-y-4">
          {revision.diff_html ? (
            <div>
              <p className="mb-1 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                Değişiklikler
              </p>
              <div className="rounded-lg bg-gray-50 p-3">
                <DiffViewer diffHtml={revision.diff_html} />
              </div>
            </div>
          ) : (
            <div>
              <p className="mb-1 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                Önerilen Metin
              </p>
              <p className="rounded-lg bg-green-50 p-3 text-sm text-green-900">
                {effectiveText}
              </p>
            </div>
          )}

          {revision.context_used && (
            <p className="text-xs italic text-gray-500">{revision.context_used}</p>
          )}
        </div>
      )}
    </div>
  );
}
