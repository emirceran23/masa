"use client";

import { useAuthStore } from "@/stores/auth-store";
import { Bell } from "lucide-react";

export default function Topbar() {
  const { user } = useAuthStore();

  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6">
      <h2 className="text-lg font-semibold text-gray-800">
        {/* Page title gets injected by each page */}
      </h2>

      <div className="flex items-center gap-4">
        <button className="relative rounded-lg p-2 text-gray-500 hover:bg-gray-100 transition">
          <Bell className="h-5 w-5" />
        </button>
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-100 text-sm font-semibold text-brand-700">
            {user?.full_name?.charAt(0).toUpperCase() ?? "U"}
          </div>
          <span className="text-sm font-medium text-gray-700">
            {user?.full_name}
          </span>
        </div>
      </div>
    </header>
  );
}
