import { useEffect, useState } from "react";
import {
  FlatList,
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { router, useLocalSearchParams } from "expo-router";

import { getConversation, sendMessage } from "../../src/api/client";
import { addItemToPlan } from "../../src/store/plan";
import type { ConciergeDomain, MessagePayload, StructuredState } from "../../src/types";

interface ChatMessage {
  id: string;
  role: "user" | "agent" | "system";
  content: string;
  payload?: MessagePayload | null;
}

function AddToPlanButton({ onPress, added }: { onPress: () => void; added?: boolean }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={[styles.addPlanBtn, added && styles.addPlanBtnDone]}
    >
      <Text style={[styles.addPlanBtnText, added && styles.addPlanBtnTextDone]}>
        {added ? '✓ En el plan' : '+ Añadir al plan'}
      </Text>
    </TouchableOpacity>
  );
}

function FlightCard({ card, onAddToPlan }: { card: any; onAddToPlan?: () => void }) {
  return (
    <View style={styles.flightCard}>
      {/* Header: airline + price */}
      <View style={styles.flightHeader}>
        <View style={styles.flightAirlineRow}>
          <View style={styles.flightAirlineDot} />
          <Text style={[styles.flightAirlineName, { marginLeft: 8 }]}>{card.airline}</Text>
          <View style={[styles.flightBadge, card.stops === 0 && styles.flightBadgeDirect, { marginLeft: 8 }]}>
            <Text style={styles.flightBadgeText}>{card.stops_label}</Text>
          </View>
        </View>
        <View style={{ alignItems: 'flex-end' }}>
          <Text style={styles.flightPrice}>€{card.price_per_person}</Text>
          <Text style={styles.flightPriceSub}>por persona</Text>
        </View>
      </View>

      {/* Route row */}
      <View style={styles.flightRoute}>
        <View style={styles.flightEndpoint}>
          <Text style={styles.flightTime}>{card.departure}</Text>
          <Text style={styles.flightIata}>{card.origin}</Text>
          <Text style={styles.flightCity}>{card.origin_city}</Text>
        </View>
        <View style={styles.flightMiddle}>
          <Text style={styles.flightDuration}>{card.duration}</Text>
          <View style={styles.flightLine}>
            <View style={styles.flightLineDot} />
            <View style={styles.flightLineBar} />
            <Text style={{ fontSize: 14, color: '#94a3b8' }}>›</Text>
          </View>
          <Text style={styles.flightCabin}>{card.cabin}</Text>
        </View>
        <View style={[styles.flightEndpoint, { alignItems: 'flex-end' }]}>
          <Text style={styles.flightTime}>{card.arrival}</Text>
          <Text style={styles.flightIata}>{card.destination}</Text>
          <Text style={styles.flightCity}>{card.destination_city}</Text>
        </View>
      </View>

      {/* Footer */}
      <View style={styles.flightFooter}>
        <Text style={styles.flightSeats}>🔴 {card.seats_left} plazas</Text>
        {onAddToPlan && <AddToPlanButton onPress={onAddToPlan} />}
      </View>
    </View>
  );
}

function VendorCard({ card }: { card: any }) {
  return (
    <View style={styles.card}>
      <View style={styles.cardRow}>
        <Text style={styles.cardAirline}>{card.name}</Text>
        <Text style={styles.cardRating}>⭐ {card.rating}</Text>
      </View>
      <Text style={styles.cardStyle}>{card.style}</Text>
      <Text style={styles.cardSeats}>
        {card.price_per_head ? `Desde €${card.price_per_head}/persona` : card.price_from ? `Desde €${card.price_from}` : ''}
        {card.reviews ? ` · ${card.reviews} opiniones` : ''}
        {card.badge ? `  ${card.badge}` : ''}
      </Text>
    </View>
  );
}

