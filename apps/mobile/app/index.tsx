import { useState } from "react";
import { ActivityIndicator, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import { createConversation } from "../src/api/client";
import type { ConciergeDomain } from "../src/types";

const TEST_USER_ID = 1;

const DOMAIN_OPTIONS: Array<{
  domain: ConciergeDomain;
  title: string;
  subtitle: string;
  icon: keyof typeof Ionicons.glyphMap;
}> = [
  {
    domain: "voyager",
    title: "Voyager",
    subtitle: "Plan trips, compare routes, and build itineraries.",
    icon: "airplane",
  },
  {
    domain: "wedding",
    title: "Wedding",
    subtitle: "Shortlist venues, vendors, and planning priorities.",
    icon: "heart",
  },
];

export default function HomeScreen() {
  const [activeDomain, setActiveDomain] = useState<ConciergeDomain | null>(null);

  const handleStart = async (domain: ConciergeDomain) => {
    try {
      setActiveDomain(domain);
      const title = domain === "voyager" ? "Voyager planning session" : "Wedding planning session";
      const response = await createConversation({
        user_id: TEST_USER_ID,
        domain,
        title,
      });

      router.replace({
        pathname: "/(tabs)/[id]",
        params: {
          id: String(response.data.conversation.id),
          title: response.data.conversation.title,
          domain: response.data.conversation.domain,
        },
      });
    } finally {
      setActiveDomain(null);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.hero}>
        <Text style={styles.eyebrow}>Pre-MVP Concierge Engine</Text>
        <Text style={styles.title}>Choose the concierge mode you want to test.</Text>
        <Text style={styles.subtitle}>
          Both flows share the same backend session engine, but load different domain logic.
        </Text>
      </View>

      <View style={styles.grid}>
        {DOMAIN_OPTIONS.map((option) => {
          const loading = activeDomain === option.domain;
          return (
            <TouchableOpacity
              key={option.domain}
              style={styles.card}
              onPress={() => handleStart(option.domain)}
              disabled={activeDomain !== null}
            >
              <View style={styles.iconWrap}>
                {loading ? (
                  <ActivityIndicator color="#ffffff" />
                ) : (
                  <Ionicons name={option.icon} size={28} color="#ffffff" />
                )}
              </View>
              <Text style={styles.cardTitle}>{option.title}</Text>
              <Text style={styles.cardSubtitle}>{option.subtitle}</Text>
              <Text style={styles.cardAction}>Open {option.title}</Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0b1220",
    paddingHorizontal: 24,
    paddingTop: 80,
    paddingBottom: 32,
  },
  hero: {
    marginBottom: 32,
  },
  eyebrow: {
    color: "#7dd3fc",
    fontSize: 13,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginBottom: 12,
  },
  title: {
    color: "#f8fafc",
    fontSize: 34,
    lineHeight: 40,
    fontWeight: "800",
    marginBottom: 12,
    maxWidth: 520,
  },
  subtitle: {
    color: "#94a3b8",
    fontSize: 16,
    lineHeight: 24,
    maxWidth: 640,
  },
  grid: {
    gap: 16,
  },
  card: {
    backgroundColor: "#111827",
    borderRadius: 22,
    padding: 22,
    borderWidth: 1,
    borderColor: "#1f2937",
  },
  iconWrap: {
    width: 56,
    height: 56,
    borderRadius: 18,
    backgroundColor: "#2563eb",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 18,
  },
  cardTitle: {
    color: "#f8fafc",
    fontSize: 24,
    fontWeight: "700",
    marginBottom: 8,
  },
  cardSubtitle: {
    color: "#94a3b8",
    fontSize: 15,
    lineHeight: 22,
    marginBottom: 18,
  },
  cardAction: {
    color: "#7dd3fc",
    fontSize: 15,
    fontWeight: "700",
  },
});
