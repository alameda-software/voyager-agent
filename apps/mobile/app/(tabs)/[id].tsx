import { View, Text, StyleSheet, FlatList, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform } from "react-native";
import { useState } from "react";
import { Ionicons } from "@expo/vector-icons";
import { router, useLocalSearchParams } from "expo-router";

// --- Types ---
type MessageType = "text" | "flight_card" | "flight_results";

interface Message {
  id: string;
  role: "user" | "agent";
  type: MessageType;
  content: string;
  data?: FlightResult[];
  timestamp: Date;
}

interface FlightResult {
  id: string;
  airline: string;
  departure: string;
  arrival: string;
  departureTime: string;
  arrivalTime: string;
  duration: string;
  stops: number;
  price: number;
  currency: string;
  cabin: string;
}

// --- Flight Card Component ---
function FlightCard({ flight }: { flight: FlightResult }) {
  return (
    <View style={styles.flightCard}>
      <View style={styles.flightHeader}>
        <Text style={styles.airline}>{flight.airline}</Text>
        <View style={styles.priceBadge}>
          <Text style={styles.priceText}>{flight.price} {flight.currency}</Text>
        </View>
      </View>

      <View style={styles.flightRoute}>
        <View style={styles.routePoint}>
          <Text style={styles.time}>{flight.departureTime}</Text>
          <Text style={styles.airport}>{flight.departure}</Text>
        </View>

        <View style={styles.routeLine}>
          <View style={styles.line} />
          <Ionicons name="airplane" size={16} color="#6c63ff" />
          <View style={styles.line} />
        </View>

        <View style={styles.routePoint}>
          <Text style={styles.time}>{flight.arrivalTime}</Text>
          <Text style={styles.airport}>{flight.arrival}</Text>
        </View>
      </View>

      <View style={styles.flightFooter}>
        <Text style={styles.detail}>{flight.duration}</Text>
        <Text style={styles.detail}>
          {flight.stops === 0 ? "Direct" : `${flight.stops} stop${flight.stops > 1 ? "s" : ""}`}
        </Text>
        <Text style={styles.detail}>{flight.cabin}</Text>
      </View>

      <TouchableOpacity style={styles.bookButton}>
        <Text style={styles.bookButtonText}>Book</Text>
      </TouchableOpacity>
    </View>
  );
}

// --- Message Renderer ---
function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  if (message.type === "flight_results" && message.data) {
    return (
      <View style={[styles.messageContainer, { alignItems: "flex-start" }]}>
        <View style={styles.agentBubble}>
          <Text style={styles.agentText}>{message.content}</Text>
          <View style={styles.cardsContainer}>
            {message.data.map((flight) => (
              <FlightCard key={flight.id} flight={flight} />
            ))}
          </View>
        </View>
      </View>
    );
  }

  return (
    <View style={[styles.messageContainer, { alignItems: isUser ? "flex-end" : "flex-start" }]}>
      <View style={[styles.bubble, isUser ? styles.userBubble : styles.agentBubble]}>
        <Text style={isUser ? styles.userText : styles.agentText}>{message.content}</Text>
      </View>
    </View>
  );
}

