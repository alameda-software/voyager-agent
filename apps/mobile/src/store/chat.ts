import { create } from "zustand";

interface Message {
  id: string;
  role: "user" | "agent" | "system";
  content: string;
  metadata?: Record<string, unknown>;
  createdAt: Date;
}

interface ChatStore {
  conversations: { id: number; title: string }[];
  currentConversation: number | null;
  messages: Message[];
  setConversations: (conversations: { id: number; title: string }[]) => void;
  setCurrentConversation: (id: number) => void;
  addMessage: (message: Message) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  conversations: [],
  currentConversation: null,
  messages: [],
  setConversations: (conversations) => set({ conversations }),
  setCurrentConversation: (id) => set({ currentConversation: id, messages: [] }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  clearMessages: () => set({ messages: [] }),
}));
