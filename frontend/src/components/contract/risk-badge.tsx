"use client";

import { AlertTriangle, CheckCircle, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";

interface RiskBadgeProps {
  level: string | null | undefined;
  size?: "sm" | "md";
  withIcon?: boolean;
}

const LEVEL_META: Record<
  string,
  { label: string; tone: string; Icon: typeof ShieldAlert }
> = {
  low: {
    label: "Düşük",
    tone: "bg-green-50 text-green-700 border-green-200",
    Icon: CheckCircle,
  },
  medium: {
    label: "Orta",
    tone: "bg-amber-50 text-amber-700 border-amber-200",
    Icon: AlertTriangle,
  },
  high: {
    label: "Yüksek",
    tone: "bg-red-50 text-red-700 border-red-200",
    Icon: ShieldAlert,
  },
};

export default function RiskBadge({ level, size = "sm", withIcon = true }: RiskBadgeProps) {
  const meta = LEVEL_META[level ?? ""] ?? {
    label: "Belirsiz",
    tone: "bg-gray-50 text-gray-600 border-gray-200",
    Icon: ShieldAlert,
  };
  const { Icon } = meta;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border font-semibold capitalize",
        meta.tone,
        size === "sm" ? "px-2 py-0.5 text-[11px]" : "px-3 py-1 text-sm",
      )}
    >
      {withIcon && <Icon className={size === "sm" ? "h-3 w-3" : "h-4 w-4"} />}
      {meta.label}
    </span>
  );
}