function HotelCard({ card, onAddToPlan }: { card: any; onAddToPlan?: () => void }) {
  const stars = '⭐'.repeat(card.stars || 3);
  return (
    <View style={styles.card}>
      <View style={styles.cardRow}>
        <View style={{ flex: 1 }}>
          <Text style={styles.cardAirline}>{card.name}</Text>
          <Text style={styles.cardStyle}>{card.location}</Text>
        </View>
        <View style={{ alignItems: 'flex-end' }}>
          <Text style={styles.cardPrice}>€{card.price_per_night}<Text style={styles.cardPriceSub}>/noche</Text></Text>
          <Text style={styles.cardStops}>{stars}</Text>
        </View>
      </View>
      <Text style={styles.cardSeats}>{card.description}</Text>
      <Text style={styles.cardSeats}>★ {card.rating} · {card.reviews} opiniones · {card.nights} noches = €{card.total_price}</Text>
      {onAddToPlan && <AddToPlanButton onPress={onAddToPlan} />}
    </View>
  );
}

function CarCard({ card, onAddToPlan }: { card: any; onAddToPlan?: () => void }) {
  return (
    <View style={styles.card}>
      <View style={styles.cardRow}>
        <View style={{ flex: 1 }}>
          <Text style={styles.cardAirline}>{card.company} · {card.category}</Text>
          <Text style={styles.cardStyle}>{card.model}</Text>
        </View>
        <View style={{ alignItems: 'flex-end' }}>
          <Text style={styles.cardPrice}>€{card.price_per_day}<Text style={styles.cardPriceSub}>/día</Text></Text>
          <Text style={styles.cardSeats}>{card.days} días = €{card.total_price}</Text>
        </View>
      </View>
      <Text style={styles.cardSeats}>
        {card.transmission} · {card.seats} plazas · {card.ac ? 'AC' : ''} · {(card.included || []).join(', ')}
      </Text>
      {onAddToPlan && <AddToPlanButton onPress={onAddToPlan} />}
    </View>
  );
}

function stripMarkdown(text: string): string {
  return text
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/\*(.+?)\*/g, '$1')
    .replace(/^\d+\.\s.*/gm, '') // remove numbered list lines when cards are shown
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function MessageBubble({ message, conversationId, conversationTitle, domain }: {
  message: ChatMessage;
  conversationId: number;
  conversationTitle: string;
  domain: string;
}) {
  const isUser = message.role === "user";
  const cards = message.payload?.cards ?? [];
  const mode = message.payload?.mode;
  const hasCards = cards.length > 0;
  const [addedItems, setAddedItems] = useState<Set<number>>(new Set());

  const handleAddToPlan = (card: any, index: number, type: 'flight' | 'hotel' | 'car' | 'vendor') => {
    addItemToPlan(conversationId, conversationTitle, domain as any, { type, data: card });
    setAddedItems(prev => new Set([...prev, index]));
  };

  const displayText = hasCards ? stripMarkdown(message.content) : message.content;

  return (
    <View style={[styles.messageContainer, { alignItems: isUser ? "flex-end" : "flex-start" }]}>
      {displayText.length > 0 && (
        <View style={[styles.bubble, isUser ? styles.userBubble : styles.agentBubble]}>
          <Text style={isUser ? styles.userText : styles.agentText}>{displayText}</Text>
        </View>
      )}
      {cards.length > 0 && (
        <View style={styles.cardsContainer}>
          {cards.map((card: any, i: number) => {
            const added = addedItems.has(i);
            if (mode === 'flight_results') return <FlightCard key={i} card={card} onAddToPlan={added ? undefined : () => handleAddToPlan(card, i, 'flight')} />;
            if (mode === 'hotel_results') return <HotelCard key={i} card={card} onAddToPlan={added ? undefined : () => handleAddToPlan(card, i, 'hotel')} />;
            if (mode === 'car_results') return <CarCard key={i} card={card} onAddToPlan={added ? undefined : () => handleAddToPlan(card, i, 'car')} />;
            return <VendorCard key={i} card={card} />;
          })}
        </View>
      )}
    </View>
  );
}

