import { StyleSheet, Text, View } from "react-native";

import { colors } from "../theme";
import type { WeddingVendorCard } from "../types";

interface VendorCardProps {
  vendor: WeddingVendorCard;
  compact?: boolean;
}

export function VendorCard({ vendor, compact = false }: VendorCardProps) {
  return (
    <View style={[styles.card, compact && styles.cardCompact]}>
      <View style={styles.body}>
        <View style={styles.row}>
          <Text style={styles.category}>{vendor.category_label}</Text>
          {vendor.featured ? <Text style={styles.featured}>Destacado</Text> : null}
        </View>
        <Text style={styles.name} numberOfLines={2}>
          {vendor.name}
        </Text>
        <Text style={styles.location}>
          {vendor.city}
          {vendor.region ? ` · ${vendor.region}` : ""}
        </Text>
        {vendor.rating != null ? (
          <Text style={styles.rating}>
            ★ {vendor.rating.toFixed(1)} · {vendor.review_count ?? 0} opiniones
          </Text>
        ) : null}
        {vendor.price_label ? <Text style={styles.price}>{vendor.price_label}</Text> : null}
        {!compact && vendor.short_description ? (
          <Text style={styles.description} numberOfLines={2}>
            {vendor.short_description}
          </Text>
        ) : null}
        {vendor.promotion ? <Text style={styles.promotion}>{vendor.promotion}</Text> : null}
        {vendor.availability_hint && !compact ? (
          <Text style={styles.availability}>{vendor.availability_hint}</Text>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: 10,
    overflow: "hidden",
  },
  cardCompact: {
    marginBottom: 8,
  },
  body: {
    padding: 14,
    gap: 3,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  category: {
    color: colors.accent,
    fontSize: 11,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 0.4,
  },
  featured: {
    color: colors.warning,
    fontSize: 11,
    fontWeight: "700",
  },
  name: {
    color: colors.text,
    fontSize: 16,
    fontWeight: "700",
    marginTop: 2,
  },
  location: {
    color: colors.textSecondary,
    fontSize: 13,
  },
  rating: {
    color: colors.text,
    fontSize: 13,
    marginTop: 2,
  },
  price: {
    color: colors.primary,
    fontSize: 14,
    fontWeight: "600",
    marginTop: 2,
  },
  description: {
    color: colors.textSecondary,
    fontSize: 13,
    lineHeight: 18,
    marginTop: 4,
  },
  promotion: {
    color: colors.success,
    fontSize: 12,
    fontWeight: "600",
    marginTop: 4,
  },
  availability: {
    color: colors.textMuted,
    fontSize: 12,
    marginTop: 2,
  },
});
