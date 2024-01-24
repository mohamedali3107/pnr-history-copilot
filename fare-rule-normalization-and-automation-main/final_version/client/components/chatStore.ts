import { create } from "zustand";
import { Message } from "ai";

interface ChatStore {
  chatHistory: Message[];
  addToHistory: (message: Message) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  chatHistory: [],
  addToHistory: (message) => set((state) => ({ chatHistory: [...state.chatHistory, message] })),
}));
