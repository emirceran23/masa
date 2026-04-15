import { create } from "zustand";
import type { Contract, PaginatedResponse } from "@/types";
import api from "@/lib/api";

interface ContractState {
  contracts: Contract[];
  total: number;
  page: number;
  loading: boolean;
  fetchContracts: (page?: number) => Promise<void>;
  uploadContract: (file: File) => Promise<Contract>;
  deleteContract: (id: string) => Promise<void>;
  startAnalysis: (id: string) => Promise<void>;
}

export const useContractStore = create<ContractState>((set, get) => ({
  contracts: [],
  total: 0,
  page: 1,
  loading: false,

  fetchContracts: async (page = 1) => {
    set({ loading: true });
    try {
      const { data } = await api.get<PaginatedResponse<Contract>>(
        `/contracts?page=${page}&size=10`
      );
      set({
        contracts: data.items,
        total: data.total,
        page: data.page,
        loading: false,
      });
    } catch {
      set({ loading: false });
    }
  },

  uploadContract: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    const { data } = await api.post<Contract>("/contracts/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    // Refresh list
    await get().fetchContracts(get().page);
    return data;
  },

  deleteContract: async (id: string) => {
    await api.delete(`/contracts/${id}`);
    await get().fetchContracts(get().page);
  },

  startAnalysis: async (id: string) => {
    await api.post(`/contracts/${id}/analyze`);
    // Refresh to see status change
    await get().fetchContracts(get().page);
  },
}));
