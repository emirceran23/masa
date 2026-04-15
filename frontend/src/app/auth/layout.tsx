import { Shield } from "lucide-react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-10 shadow-lg">
        <div className="flex flex-col items-center">
          <Shield className="h-12 w-12 text-brand-600" />
          <h1 className="mt-3 text-2xl font-bold text-gray-800">Lagent</h1>
          <p className="text-sm text-gray-500">
            Sözleşme İnceleme Platformu
          </p>
        </div>
        {children}
      </div>
    </div>
  );
}