export default function ChatScreen() {
  const { id, title, domain } = useLocalSearchParams<{ id: string; title?: string; domain?: ConciergeDomain }>();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [state, setState] = useState<StructuredState | null>(null);
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    if (!id) {
      return;
    }

    void loadConversation(Number(id));
  }, [id]);

  const loadConversation = async (conversationId: number) => {
    const response = await getConversation(conversationId);
    setState(response.data.structured_state);
    setMessages(
      response.data.messages.map((message) => ({
        id: String(message.id),
        role: message.role,
        content: message.content,
        payload: message.payload,
      })),
    );
  };

  const handleSend = async () => {
    if (!input.trim() || !id || isSending) {
      return;
    }

    try {
      setIsSending(true);
      const response = await sendMessage(Number(id), input.trim());
      setInput("");
      setState(response.data.structured_state);
      // Reload from server to get canonical state (avoids duplicates)
      await loadConversation(Number(id));
    } finally {
      setIsSending(false);
    }
  };

  const activeDomain = domain ?? state?.domain ?? "voyager";
  const plannerLabel = activeDomain === "voyager" ? "Voyager concierge" : "Wedding concierge";
  const placeholder = activeDomain === "voyager" ? "Describe your trip..." : "Describe your wedding plan...";

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      keyboardVerticalOffset={Platform.OS === "ios" ? 90 : 70}
    >
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.replace("/")} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#0f172a" />
        </TouchableOpacity>
        <View style={styles.headerCopy}>
          <Text style={styles.headerTitle}>{title || plannerLabel}</Text>
          <Text style={styles.headerSub}>{plannerLabel}</Text>
        </View>
        <View style={styles.domainBadge}>
          <Text style={styles.domainBadgeText}>{activeDomain}</Text>
        </View>
      </View>

      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <MessageBubble
            message={item}
            conversationId={Number(id)}
            conversationTitle={title || plannerLabel}
            domain={activeDomain}
          />
        )}
        contentContainerStyle={styles.messagesList}
        style={styles.messagesContainer}
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder={placeholder}
          placeholderTextColor="#64748b"
          onSubmitEditing={handleSend}
          returnKeyType="send"
          editable={!isSending}
        />
        <TouchableOpacity style={styles.sendButton} onPress={handleSend} disabled={isSending}>
          <Ionicons name="send" size={18} color="#ffffff" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#ffffff" },
  header: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingTop: Platform.OS === "ios" ? 52 : 32,
    paddingBottom: 10,
    backgroundColor: "#ffffff",
    borderBottomWidth: 1,
    borderBottomColor: "#e2e8f0",
  },
  backButton: { padding: 6, marginRight: 4 },
  headerCopy: { flex: 1 },
  headerTitle: { fontSize: 15, fontWeight: "700", color: "#0f172a" },
  headerSub: { fontSize: 11, color: "#2563eb", marginTop: 1, textTransform: "capitalize" },
  domainBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 999,
    backgroundColor: "#eff6ff",
  },
  domainBadgeText: { color: "#2563eb", fontSize: 11, fontWeight: "700", textTransform: "capitalize" },
  messagesContainer: { flex: 1, backgroundColor: "#f8fafc" },
  messagesList: { padding: 12, paddingBottom: 8, backgroundColor: "#f8fafc" },
  stateCard: { display: 'none' },
  stateTitle: { display: 'none' },
  stateBody: { display: 'none' },
  messageContainer: { marginBottom: 8 },
  bubble: { maxWidth: "88%", padding: 10, borderRadius: 16 },
  userBubble: { backgroundColor: "#2563eb", borderBottomRightRadius: 4 },
  agentBubble: { backgroundColor: "#ffffff", borderBottomLeftRadius: 4, borderWidth: 1, borderColor: "#e2e8f0" },
  userText: { color: "#ffffff", fontSize: 14, lineHeight: 20 },
  agentText: { color: "#1e293b", fontSize: 14, lineHeight: 20 },

  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: "#ffffff",
    borderTopWidth: 1,
    borderTopColor: "#e2e8f0",
  },
  input: {
    flex: 1,
    backgroundColor: "#f1f5f9",
    color: "#0f172a",
    borderRadius: 20,
    paddingHorizontal: 14,
    paddingVertical: 9,
    fontSize: 14,
    marginRight: 8,
  },
  sendButton: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: "#2563eb",
    alignItems: "center",
    justifyContent: "center",
  },
  cardsContainer: { marginTop: 6, width: '100%' },

  // Generic card
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: "#e2e8f0",
    marginBottom: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 2,
  },
  cardRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 4 },
  cardAirline: { fontSize: 14, fontWeight: "700", color: "#0f172a" },
  cardPrice: { fontSize: 16, fontWeight: "800", color: "#2563eb" },
  cardPriceSub: { fontSize: 11, fontWeight: "400", color: "#64748b" },
  cardFlight: { alignItems: "flex-start" },
  cardMiddle: { alignItems: "center", flex: 1 },
  cardTime: { fontSize: 16, fontWeight: "800", color: "#0f172a" },
  cardIata: { fontSize: 11, color: "#64748b", marginTop: 1 },
  cardDuration: { fontSize: 11, color: "#64748b" },
  cardStops: { fontSize: 10, color: "#2563eb", fontWeight: "600", marginTop: 1 },
  cardSeats: { fontSize: 11, color: "#94a3b8", marginTop: 3 },
  cardStyle: { fontSize: 12, color: "#475569", marginBottom: 3 },
  cardRating: { fontSize: 13, fontWeight: "700", color: "#f59e0b" },

  // Flight card
  flightCard: {
    backgroundColor: "#ffffff",
    borderRadius: 14,
    padding: 12,
    borderWidth: 1,
    borderColor: "#e2e8f0",
    marginBottom: 8,
    shadowColor: "#2563eb",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 8,
    elevation: 3,
  },
  flightHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 },
  flightAirlineRow: { flexDirection: 'row', alignItems: 'center' },
  flightAirlineDot: { width: 7, height: 7, borderRadius: 4, backgroundColor: '#2563eb' },
  flightAirlineName: { fontSize: 13, fontWeight: '700', color: '#0f172a' },
  flightBadge: { paddingHorizontal: 7, paddingVertical: 2, borderRadius: 20, backgroundColor: '#f1f5f9' },
  flightBadgeDirect: { backgroundColor: '#dcfce7' },
  flightBadgeText: { fontSize: 10, fontWeight: '700', color: '#475569' },
  flightPrice: { fontSize: 18, fontWeight: '800', color: '#2563eb' },
  flightPriceSub: { fontSize: 10, color: '#94a3b8', textAlign: 'right' },
  flightRoute: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  flightEndpoint: { alignItems: 'flex-start', minWidth: 60 },
  flightTime: { fontSize: 18, fontWeight: '800', color: '#0f172a' },
  flightIata: { fontSize: 11, fontWeight: '700', color: '#64748b', marginTop: 1 },
  flightCity: { fontSize: 10, color: '#94a3b8', marginTop: 1 },
  flightMiddle: { flex: 1, alignItems: 'center', paddingHorizontal: 6 },
  flightDuration: { fontSize: 10, color: '#64748b', marginBottom: 3 },
  flightLine: { flexDirection: 'row', alignItems: 'center', width: '100%' },
  flightLineDot: { width: 6, height: 6, borderRadius: 3, borderWidth: 1.5, borderColor: '#94a3b8' },
  flightLineBar: { flex: 1, height: 1.5, backgroundColor: '#cbd5e1' },

  flightCabin: { fontSize: 10, color: '#94a3b8', marginTop: 4 },
  flightFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingTop: 10, borderTopWidth: 1, borderTopColor: '#f1f5f9' },
  flightSeats: { fontSize: 11, color: '#ef4444' },
  flightTotal: { fontSize: 12, fontWeight: '600', color: '#64748b' },
  addPlanBtn: {
    marginTop: 10, paddingVertical: 8, borderRadius: 10,
    backgroundColor: '#eff6ff', borderWidth: 1, borderColor: '#bfdbfe',
    alignItems: 'center',
  },
  addPlanBtnDone: { backgroundColor: '#f0fdf4', borderColor: '#86efac' },
  addPlanBtnText: { fontSize: 13, fontWeight: '700', color: '#2563eb' },
  addPlanBtnTextDone: { color: '#16a34a' },
});
