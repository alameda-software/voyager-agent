import { useEffect, useMemo, useState } from "react";
import {
  Image,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

import { MobileScreen } from "../../src/components/MobileScreen";
import { colors } from "../../src/theme";
import { searchWeddingVendors, getWeddingCategories } from "../../src/api/client";

interface Category {
  id: string;
  label: string;
  description: string;
  icon: string;
  bodas_path: string;
  vendor_count: number;
}

interface Vendor {
  id: string;
  name: string;
  category: string;
  category_label: string;
  city: string;
  region?: string;
  rating?: number;
  review_count?: number;
  price_from?: number;
  price_label?: string;
  short_description?: string;
  tags: string[];
  capacity_min?: number;
  capacity_max?: number;
  featured: boolean;
  promotion?: string;
  availability_hint?: string;
  image_url?: string;
}

function VendorRow({ vendor }: { vendor: Vendor }) {
  return (
    <TouchableOpacity style={styles.vendorRow} activeOpacity={0.7}>
      {vendor.image_url && (
        <Image
          source={{ uri: vendor.image_url }}
          style={styles.vendorImage}
        />
      )}
      <View style={styles.vendorMain}>
        <Text style={styles.vendorName}>{vendor.name}</Text>
        <Text style={styles.vendorMeta}>{vendor.tags.slice(0, 2).join(" · ")}</Text>
        <Text style={styles.vendorLocation}>{vendor.city}</Text>
        {vendor.price_label && <Text style={styles.vendorPrice}>{vendor.price_label}</Text>}
      </View>
      <View style={styles.vendorAside}>
        {vendor.featured && <Text style={styles.vendorBadge}>Destacado</Text>}
        {vendor.rating && (
          <>
            <Text style={styles.vendorRating}>★ {vendor.rating.toFixed(1)}</Text>
            <Text style={styles.vendorReviews}>{vendor.review_count} opiniones</Text>
          </>
        )}
      </View>
    </TouchableOpacity>
  );
}

export default function BrowseScreen() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [activeCategory, setActiveCategory] = useState<string>("finca");
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("Sevilla");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    loadVendors();
  }, [activeCategory, location]);

  const loadCategories = async () => {
    try {
      const response = await getWeddingCategories();
      setCategories(response.data);
      if (response.data.length > 0) {
        setActiveCategory(response.data[0].id);
      }
    } catch (error) {
      console.error("Error loading categories:", error);
    }
  };

  const loadVendors = async () => {
    setLoading(true);
    try {
      const response = await searchWeddingVendors({
        category: activeCategory,
        city: location,
        limit: 20,
      });
      setVendors(response.data.results);
    } catch (error) {
      console.error("Error loading vendors:", error);
    } finally {
      setLoading(false);
    }
  };

  const activeMeta = categories.find((c) => c.id === activeCategory);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      return vendors;
    }
    return vendors.filter(
      (v) =>
        v.name.toLowerCase().includes(q) ||
        v.short_description?.toLowerCase().includes(q) ||
        v.city.toLowerCase().includes(q),
    );
  }, [vendors, query]);

  return (
    <View style={styles.page}>
      <MobileScreen padded={false} style={styles.column}>
        <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scroll}>
          <View style={styles.topPad} />
          <Text style={styles.breadcrumb}>Bodas / Proveedores</Text>
          <Text style={styles.pageTitle}>Proveedores</Text>

          <View style={styles.searchBox}>
            <View style={styles.searchField}>
              <Ionicons name="search-outline" size={18} color={colors.textMuted} />
              <TextInput
                style={styles.searchInput}
                placeholder="Proveedores"
                placeholderTextColor={colors.textMuted}
                value={query}
                onChangeText={setQuery}
              />
            </View>
            <View style={styles.searchDivider} />
            <View style={styles.searchField}>
              <Ionicons name="location-outline" size={18} color={colors.textMuted} />
              <TextInput
                style={styles.searchInput}
                placeholder="Dónde"
                placeholderTextColor={colors.textMuted}
                value={location}
                onChangeText={setLocation}
                onEndEditing={loadVendors}
              />
            </View>
          </View>

          <Text style={styles.sectionHeading}>Busca profesionales para tu boda por categoría</Text>

          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.categoryRow}
          >
            {categories.map((cat) => {
              const active = cat.id === activeCategory;
              return (
                <TouchableOpacity
                  key={cat.id}
                  style={[styles.categoryCard, active && styles.categoryCardActive]}
                  onPress={() => setActiveCategory(cat.id)}
                >
                  <Text style={[styles.categoryLabel, active && styles.categoryLabelActive]}>
                    {cat.label}
                  </Text>
                  <Text style={[styles.categoryCount, active && styles.categoryCountActive]}>
                    {cat.vendor_count} proveedores
                  </Text>
                </TouchableOpacity>
              );
            })}
          </ScrollView>

          {activeMeta ? (
            <View style={styles.categoryIntro}>
              <Text style={styles.categoryIntroTitle}>{activeMeta.label}</Text>
              <Text style={styles.categoryIntroText}>{activeMeta.description}</Text>
              <TouchableOpacity style={styles.ctaButton} activeOpacity={0.85}>
                <Text style={styles.ctaButtonText}>Ver {activeMeta.label.toLowerCase()}</Text>
              </TouchableOpacity>
            </View>
          ) : null}

          <Text style={styles.resultsLabel}>
            {loading ? "Cargando..." : `${filtered.length} resultados · ${location}`}
          </Text>

          <View style={styles.vendorList}>
            {filtered.map((vendor) => (
              <VendorRow key={vendor.id} vendor={vendor} />
            ))}
          </View>
        </ScrollView>
      </MobileScreen>
    </View>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: colors.background },
  column: { flex: 1 },
  scroll: { paddingBottom: 32 },
  topPad: { height: 48 },
  breadcrumb: {
    fontSize: 13,
    color: colors.textMuted,
    paddingHorizontal: 16,
    marginBottom: 6,
  },
  pageTitle: {
    fontSize: 32,
    fontWeight: "700",
    color: colors.text,
    paddingHorizontal: 16,
    marginBottom: 16,
    letterSpacing: -0.5,
  },
  searchBox: {
    flexDirection: "row",
    alignItems: "center",
    marginHorizontal: 16,
    marginBottom: 24,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.background,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  searchField: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 12,
    gap: 8,
  },
  searchDivider: {
    width: 1,
    alignSelf: "stretch",
    backgroundColor: colors.border,
    marginVertical: 8,
  },
  searchInput: {
    flex: 1,
    fontSize: 15,
    color: colors.text,
    padding: 0,
  },
  sectionHeading: {
    fontSize: 20,
    fontWeight: "700",
    color: colors.text,
    paddingHorizontal: 16,
    marginBottom: 14,
    lineHeight: 26,
  },
  categoryRow: {
    paddingHorizontal: 16,
    paddingBottom: 8,
    gap: 10,
  },
  categoryCard: {
    width: 140,
    paddingVertical: 14,
    paddingHorizontal: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.background,
  },
  categoryCardActive: {
    borderColor: colors.accent,
    backgroundColor: colors.accentSoft,
  },
  categoryLabel: {
    fontSize: 15,
    fontWeight: "700",
    color: colors.text,
    marginBottom: 6,
  },
  categoryLabelActive: {
    color: colors.accent,
  },
  categoryCount: {
    fontSize: 12,
    color: colors.textMuted,
  },
  categoryCountActive: {
    color: colors.accent,
  },
  categoryIntro: {
    paddingHorizontal: 16,
    paddingTop: 20,
    paddingBottom: 8,
  },
  categoryIntroTitle: {
    fontSize: 22,
    fontWeight: "700",
    color: colors.text,
    marginBottom: 8,
  },
  categoryIntroText: {
    fontSize: 15,
    lineHeight: 22,
    color: colors.textSecondary,
    marginBottom: 14,
  },
  ctaButton: {
    alignSelf: "flex-start",
    backgroundColor: colors.accent,
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 24,
  },
  ctaButtonText: {
    color: "#ffffff",
    fontSize: 15,
    fontWeight: "700",
  },
  resultsLabel: {
    fontSize: 13,
    color: colors.textMuted,
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 8,
  },
  vendorList: {
    borderTopWidth: 1,
    borderTopColor: colors.border,
    marginHorizontal: 16,
  },
  vendorRow: {
    flexDirection: "row",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    gap: 12,
    alignItems: "flex-start",
  },
  vendorImage: {
    width: 80,
    height: 80,
    borderRadius: 8,
    backgroundColor: colors.border,
  },
  vendorMain: { flex: 1, paddingTop: 2 },
  vendorName: {
    fontSize: 16,
    fontWeight: "700",
    color: colors.text,
    marginBottom: 3,
  },
  vendorMeta: {
    fontSize: 13,
    color: colors.textSecondary,
    marginBottom: 2,
  },
  vendorLocation: {
    fontSize: 13,
    color: colors.textMuted,
    marginBottom: 6,
  },
  vendorPrice: {
    fontSize: 14,
    fontWeight: "600",
    color: colors.text,
  },
  vendorAside: { alignItems: "flex-end", minWidth: 72 },
  vendorBadge: {
    fontSize: 10,
    fontWeight: "700",
    color: colors.accent,
    textTransform: "uppercase",
    marginBottom: 6,
    letterSpacing: 0.3,
  },
  vendorRating: {
    fontSize: 14,
    fontWeight: "700",
    color: colors.text,
  },
  vendorReviews: {
    fontSize: 12,
    color: colors.textMuted,
    marginTop: 2,
  },
});
