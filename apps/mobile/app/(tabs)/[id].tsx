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
import type { ConciergeDomain, MessagePayload, StructuredState } from "../../src/types";

interface ChatMessage {
  id: string;
  role: "user" | "agent" | "system";
  content: string;
  payload?: MessagePayload | null;
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const actionHints = message.payload?.suggested_actions ?? [];

  return (
    <View style={[styles.messageContainer, { alignItems: isUser ? "flex-end" : "flex-start" }]}>
      <View style={[styles.bubble, isUser ? styles.userBubble : styles.agentBubble]}>
        <Text style={isUser ? styles.userText : styles.agentText}>{message.content}</Text>

      </View>
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
        renderItem={({ item }) => <MessageBubble message={item} />}
        contentContainerStyle={styles.messagesList}
        style={styles.messagesContainer}
        ListHeaderComponent={
          state ? (
            <View style={styles.stateCard}>
              <Text style={styles.stateTitle}>Structured state</Text>
              <Text style={styles.stateBody}>{JSON.stringify(state.payload, null, 2)}</Text>
            </View>
          ) : null
        }
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
    paddingHorizontal: 16,
    paddingTop: Platform.OS === "ios" ? 60 : 40,
    paddingBottom: 12,
    backgroundColor: "#ffffff",
    borderBottomWidth: 1,
    borderBottomColor: "#e2e8f0",
  },
  backButton: { padding: 4, marginRight: 8 },
  headerCopy: { flex: 1 },
  headerTitle: { fontSize: 18, fontWeight: "700", color: "#0f172a" },
  headerSub: { fontSize: 12, color: "#2563eb", marginTop: 2, textTransform: "capitalize" },
  domainBadge: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 999,
    backgroundColor: "#eff6ff",
  },
  domainBadgeText: { color: "#2563eb", fontSize: 12, fontWeight: "700", textTransform: "capitalize" },
  messagesContainer: { flex: 1, backgroundColor: "#f8fafc" },
  messagesList: { padding: 16, paddingBottom: 8, backgroundColor: "#f8fafc" },
  stateCard: {
    backgroundColor: "#f1f5f9",
    borderRadius: 18,
    padding: 14,
    marginBottom: 18,
    borderWidth: 1,
    borderColor: "#e2e8f0",
  },
  stateTitle: { color: "#2563eb", fontSize: 13, fontWeight: "700", marginBottom: 10, textTransform: "uppercase" },
  stateBody: { color: "#475569", fontSize: 12, lineHeight: 18, fontFamily: Platform.select({ ios: "Menlo", default: "monospace" }) },
  messageContainer: { marginBottom: 10 },
  bubble: { maxWidth: "88%", padding: 14, borderRadius: 18 },
  userBubble: { backgroundColor: "#2563eb", borderBottomRightRadius: 4 },
  agentBubble: { backgroundColor: "#ffffff", borderBottomLeftRadius: 4, borderWidth: 1, borderColor: "#e2e8f0" },
  userText: { color: "#ffffff", fontSize: 15, lineHeight: 22 },
  agentText: { color: "#1e293b", fontSize: 15, lineHeight: 22 },

  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 14,
    paddingVertical: 12,
    backgroundColor: "#ffffff",
    borderTopWidth: 1,
    borderTopColor: "#e2e8f0",
  },
  input: {
    flex: 1,
    backgroundColor: "#f1f5f9",
    color: "#0f172a",
    borderRadius: 16,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 15,
    marginRight: 10,
  },
  sendButton: {
    width: 42,
    height: 42,
    borderRadius: 14,
    backgroundColor: "#2563eb",
    alignItems: "center",
    justifyContent: "center",
  },
});
