import { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ScrollView, Alert } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { getPlans, setPreferred, removeItem, getPlanSummary, type TripPlan, type PlanItem } from "../../src/store/plan";

function clearAllPlans() {
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('trip_plans');
    }
  } catch {}
}

function SectionHeader({ icon, title, count }: { icon: string; title: string; count: number }) {
  return (
    <View style={styles.sectionHeader}>
      <Text style={styles.sectionIcon}>{icon}</Text>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionBadge}>
        <Text style={styles.sectionBadgeText}>{count}</Text>
      </View>
    </View>
  );
}

function PlanItemRow({ item, planId, onUpdate }: { item: PlanItem; planId: string; onUpdate: () => void }) {
  const d = item.data;
  const [reserved, setReserved] = useState(item.reserved || false);
  let title = '';
  let subtitle = '';
  let price = '';

  if (item.type === 'flight') {
    title = `${d.airline} · ${d.departure} → ${d.arrival}`;
    subtitle = `${d.origin} → ${d.destination} · ${d.stops_label} · ${d.duration}`;
    price = `€${d.price_per_person}/pax`;
  } else if (item.type === 'hotel') {
    title = d.name;
    subtitle = `${d.location} · ${'⭐'.repeat(d.stars || 3)}`;
    price = `€${d.price_per_night}/noche`;
  } else if (item.type === 'car') {
    title = `${d.company} · ${d.category}`;
    subtitle = `${d.model} · ${d.transmission}`;
    price = `€${d.price_per_day}/día`;
  } else if (item.type === 'vendor') {
    title = d.name;
    subtitle = d.style || d.vendor_type;
    price = d.price_display || '';
  }

  const handleReserve = () => {
    Alert.alert(
      reserved ? '✅ Ya reservado' : `Reservar ${title}`,
      reserved
        ? 'Este elemento ya está marcado como reservado.'
        : `¿Confirmar reserva de ${title} por ${price}?`,
      reserved
        ? [{ text: 'OK' }]
        : [
            { text: 'Cancelar', style: 'cancel' },
            {
              text: '✅ Reservar',
              onPress: () => {
                setReserved(true);
                setPreferred(planId, item.id);
                onUpdate();
              },
            },
          ]
    );
  };

  return (
    <View style={[styles.itemRow, item.preferred && styles.itemRowPreferred, reserved && styles.itemRowReserved]}>
      <TouchableOpacity
        style={styles.starBtn}
        onPress={() => { setPreferred(planId, item.id); onUpdate(); }}
      >
        <Text style={styles.starIcon}>{item.preferred ? '★' : '☆'}</Text>
      </TouchableOpacity>
      <View style={styles.itemContent}>
        <Text style={styles.itemTitle}>{title}</Text>
        <Text style={styles.itemSubtitle}>{subtitle}</Text>
        <Text style={styles.itemPrice}>{price}</Text>
      </View>
      <View style={styles.itemRight}>
        <TouchableOpacity
          style={[styles.reserveBtn, reserved && styles.reserveBtnDone]}
          onPress={handleReserve}
        >
          <Text style={[styles.reserveBtnText, reserved && styles.reserveBtnTextDone]}>
            {reserved ? '✅ Reservado' : 'Reservar'}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => { removeItem(planId, item.id); onUpdate(); }} style={styles.removeBtn}>
          <Ionicons name="close-circle-outline" size={18} color="#94a3b8" />
        </TouchableOpacity>
      </View>
    </View>
  );
}

function PlanCard({ plan, onUpdate }: { plan: TripPlan; onUpdate: () => void }) {
  const { flights, hotels, cars, vendors, totalEstimate } = getPlanSummary(plan);

  return (
    <View style={styles.planCard}>
      <View style={styles.planCardHeader}>
        <Text style={styles.planCardTitle}>{plan.domain === 'voyager' ? '✈️' : '💍'} {plan.title}</Text>
        {totalEstimate > 0 && (
          <Text style={styles.planCardEstimate}>~€{totalEstimate}/día est.</Text>
        )}
      </View>

      {flights.length > 0 && (
        <View style={styles.section}>
          <SectionHeader icon="✈️" title="Vuelos" count={flights.length} />
          {flights.map(item => <PlanItemRow key={item.id} item={item} planId={plan.id} onUpdate={onUpdate} />)}
        </View>
      )}
      {hotels.length > 0 && (
        <View style={styles.section}>
          <SectionHeader icon="🏨" title="Hoteles" count={hotels.length} />
          {hotels.map(item => <PlanItemRow key={item.id} item={item} planId={plan.id} onUpdate={onUpdate} />)}
        </View>
      )}
      {cars.length > 0 && (
        <View style={styles.section}>
          <SectionHeader icon="🚗" title="Coche" count={cars.length} />
          {cars.map(item => <PlanItemRow key={item.id} item={item} planId={plan.id} onUpdate={onUpdate} />)}
        </View>
      )}
      {vendors.length > 0 && (
        <View style={styles.section}>
          <SectionHeader icon="💍" title="Proveedores" count={vendors.length} />
          {vendors.map(item => <PlanItemRow key={item.id} item={item} planId={plan.id} onUpdate={onUpdate} />)}
        </View>
      )}

      {flights.length === 0 && hotels.length === 0 && cars.length === 0 && vendors.length === 0 && (
        <Text style={styles.emptyPlan}>Añade opciones desde el chat con "+ Añadir al plan"</Text>
      )}
    </View>
  );
}

