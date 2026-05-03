"use client";

/**
 * DiffViewer — renders an HTML diff string produced by utils/diff.py.
 * Deletions get a red background, insertions get a green background.
 * The CSS classes diff-del / diff-ins are defined in globals.css.
 */

interface DiffViewerProps {
  diffHtml: string;
  className?: string;
}

export default function DiffViewer({ diffHtml, className }: DiffViewerProps) {
  return (
    <div
      className={`diff-viewer text-sm leading-relaxed ${className ?? ""}`}
      dangerouslySetInnerHTML={{ __html: diffHtml }}
    />
  );
}
