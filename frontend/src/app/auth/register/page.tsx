"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { register } from "@/lib/auth";
import { extractApiError } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      await register(email, password, fullName);
      toast.success("Kayıt başarılı! Giriş yapabilirsiniz.");
      router.push("/auth/login");
    } catch (err: any) {
      toast.error(extractApiError(err, "Kayıt başarısız."));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Ad Soyad
        </label>
        <input
          type="text"
          required
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="w-full rounded-lg border px-4 py-2.5 text-sm focus:border-brand-500 focus:ring-brand-500"
          placeholder="Adınız Soyadınız"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          E-posta
        </label>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded-lg border px-4 py-2.5 text-sm focus:border-brand-500 focus:ring-brand-500"
          placeholder="ornek@email.com"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Şifre
        </label>
        <input
          type="password"
          required
          minLength={12}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded-lg border px-4 py-2.5 text-sm focus:border-brand-500 focus:ring-brand-500"
          placeholder="En az 12 karakter"
        />
        <p className="mt-1 text-xs text-gray-400">
          Büyük/küçük harf, rakam ve özel karakter içermelidir.
        </p>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50 transition"
      >
        {loading && <Loader2 className="h-4 w-4 animate-spin" />}
        Kayıt Ol
      </button>

      <p className="text-center text-sm text-gray-500">
        Zaten hesabınız var mı?{" "}
        <Link href="/auth/login" className="font-medium text-brand-600 hover:underline">
          Giriş Yap
        </Link>
      </p>
    </form>
  );
}
