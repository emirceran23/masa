"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { login } from "@/lib/auth";
import { useAuthStore } from "@/stores/auth-store";
import { extractApiError } from "@/lib/utils";
import { Loader2 } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { fetchUser } = useAuthStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      await fetchUser();
      toast.success("Giriş başarılı!");
      router.push("/dashboard");
    } catch (err: any) {
      toast.error(extractApiError(err, "Giriş başarısız."));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
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
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded-lg border px-4 py-2.5 text-sm focus:border-brand-500 focus:ring-brand-500"
          placeholder="••••••••••••"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50 transition"
      >
        {loading && <Loader2 className="h-4 w-4 animate-spin" />}
        Giriş Yap
      </button>

      <p className="text-center text-sm text-gray-500">
        Hesabınız yok mu?{" "}
        <Link href="/auth/register" className="font-medium text-brand-600 hover:underline">
          Kayıt Ol
        </Link>
      </p>
    </form>
  );
}