// --- Main Chat Screen ---
export default function ChatScreen() {
  const { id, title } = useLocalSearchParams<{ id: string; title: string }>();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "0",
      role: "agent",
      type: "text",
      content: "Hey! Where are you heading? I can search flights for you. ✈️",
      timestamp: new Date(),
    },
    // Demo: simulate flight results
    {
      id: "1",
      role: "user",
      type: "text",
      content: "Find me a flight from SVQ to LHR next Friday",
      timestamp: new Date(),
    },
    {
      id: "2",
      role: "agent",
      type: "flight_results",
      content: "Here are some options for Seville → London:",
      timestamp: new Date(),
      data: [
        {
          id: "f1",
          airline: "Ryanair",
          departure: "SVQ",
          arrival: "STN",
          departureTime: "06:30",
          arrivalTime: "08:45",
          duration: "2h 15m",
          stops: 0,
          price: 49,
          currency: "€",
          cabin: "Economy",
        },
        {
          id: "f2",
          airline: "Vueling",
          departure: "SVQ",
          arrival: "LGW",
          departureTime: "10:15",
          arrivalTime: "12:30",
          duration: "2h 15m",
          stops: 0,
          price: 78,
          currency: "€",
          cabin: "Economy",
        },
        {
          id: "f3",
          airline: "British Airways",
          departure: "SVQ",
          arrival: "LHR",
          departureTime: "14:20",
          arrivalTime: "17:50",
          duration: "3h 30m",
          stops: 1,
          price: 142,
          currency: "€",
          cabin: "Economy",
        },
      ],
    },
  ]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      type: "text",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    // TODO: send to API, get agent response
    // For now, simulate agent thinking
    setTimeout(() => {
      const agentMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "agent",
        type: "text",
        content: "Got it! Searching for flights... 🔍",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, agentMsg]);
    }, 1000);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      keyboardVerticalOffset={Platform.OS === "ios" ? 90 : 70}
    >
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{title || "VoyagerAgent"}</Text>
        <View style={{ width: 24 }} />
      </View>

      {/* Messages */}
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => <MessageBubble message={item} />}
        contentContainerStyle={styles.messagesList}
        style={styles.messagesContainer}
      />

      {/* Input */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Search flights, hotels..."
          placeholderTextColor="#555"
          onSubmitEditing={handleSend}
          returnKeyType="send"
        />
        <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
          <Ionicons name="send" size={20} color="#6c63ff" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f23" },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingTop: Platform.OS === "ios" ? 60 : 40,
    paddingBottom: 12,
    backgroundColor: "#1a1a2e",
    borderBottomWidth: 1,
    borderBottomColor: "#2a2a4a",
  },
  backButton: { padding: 4 },
  headerTitle: { fontSize: 18, fontWeight: "700", color: "#fff" },

  messagesContainer: { flex: 1 },
  messagesList: { padding: 16, paddingBottom: 8 },
  messageContainer: { marginBottom: 8 },

  bubble: {
    maxWidth: "85%",
    padding: 12,
    borderRadius: 16,
  },
  userBubble: {
    backgroundColor: "#6c63ff",
    borderBottomRightRadius: 4,
  },
  agentBubble: {
    backgroundColor: "#1a1a2e",
    borderBottomLeftRadius: 4,
  },
  userText: { color: "#fff", fontSize: 15 },
  agentText: { color: "#e0e0e0", fontSize: 15 },

  // Flight cards
  cardsContainer: { marginTop: 12 },
  flightCard: {
    backgroundColor: "#252545",
    borderRadius: 12,
    padding: 14,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: "#333366",
  },
  flightHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 12,
  },
  airline: { color: "#fff", fontSize: 15, fontWeight: "600" },
  priceBadge: {
    backgroundColor: "#6c63ff20",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  priceText: { color: "#6c63ff", fontSize: 14, fontWeight: "700" },

  flightRoute: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
  },
  routePoint: { flex: 1, alignItems: "center" },
  time: { color: "#fff", fontSize: 18, fontWeight: "700" },
  airport: { color: "#888", fontSize: 12, marginTop: 2 },
  routeLine: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 8,
  },
  line: {
    flex: 1,
    height: 1,
    backgroundColor: "#6c63ff40",
  },

  flightFooter: {
    flexDirection: "row",
    justifyContent: "space-around",
    paddingVertical: 8,
    borderTopWidth: 1,
    borderTopColor: "#333366",
  },
  detail: { color: "#888", fontSize: 12 },

  bookButton: {
    backgroundColor: "#6c63ff",
    borderRadius: 8,
    padding: 10,
    alignItems: "center",
    marginTop: 10,
  },
  bookButtonText: { color: "#fff", fontSize: 14, fontWeight: "600" },

  // Input
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: "#1a1a2e",
    borderTopWidth: 1,
    borderTopColor: "#2a2a4a",
  },
  input: {
    flex: 1,
    backgroundColor: "#252545",
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    color: "#fff",
    fontSize: 15,
    marginRight: 8,
  },
  sendButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#1a1a2e",
    alignItems: "center",
    justifyContent: "center",
  },
});
