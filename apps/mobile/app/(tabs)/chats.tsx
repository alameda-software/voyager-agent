import { View, Text, FlatList, StyleSheet, TouchableOpacity } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { useState } from "react";

interface Conversation {
  id: string;
  title: string;
  preview: string;
  time: string;
  emoji: string;
}

// Demo data
const initialConversations: Conversation[] = [
  { id: "1", title: "Trip to London", preview: "Found 3 flights for next weekend...", time: "10:30", emoji: "✈️" },
];

export default function ChatsScreen() {
  const [conversations, setConversations] = useState<Conversation[]>(initialConversations);

  const startNewChat = () => {
    const newId = Date.now().toString();
    const newConv: Conversation = {
      id: newId,
      title: "New search",
      preview: "Where are you heading?",
      time: "Now",
      emoji: "🌍",
    };
    setConversations((prev) => [newConv, ...prev]);
    router.push({ pathname: "/(tabs)/[id]", params: { id: newId, title: "New search" } });
  };

  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.header}>Chats</Text>
        <TouchableOpacity style={styles.newChatBtn} onPress={startNewChat}>
          <Ionicons name="add" size={24} color="#6c63ff" />
        </TouchableOpacity>
      </View>
      <FlatList
        data={conversations}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.item}
            onPress={() => router.push({ pathname: "/(tabs)/[id]", params: { id: item.id, title: item.title } })}
          >
            <Text style={styles.emoji}>{item.emoji}</Text>
            <View style={styles.itemContent}>
              <Text style={styles.title}>{item.title}</Text>
              <Text style={styles.preview} numberOfLines={1}>{item.preview}</Text>
            </View>
            <Text style={styles.time}>{item.time}</Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.emptyText}>No conversations yet</Text>
            <Text style={styles.emptySub}>Tap + to start searching</Text>
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
  time: { fontSize: 12, color: "#666" },
  empty: { alignItems: "center", marginTop: 80 },
  emptyText: { fontSize: 18, color: "#555" },
  emptySub: { fontSize: 14, color: "#444", marginTop: 8 },
});
