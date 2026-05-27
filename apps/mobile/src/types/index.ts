export type ConciergeDomain = "voyager" | "wedding";

export interface User {
  id: number;
  email: string;
  displayName: string | null;
}

export interface Conversation {
  id: number;
  userId: number;
  domain: ConciergeDomain;
  title: string;
  createdAt: string;
}

export interface Message {
  id: number;
  conversationId: number;
  role: "user" | "agent" | "system";
  content: string;
  payload?: MessagePayload | null;
  createdAt: string;
}

export interface WeddingVendorCard {
  id: string;
  name: string;
  category: string;
  category_label: string;
  city: string;
  region?: string | null;
  rating?: number | null;
  review_count?: number | null;
  price_from?: number | null;
  price_label?: string | null;
  short_description?: string | null;
  tags?: string[];
  capacity_min?: number | null;
  capacity_max?: number | null;
  featured?: boolean;
  promotion?: string | null;
  availability_hint?: string | null;
  image_url?: string | null;
}

export interface WeddingVendorCategory {
  id: string;
  label: string;
  description: string;
  icon: string;
  bodas_path: string;
  vendor_count: number;
}

export interface MessagePayload {
  mode?: string;
  domain?: ConciergeDomain;
  suggested_actions?: string[];
  type?: "text" | "flight_card" | "hotel_card" | "car_card" | "tour_card" | "vendor_cards" | "quick_replies";
  options?: string[];
  data?: Record<string, unknown> & {
    vendors?: WeddingVendorCard[];
    filters?: { category?: string | null; city?: string | null };
  };
  cards?: Record<string, unknown>[];
  category?: string;
  checklist?: Record<string, unknown>;
  [key: string]: unknown;
}

export interface StructuredState {
  conversation_id: number;
  domain: ConciergeDomain;
  payload: Record<string, unknown>;
  updated_at: string;
}

export interface ConversationDetailResponse {
  conversation: {
    id: number;
    user_id: number;
    domain: ConciergeDomain;
    title: string;
    created_at: string;
  };
  structured_state: StructuredState;
  messages: Array<{
    id: number;
    conversation_id: number;
    role: "user" | "agent" | "system";
    content: string;
    payload: MessagePayload | null;
    created_at: string;
  }>;
}

export interface CreateConversationRequest {
  user_id: number;
  domain: ConciergeDomain;
  title: string;
}

export interface SendMessageResponse {
  conversation: {
    id: number;
    user_id: number;
    domain: ConciergeDomain;
    title: string;
    created_at: string;
  };
  structured_state: StructuredState;
  user_message: {
    id: number;
    conversation_id: number;
    role: "user" | "agent" | "system";
    content: string;
    payload: MessagePayload | null;
    created_at: string;
  };
  agent_message: {
    id: number;
    conversation_id: number;
    role: "user" | "agent" | "system";
    content: string;
    payload: MessagePayload | null;
    created_at: string;
  };
}

export interface SearchResult {
  id: string;
  type: "flight" | "hotel" | "car" | "tour";
  title: string;
  price: number;
  currency: string;
  details: Record<string, unknown>;
}
