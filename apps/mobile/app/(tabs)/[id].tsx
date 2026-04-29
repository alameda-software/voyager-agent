import { View, Text, StyleSheet } from "react-native";

export default function ChatScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Chat</Text>
      <Text style={styles.sub}>Conversation with VA goes here</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f23", justifyContent: "center", alignItems: "center" },
  text: { fontSize: 24, fontWeight: "700", color: "#fff" },
  sub: { fontSize: 14, color: "#666", marginTop: 8 },
});
