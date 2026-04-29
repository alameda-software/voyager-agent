import { View, Text, StyleSheet } from "react-native";

export default function SearchScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Search</Text>
      <Text style={styles.sub}>Quick search for flights, hotels, cars & more</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f23", justifyContent: "center", alignItems: "center" },
  text: { fontSize: 24, fontWeight: "700", color: "#fff" },
  sub: { fontSize: 14, color: "#666", marginTop: 8 },
});
