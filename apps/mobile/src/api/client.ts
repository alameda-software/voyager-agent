import axios from "axios";

import type {
  ConciergeDomain,
  ConversationDetailResponse,
  CreateConversationRequest,
  SendMessageResponse,
} from "../types";

// Lazy function to get API URL at request time
function getApiUrl(): string {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;

    // For development
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return "http://localhost:8000";
    }
    // For production at leafgate.es domain
    else if (hostname.includes("leafgate.es")) {
      return `${protocol}//api.leafgate.es`;
    }
    // Default: same domain, port 8000
    else {
      return `${protocol}//${hostname}:8000`;
    }
  }
  // Fallback for non-browser
  return "http://localhost:8000";
}

// Create axios instance with dynamic baseURL
export const api = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
});

// Intercept requests to set baseURL dynamically
api.interceptors.request.use((config) => {
  if (!config.baseURL) {
    config.baseURL = getApiUrl();
  }
  return config;
});

// Auth
export const login = (email: string, password: string) =>
  api.post("/api/v1/auth/login", { email, password });

export const register = (email: string, password: string, displayName: string) =>
  api.post("/api/v1/auth/register", { email, password, display_name: displayName });

// Chat
export const createConversation = (payload: CreateConversationRequest) =>
  api.post<ConversationDetailResponse>("/api/v1/chat/conversations", payload);

export const listConversations = (userId: number, domain?: ConciergeDomain) =>
  api.get("/api/v1/chat/conversations", { params: { user_id: userId, domain } });

export const getConversation = (conversationId: number) =>
  api.get<ConversationDetailResponse>(`/api/v1/chat/conversations/${conversationId}`);

export const sendMessage = (conversationId: number, content: string) =>
  api.post<SendMessageResponse>("/api/v1/chat/send", { conversation_id: conversationId, content });

export const getHistory = (conversationId: number) =>
  api.get(`/api/v1/chat/history?conversation_id=${conversationId}`);

// Search
export const searchFlights = (params: Record<string, string>) =>
  api.post("/api/v1/search/flights", params);

export const searchHotels = (params: Record<string, string>) =>
  api.post("/api/v1/search/hotels", params);

// Wedding vendors (Bodas.net-style MVP catalog)
export const getWeddingCategories = () => api.get("/api/v1/wedding/categories");

export const searchWeddingVendors = (params: {
  category?: string;
  city?: string;
  q?: string;
  limit?: number;
}) => api.get("/api/v1/wedding/vendors", { params });
