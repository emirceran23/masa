import { create } from "zustand";
import api from "@/lib/api";
import type {
  Playbook,
  PlaybookDetail,
  PlaybookRuleInput,
} from "@/types";

interface PlaybookState {
  items: Playbook[];
  loading: boolean;
  fetchAll: () => Promise<void>;
  get: (id: string) => Promise<PlaybookDetail>;
  create: (payload: {
    name: string;
    description?: string | null;
    rules: PlaybookRuleInput[];
  }) => Promise<PlaybookDetail>;
  update: (
    id: string,
    payload: {
      name?: string;
      description?: string | null;
      rules?: PlaybookRuleInput[];
    },
  ) => Promise<PlaybookDetail>;
  remove: (id: string) => Promise<void>;
}

export const usePlaybookStore = create<PlaybookState>((set, get) => ({
  items: [],
  loading: false,

  fetchAll: async () => {
    set({ loading: true });
    try {
      const { data } = await api.get<Playbook[]>("/playbooks");
      set({ items: data, loading: false });
    } catch {
      set({ loading: false });
    }
  },

  get: async (id) => {
    const { data } = await api.get<PlaybookDetail>(`/playbooks/${id}`);
    return data;
  },

  create: async (payload) => {
    const { data } = await api.post<PlaybookDetail>("/playbooks", payload);
    await get().fetchAll();
    return data;
  },

  update: async (id, payload) => {
    const { data } = await api.put<PlaybookDetail>(
      `/playbooks/${id}`,
      payload,
    );
    await get().fetchAll();
    return data;
  },

  remove: async (id) => {
    await api.delete(`/playbooks/${id}`);
    await get().fetchAll();
  },
}));
