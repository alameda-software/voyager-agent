import { useState, useEffect } from "react";
import { ActivityIndicator, ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import { createConversation } from "../../src/api/client";
import { MobileScreen } from "../../src/components/MobileScreen";
import { colors } from "../../src/theme";
import type { ConciergeDomain } from "../../src/types";
import { getUser, clearAuth, type UserProfile } from "../../src/store/auth";

const TEST_USER_ID = 1;

const DOMAIN_OPTIONS = [
  {
    domain: "voyager" as ConciergeDomain,
    title: "Voyager",
    subtitle: "Flights, hotels, cars & itineraries",
    icon: "airplane" as const,
    color: "#2563eb",
    bg: "#eff6ff",
  },
  {
    domain: "wedding" as ConciergeDomain,
    title: "Wedding",
    subtitle: "Venues, vendors & planning",
    icon: "heart" as const,
    color: "#db2777",
    bg: "#fdf2f8",
  },
];

export default function HomeTab() {
  const [activeDomain, setActiveDomain] = useState<ConciergeDomain | null>(null);
  const [user, setUser] = useState<UserProfile | null>(null);

  useEffect(() => {
    setUser(getUser());
  }, []);

  const handleLogout = () => {
    clearAuth();
    setUser(null);
    router.replace('/login');
  };

  const handleStart = async (domain: ConciergeDomain) => {
    try {
      setActiveDomain(domain);
      const title = domain === "voyager" ? "Voyager planning session" : "Wedding planning session";
      const response = await createConversation({ user_id: TEST_USER_ID, domain, title });
      router.push({
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
    <MobileScreen padded={false} style={styles.screen}>
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.container}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <View style={styles.headerTop}>
            <Text style={styles.logo}>✦ LiveGate</Text>
            {user ? (
              <View style={styles.userPill}>
                <Text style={styles.userPillText}>{user.display_name || user.email.split('@')[0]}</Text>
                <TouchableOpacity onPress={handleLogout} style={styles.logoutBtn}>
                  <Ionicons name="log-out-outline" size={15} color="#64748b" />
                </TouchableOpacity>
              </View>
            ) : (
              <TouchableOpacity onPress={() => router.push('/login')} style={styles.loginBtn}>
                <Text style={styles.loginBtnText}>Entrar</Text>
              </TouchableOpacity>
            )}
          </View>
          <Text style={styles.title}>
            {user ? `Hola, ${user.display_name || user.email.split('@')[0]} 👋` : 'What are you planning?'}
          </Text>
          <Text style={styles.subtitle}>Your AI assistant will guide you step by step.</Text>
        </View>

        <View style={styles.grid}>
          {DOMAIN_OPTIONS.map((option) => {
            const loading = activeDomain === option.domain;
            return (
              <TouchableOpacity
                key={option.domain}
                style={[styles.card, { borderColor: option.color + "33" }]}
                onPress={() => handleStart(option.domain)}
                disabled={activeDomain !== null}
                activeOpacity={0.85}
              >
                <View style={[styles.iconWrap, { backgroundColor: option.bg }]}>
                  {loading ? (
                    <ActivityIndicator color={option.color} size="small" />
                  ) : (
                    <Ionicons name={option.icon} size={22} color={option.color} />
                  )}
                </View>
                <View style={styles.cardText}>
                  <Text style={styles.cardTitle}>{option.title}</Text>
                  <Text style={styles.cardSubtitle}>{option.subtitle}</Text>
                </View>
                <Ionicons name="chevron-forward" size={18} color="#cbd5e1" />
              </TouchableOpacity>
            );
          })}
        </View>

        <Text style={styles.hint}>Tap a mode to start chatting with your AI concierge</Text>
      </ScrollView>
    </MobileScreen>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#ffffff" },
  scroll: { flex: 1 },
  container: {
    flexGrow: 1,
    backgroundColor: "#ffffff",
    paddingHorizontal: 20,
    paddingTop: 64,
    paddingBottom: 32,
  },
  header: { marginBottom: 28 },
  logo: {
    fontSize: 13,
    fontWeight: "700",
    color: "#2563eb",
    letterSpacing: 1,
    marginBottom: 10,
    textTransform: "uppercase",
  },
  title: { fontSize: 26, fontWeight: "800", color: "#0f172a", lineHeight: 32, marginBottom: 8 },
  subtitle: { fontSize: 14, color: "#64748b", lineHeight: 20 },
  grid: { gap: 12 },
  card: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#ffffff",
    borderRadius: 16,
    padding: 16,
    borderWidth: 1.5,
    borderColor: "#e2e8f0",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  iconWrap: {
    width: 44,
    height: 44,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 14,
  },
  cardText: { flex: 1 },
  cardTitle: { fontSize: 16, fontWeight: "700", color: "#0f172a", marginBottom: 2 },
  cardSubtitle: { fontSize: 13, color: "#64748b", lineHeight: 18 },
  hint: { marginTop: 28, fontSize: 12, color: "#94a3b8", textAlign: "center" },
  headerTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 },
  userPill: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#f1f5f9', borderRadius: 20, paddingHorizontal: 12, paddingVertical: 5 },
  userPillText: { fontSize: 13, fontWeight: '600', color: '#0f172a', marginRight: 6 },
  logoutBtn: { padding: 2 },
  loginBtn: { backgroundColor: '#2563eb', borderRadius: 20, paddingHorizontal: 14, paddingVertical: 6 },
  loginBtnText: { color: '#fff', fontSize: 13, fontWeight: '700' },
});
