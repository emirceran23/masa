"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileText } from "lucide-react";
import { cn } from "@/lib/utils";

interface UploadDropzoneProps {
  onFileSelect: (file: File) => void;
  uploading?: boolean;
}

export default function UploadDropzone({
  onFileSelect,
  uploading = false,
}: UploadDropzoneProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } =
    useDropzone({
      onDrop,
      accept: {
        "application/pdf": [".pdf"],
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
          [".docx"],
      },
      maxFiles: 1,
      maxSize: 10 * 1024 * 1024, // 10 MB
      disabled: uploading,
    });

  return (
    <div
      {...getRootProps()}
      className={cn(
        "flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-10 transition-colors",
        isDragActive
          ? "border-brand-400 bg-brand-50"
          : "border-gray-300 bg-gray-50 hover:border-brand-300 hover:bg-brand-50/30",
        uploading && "pointer-events-none opacity-50"
      )}
    >
      <input {...getInputProps()} />
      {acceptedFiles.length > 0 ? (
        <div className="flex items-center gap-3">
          <FileText className="h-8 w-8 text-brand-500" />
          <span className="text-sm font-medium text-gray-700">
            {acceptedFiles[0].name}
          </span>
        </div>
      ) : (
        <>
          <Upload className="mb-3 h-10 w-10 text-gray-400" />
          <p className="text-sm font-medium text-gray-600">
            {isDragActive
              ? "Dosyayı buraya bırakın..."
              : "Sözleşme dosyasını sürükleyip bırakın veya tıklayın"}
          </p>
          <p className="mt-1 text-xs text-gray-400">
            PDF veya DOCX • Maks. 10 MB
          </p>
        </>
      )}
    </div>
  );
}