export default function PlanScreen() {
  const [plans, setPlans] = useState<TripPlan[]>([]);

  const refresh = () => setPlans(getPlans().filter(p => p.items.length > 0));

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleClearAll = () => {
    Alert.alert(
      'Limpiar plan',
      '¿Eliminar todos los elementos del plan?',
      [
        { text: 'Cancelar', style: 'cancel' },
        { text: '🗑️ Limpiar todo', style: 'destructive', onPress: () => { clearAllPlans(); refresh(); } },
      ]
    );
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.headerRow}>
        <View>
          <Text style={styles.header}>Mi Plan</Text>
          <Text style={styles.headerSub}>★ marca tu preferida · Reservar para confirmar</Text>
        </View>
        {plans.length > 0 && (
          <TouchableOpacity onPress={handleClearAll} style={styles.clearBtn}>
            <Ionicons name="trash-outline" size={18} color="#ef4444" />
          </TouchableOpacity>
        )}
      </View>

      {plans.length === 0 ? (
        <View style={styles.empty}>
          <Text style={styles.emptyIcon}>🗺️</Text>
          <Text style={styles.emptyTitle}>Tu plan está vacío</Text>
          <Text style={styles.emptyText}>Ve al chat, busca vuelos, hoteles o coches y toca "+ Añadir al plan"</Text>
        </View>
      ) : (
        plans.map(plan => <PlanCard key={plan.id} plan={plan} onUpdate={refresh} />)
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f8fafc" },
  content: { padding: 20, paddingTop: 60, paddingBottom: 40 },
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24 },
  header: { fontSize: 28, fontWeight: "800", color: "#0f172a", marginBottom: 4 },
  headerSub: { fontSize: 13, color: "#64748b" },
  clearBtn: { padding: 8, backgroundColor: '#fff1f2', borderRadius: 10, borderWidth: 1, borderColor: '#fecaca' },
  planCard: {
    backgroundColor: "#ffffff", borderRadius: 20, padding: 16,
    borderWidth: 1, borderColor: "#e2e8f0", marginBottom: 20,
    shadowColor: "#000", shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06, shadowRadius: 8, elevation: 3,
  },
  planCardHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 16 },
  planCardTitle: { fontSize: 17, fontWeight: "700", color: "#0f172a", flex: 1 },
  planCardEstimate: { fontSize: 13, fontWeight: "600", color: "#2563eb" },
  section: { marginBottom: 12 },
  sectionHeader: { flexDirection: "row", alignItems: "center", marginBottom: 8, paddingBottom: 6, borderBottomWidth: 1, borderBottomColor: "#f1f5f9" },
  sectionIcon: { fontSize: 16, marginRight: 6 },
  sectionTitle: { fontSize: 13, fontWeight: "700", color: "#475569", textTransform: "uppercase", letterSpacing: 0.5, flex: 1 },
  sectionBadge: { backgroundColor: "#f1f5f9", paddingHorizontal: 8, paddingVertical: 2, borderRadius: 20 },
  sectionBadgeText: { fontSize: 11, fontWeight: "700", color: "#64748b" },
  itemRow: { flexDirection: "row", alignItems: "center", paddingVertical: 10, paddingHorizontal: 8, borderRadius: 12, marginBottom: 6, borderWidth: 1, borderColor: '#f1f5f9', backgroundColor: '#ffffff' },
  itemRowPreferred: { backgroundColor: "#eff6ff", borderColor: '#bfdbfe' },
  itemRowReserved: { backgroundColor: "#f0fdf4", borderColor: '#86efac' },
  starBtn: { marginRight: 8 },
  starIcon: { fontSize: 20, color: "#f59e0b" },
  itemContent: { flex: 1 },
  itemTitle: { fontSize: 13, fontWeight: "600", color: "#0f172a" },
  itemSubtitle: { fontSize: 11, color: "#64748b", marginTop: 1 },
  itemPrice: { fontSize: 12, fontWeight: "700", color: "#2563eb", marginTop: 3 },
  itemRight: { alignItems: 'flex-end', marginLeft: 8 },
  removeBtn: { marginTop: 6 },
  reserveBtn: { backgroundColor: '#2563eb', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8 },
  reserveBtnDone: { backgroundColor: '#dcfce7' },
  reserveBtnText: { fontSize: 12, fontWeight: '700', color: '#ffffff' },
  reserveBtnTextDone: { color: '#16a34a' },
  emptyPlan: { fontSize: 13, color: "#94a3b8", textAlign: "center", paddingVertical: 16 },
  empty: { alignItems: "center", paddingTop: 80 },
  emptyIcon: { fontSize: 56, marginBottom: 16 },
  emptyTitle: { fontSize: 20, fontWeight: "700", color: "#0f172a", marginBottom: 8 },
  emptyText: { fontSize: 14, color: "#64748b", textAlign: "center", lineHeight: 22, maxWidth: 280 },
});
