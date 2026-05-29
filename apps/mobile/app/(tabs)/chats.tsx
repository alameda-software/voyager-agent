import { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity, Alert } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import { listConversations, deleteConversation } from "../../src/api/client";
import { MobileScreen } from "../../src/components/MobileScreen";
import { colors } from "../../src/theme";
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

  const handleDelete = (id: number, title: string) => {
    Alert.alert(
      "Delete Chat",
      `Are you sure you want to delete "${title}"?`,
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Delete",
          style: "destructive",
          onPress: async () => {
            try {
              await deleteConversation(id);
              setConversations((prev) => prev.filter((c) => c.id !== id));
            } catch (error) {
              Alert.alert("Error", "Failed to delete chat");
            }
          },
        },
      ]
    );
  };

  return (
    <MobileScreen padded={false} style={styles.screen}>
      <View style={styles.headerRow}>
        <Text style={styles.header}>Chats</Text>
        <TouchableOpacity style={styles.newChatBtn} onPress={() => router.push("/")}>
          <Ionicons name="add" size={26} color={colors.primary} />
        </TouchableOpacity>
      </View>
      <FlatList
        data={conversations}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={styles.itemWrapper}>
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
                  {item.domain === "voyager" ? "Travel concierge" : "Wedding concierge"}
                </Text>
              </View>
              <Text style={styles.badge}>{item.domain}</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.deleteBtn}
              onPress={() => handleDelete(item.id, item.title)}
            >
              <Ionicons name="trash-outline" size={20} color="#ef4444" />
            </TouchableOpacity>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.emptyText}>No conversations yet</Text>
            <Text style={styles.emptySub}>Tap + to start Voyager or Wedding</Text>
          </View>
        }
      />
    </MobileScreen>
  );
}

const styles = StyleSheet.create({
  screen: { paddingTop: 56 },
  headerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    marginBottom: 12,
  },
  header: { fontSize: 26, fontWeight: "700", color: colors.text },
  newChatBtn: { padding: 4 },
  itemWrapper: { flexDirection: "row", alignItems: "center" },
  item: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 14,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    flex: 1,
  },
  deleteBtn: {
    paddingHorizontal: 12,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    justifyContent: "center",
    alignItems: "center",
  },
  emoji: { fontSize: 26, marginRight: 12 },
  itemContent: { flex: 1 },
  title: { fontSize: 16, fontWeight: "600", color: colors.text },
  preview: { fontSize: 14, color: colors.textSecondary, marginTop: 3 },
  badge: { fontSize: 11, color: colors.primary, textTransform: "capitalize", fontWeight: "600" },
  empty: { alignItems: "center", marginTop: 60, paddingHorizontal: 16 },
  emptyText: { fontSize: 17, color: colors.textSecondary },
  emptySub: { fontSize: 14, color: colors.textMuted, marginTop: 8 },
});
