import { View, Text, FlatList, StyleSheet } from "react-native";

// Placeholder — will be replaced with real conversation list
const conversations = [
  { id: "1", title: "✈️ Trip to London", preview: "Found 3 flights for next weekend...", time: "10:30" },
  { id: "2", title: "🏨 Hotels in Barcelona", preview: "I found some great options near...", time: "Yesterday" },
];

export default function ChatsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Chats</Text>
      <FlatList
        data={conversations}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <View style={styles.itemContent}>
              <Text style={styles.title}>{item.title}</Text>
              <Text style={styles.preview} numberOfLines={1}>{item.preview}</Text>
            </View>
            <Text style={styles.time}>{item.time}</Text>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.emptyText}>No conversations yet</Text>
            <Text style={styles.emptySub}>Start a new chat with VA</Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f23", paddingTop: 60 },
  header: { fontSize: 28, fontWeight: "700", color: "#fff", paddingHorizontal: 20, marginBottom: 16 },
  item: {
    flexDirection: "row",
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#1a1a2e",
  },
  itemContent: { flex: 1 },
  title: { fontSize: 16, fontWeight: "600", color: "#fff" },
  preview: { fontSize: 14, color: "#888", marginTop: 4 },
  time: { fontSize: 12, color: "#666" },
  empty: { alignItems: "center", marginTop: 80 },
  emptyText: { fontSize: 18, color: "#555" },
  emptySub: { fontSize: 14, color: "#444", marginTop: 8 },
});
