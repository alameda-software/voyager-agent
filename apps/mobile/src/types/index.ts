export interface User {
  id: number;
  email: string;
  displayName: string | null;
}

export interface Conversation {
  id: number;
  userId: number;
  title: string;
  createdAt: string;
}

export interface Message {
  id: number;
  conversationId: number;
  role: "user" | "agent" | "system";
  content: string;
  metadata?: MessageMetadata | null;
  createdAt: string;
}

export interface MessageMetadata {
  type?: "text" | "flight_card" | "hotel_card" | "car_card" | "tour_card" | "quick_replies";
  options?: string[];
  data?: Record<string, unknown>;
}

export interface SearchResult {
  id: string;
  type: "flight" | "hotel" | "car" | "tour";
  title: string;
  price: number;
  currency: string;
  details: Record<string, unknown>;
}
