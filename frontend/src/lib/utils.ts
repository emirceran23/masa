import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Safely extract an error message from an Axios error.
 * FastAPI validation errors return `detail` as an array of objects,
 * while custom HTTPExceptions return `detail` as a string.
 */
export function extractApiError(err: any, fallback = "Bir hata oluştu."): string {
  const detail = err?.response?.data?.detail;
  if (!detail) return fallback;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((d: any) => d.msg || JSON.stringify(d)).join(", ");
  }
  return fallback;
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatDate(dateStr: string | undefined | null): string {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return "—";
  return new Intl.DateTimeFormat("tr-TR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(d);
}

export function statusLabel(status: string): string {
  const map: Record<string, string> = {
    uploaded: "Yüklendi",
    processing: "İşleniyor",
    analyzed: "Analiz Edildi",
    error: "Hata",
    draft: "Taslak",
    in_review: "İnceleniyor",
    approved: "Onaylandı",
    rejected: "Reddedildi",
  };
  return map[status] ?? status;
}

export function riskColor(level: string): string {
  const map: Record<string, string> = {
    low: "text-green-600 bg-green-50",
    medium: "text-yellow-600 bg-yellow-50",
    high: "text-red-600 bg-red-50",
    critical: "text-purple-600 bg-purple-50",
  };
  return map[level] ?? "text-gray-600 bg-gray-50";
}

export function categoryLabel(category: string): string {
  const map: Record<string, string> = {
    sorumluluk: "Sorumluluk",
    fesih: "Fesih",
    gizlilik: "Gizlilik",
    odeme: "Ödeme",
    fikri_mulkiyet: "Fikri Mülkiyet",
    tazminat: "Tazminat",
    uyusmazlik: "Uyuşmazlık Çözümü",
    rekabet_yasagi: "Rekabet Yasağı",
    belirsiz: "Belirsiz",
  };
  return map[category] ?? category;
}
