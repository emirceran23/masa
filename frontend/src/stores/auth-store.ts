import { create } from "zustand";
import type { User } from "@/types";
import { getMe, logout as doLogout } from "@/lib/auth";

interface AuthState {
  user: User | null;
  loading: boolean;
  setUser: (user: User | null) => void;
  fetchUser: () => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: true,

  setUser: (user) => set({ user, loading: false }),

  fetchUser: async () => {
    try {
      set({ loading: true });
      const user = await getMe();
      set({ user, loading: false });
    } catch {
      set({ user: null, loading: false });
    }
  },

  logout: () => {
    set({ user: null, loading: false });
    doLogout();
  },
}));
