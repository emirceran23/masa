"use client";

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import PlaybookForm from "@/components/playbook/playbook-form";

export default function NewPlaybookPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <Link
          href="/playbooks"
          className="rounded-lg p-2 hover:bg-gray-100 transition"
          aria-label="Geri"
        >
          <ArrowLeft className="h-5 w-5 text-gray-500" />
        </Link>
        <h1 className="text-xl font-bold text-gray-800">Yeni Playbook</h1>
      </div>

      <PlaybookForm />
    </div>
  );
}
