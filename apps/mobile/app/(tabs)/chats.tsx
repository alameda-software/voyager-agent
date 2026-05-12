import { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import { listConversations } from "../../src/api/client";
import type { ConciergeDomain } from "../../src/types";

const TEST_USER_ID = 1;

export default function ChatsScreen() {
  const [conversations, setConversations] = useState<
    Array<{ id: number; title: string; domain: ConciergeDomain; created_at: string }>
  >([]);

  useEffect(() => {
    void loadConversations();
  }, []);

  const loadConversations = async () => {
    const response = await listConversations(TEST_USER_ID);
    setConversations(response.data);
  };

  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.header}>Chats</Text>
        <TouchableOpacity style={styles.newChatBtn} onPress={() => router.push("/")}>
          <Ionicons name="add" size={24} color="#6c63ff" />
        </TouchableOpacity>
      </View>
      <FlatList
        data={conversations}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.item}
            onPress={() =>
              router.push({
                pathname: "/(tabs)/[id]",
                params: { id: String(item.id), title: item.title, domain: item.domain },
              })
            }
          >
            <Text style={styles.emoji}>{item.domain === "voyager" ? "✈️" : "💍"}</Text>
            <View style={styles.itemContent}>
              <Text style={styles.title}>{item.title}</Text>
              <Text style={styles.preview} numberOfLines={1}>
                {item.domain === "voyager" ? "Travel concierge session" : "Wedding concierge session"}
              </Text>
            </View>
            <Text style={styles.time}>{item.domain}</Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.emptyText}>No conversations yet</Text>
            <Text style={styles.emptySub}>Tap + to start Voyager or Wedding</Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f23", paddingTop: 60 },
  headerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  header: { fontSize: 28, fontWeight: "700", color: "#fff" },
  newChatBtn: { padding: 4 },
  item: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#1a1a2e",
  },
  emoji: { fontSize: 28, marginRight: 14 },
  itemContent: { flex: 1 },
  title: { fontSize: 16, fontWeight: "600", color: "#fff" },
  preview: { fontSize: 14, color: "#888", marginTop: 4 },
  time: { fontSize: 12, color: "#7dd3fc", textTransform: "capitalize" },
  empty: { alignItems: "center", marginTop: 80 },
  emptyText: { fontSize: 18, color: "#555" },
  emptySub: { fontSize: 14, color: "#444", marginTop: 8 },
});
