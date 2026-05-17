import { useState } from "react";
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, Image } from "react-native";
import { Ionicons } from "@expo/vector-icons";

const CATEGORIES = [
  { id: "venue",       label: "Venues",      emoji: "🏛️" },
  { id: "catering",    label: "Catering",    emoji: "🍽️" },
  { id: "photography", label: "Foto",        emoji: "📸" },
  { id: "music",       label: "Música",      emoji: "🎵" },
  { id: "florist",     label: "Flores",      emoji: "💐" },
  { id: "cake",        label: "Tarta",       emoji: "🎂" },
  { id: "transport",   label: "Transporte",  emoji: "🚗" },
  { id: "beauty",      label: "Belleza",     emoji: "💄" },
  { id: "invitations", label: "Invitaciones",emoji: "💌" },
  { id: "planner",     label: "Planner",     emoji: "📋" },
];

const CATEGORY_IMAGES: Record<string, string[]> = {
  venue:       ["https://images.unsplash.com/photo-1519741497674-611481863552?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1464047736614-af63643285bf?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1519225421980-716433b7e5de?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1507504031003-b417219a0fde?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1478146059778-26028b07395a?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1510076857177-7470076d4098?w=600&h=240&fit=crop"],
  catering:    ["https://images.unsplash.com/photo-1555244162-803834f70033?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600&h=240&fit=crop"],
  photography: ["https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1519845081274-cf544b4cb74f?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=600&h=240&fit=crop"],
  music:       ["https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=600&h=240&fit=crop"],
  florist:     ["https://images.unsplash.com/photo-1490750967868-88df5691cc46?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1487530811015-780780616df2?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1453301109223-4a9f04e87419?w=600&h=240&fit=crop"],
  cake:        ["https://images.unsplash.com/photo-1464349153735-7db50ed83c84?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1535254973040-607b474cb50d?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1522767131594-6a5e8599b9a7?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&h=240&fit=crop"],
  transport:   ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1566008885218-90a4fc6780a3?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1474552226712-ac0f0961a954?w=600&h=240&fit=crop"],
  beauty:      ["https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1560869713-da86bd23f438?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&h=240&fit=crop"],
  invitations: ["https://images.unsplash.com/photo-1519655966628-3c7fe16e6b24?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1506806732259-39c2d0268443?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=600&h=240&fit=crop"],
  planner:     ["https://images.unsplash.com/photo-1543269664-647163ec1d7c?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1520854221256-17451cc331bf?w=600&h=240&fit=crop",
                "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?w=600&h=240&fit=crop"],
};

// Static vendor data (mirrors fake_data.py)
const VENDORS: Record<string, any[]> = {
  venue: [
    { name: "Hacienda Tierra Blanca", style: "Hacienda · Jardín", location: "Salteras, Sevilla", price_display: "Desde 85€/persona", capacity: 400, rating: 4.9, reviews: 476, badge: "🏆 Wedding Award", description: "De los más buscados en Sevilla. Más de 960 parejas." },
    { name: "Hacienda Alboreá", style: "Hacienda · Finca", location: "Sevilla", price_display: "Desde 69€/persona", capacity: 700, rating: 4.9, reviews: 312, badge: "🏆 Wedding Award", description: "Hasta 700 invitados. Instalaciones únicas para toda la boda." },
    { name: "Real Venta de Antequera", style: "Histórico · Clásico", location: "Sevilla", price_display: "Desde 4.000€ alquiler", capacity: 500, rating: 4.8, reviews: 203, badge: null, description: "Casi un siglo de historia. Esencia auténtica sevillana." },
    { name: "Hacienda El Alba", style: "Hacienda · Catering propio", location: "Santiponce", price_display: "Desde 88€/persona", capacity: 500, rating: 4.8, reviews: 178, badge: null, description: "Gestionada por Catering Joaquín Jaén." },
    { name: "Robles Bodas Espacio", style: "Hacienda Andaluza", location: "Triana, Sevilla", price_display: "Desde 50€/persona", capacity: 400, rating: 4.7, reviews: 132, badge: null, description: "A 5 min de Triana. Tres salones + carpa." },
    { name: "Cortijo El Esparragal", style: "Cortijo · Catering propio", location: "Sevilla", price_display: "Desde 87€/persona", capacity: 400, rating: 4.8, reviews: 221, badge: "🏆 Wedding Award", description: "Cortijo con catering de primera categoría." },
  ],
  catering: [
    { name: "Matalahúva Catering", style: "Mediterráneo · Creativo", location: "Alcalá de Guadaíra", price_display: "Desde 90€/persona", rating: 4.9, reviews: 198, badge: "🏆 Wedding Award", description: "98% de parejas lo recomiendan. Cocina creativa mediterránea." },
    { name: "Alabardero Catering", style: "Premium · Gastronómico", location: "Sevilla", price_display: "Desde 100€/persona", rating: 4.9, reviews: 234, badge: "🏆 Wedding Award", description: "La referencia gastronómica de Sevilla en eventos." },
    { name: "Medinaceli Catering", style: "Tradicional sevillano", location: "Sevilla", price_display: "Desde 95€/persona", rating: 4.8, reviews: 145, badge: null, description: "Todo el sabor de la gastronomía andaluza." },
    { name: "Pando Catering", style: "Alta cocina · Versátil", location: "Dos Hermanas", price_display: "Desde 70€/persona", rating: 4.8, reviews: 167, badge: null, description: "Gastronomía de primer nivel en hacienda propia." },
  ],
  photography: [
    { name: "Estamosgrabando", style: "Foto + Vídeo · Reportaje", location: "Sevilla", price_display: "Desde 1.600€", rating: 4.9, reviews: 284, badge: "🏆 Wedding Award", description: "Equipo de referencia en Sevilla. Enfoque documental." },
    { name: "Foto Stilo Azahar", style: "Clásico · Natural · Vídeo", location: "Sevilla", price_display: "Desde 395€", rating: 4.9, reviews: 210, badge: "🏆 Wedding Award", description: "Más de 30 años. 98% de recomendación." },
    { name: "Juan Luis Morilla", style: "Reportaje · Alta gama", location: "Sevilla", price_display: "Desde 2.400€", rating: 5.0, reviews: 64, badge: "🏆 Wedding Award", description: "Fotógrafo de referencia en Andalucía. Editorial." },
    { name: "Lola Pérez Studio", style: "Fine Art · Premium", location: "Sevilla", price_display: "Desde 1.850€", rating: 5.0, reviews: 38, badge: "🏆 Wedding Award", description: "Fotografía de autor, estilo artístico y elegante." },
    { name: "GetWild - Foto y Vídeo", style: "Documental · Artístico", location: "Sevilla", price_display: "Desde 1.390€", rating: 5.0, reviews: 17, badge: null, description: "Fotografía y vídeo con mirada única y personal." },
  ],
  music: [
    { name: "Elegancia de Fiesta", style: "DJ + Sonido + Animación", location: "Sevilla", price_display: "Desde 450€", rating: 4.9, reviews: 353, badge: "🏆 Wedding Award", description: "Sello de Oro desde 2011. 30 años de experiencia." },
    { name: "Grupo Bumburay", style: "Grupo en vivo · Versátil", location: "Sevilla", price_display: "Desde 1.100€", rating: 4.9, reviews: 145, badge: "🏆 Wedding Award", description: "Amplio repertorio para ceremonia, cóctel y baile." },
    { name: "Cuarteto Isbilya", style: "Cuarteto de cuerda · Clásico", location: "Sevilla", price_display: "Desde 600€", rating: 4.9, reviews: 78, badge: "🏆 Wedding Award", description: "Clásico para ceremonia y cóctel. Muy recomendado." },
    { name: "Grupo Reyther D'Akokán", style: "Salsa · Cubano · Latino", location: "Sevilla", price_display: "Desde 1.700€", rating: 4.8, reviews: 89, badge: null, description: "Quinteto en vivo. Salsa, bachata, merengue." },
  ],
  florist: [
    { name: "Flores Sevilla · La Azalea", style: "Romántico · Natural", location: "Sevilla", price_display: "Desde 800€", rating: 4.9, reviews: 134, badge: null, description: "Especialistas en bodas románticas. Decoración completa." },
    { name: "Jardín Secreto Eventos", style: "Boho · Silvestre", location: "Sevilla", price_display: "Desde 600€", rating: 4.8, reviews: 89, badge: null, description: "Flores de temporada y decoración de espacios." },
    { name: "La Espiga Dorada", style: "Moderno · Minimalista", location: "Sevilla", price_display: "Desde 900€", rating: 4.9, reviews: 112, badge: null, description: "Diseño floral minimalista. Premio mejor floristería 2024." },
  ],
  cake: [
    { name: "Dulce Evento · Pastelería Nupcial", style: "Artístico · A medida", location: "Sevilla", price_display: "Desde 350€", rating: 5.0, reviews: 203, badge: null, description: "Tartas de diseño único. Degustación gratuita." },
    { name: "La Tarta de Ana", style: "Fondant · Clásico", location: "Sevilla", price_display: "Desde 250€", rating: 4.9, reviews: 178, badge: null, description: "Especialistas en fondant artesanal. +500 bodas." },
    { name: "Sugar & Dreams", style: "Naked cake · Boho", location: "Sevilla", price_display: "Desde 280€", rating: 4.8, reviews: 145, badge: null, description: "Naked cakes con flores naturales. Muy instagrameable." },
  ],
  transport: [
    { name: "Bodas en Rolls Royce Sevilla", style: "Rolls Royce · Lujo", location: "Sevilla", price_display: "Desde 450€", rating: 5.0, reviews: 89, badge: null, description: "Rolls Royce Silver Shadow y Phantom." },
    { name: "Coche de Época Sevilla", style: "Vintage · Época", location: "Sevilla", price_display: "Desde 300€", rating: 4.9, reviews: 134, badge: null, description: "Jaguar, Citroën DS, Mercedes clásico." },
    { name: "Autocares Boda Sevilla", style: "Autobús invitados", location: "Sevilla", price_display: "Desde 280€", rating: 4.6, reviews: 45, badge: null, description: "Traslado de invitados. Conductor de librea." },
  ],
  beauty: [
    { name: "Maquillaje Nupcial · Rocío García", style: "Natural · Airbrush", location: "Sevilla", price_display: "Desde 250€", rating: 5.0, reviews: 312, badge: null, description: "Airbrush de larga duración. Prueba incluida. 500+ novias." },
    { name: "Estudio Novia Sevilla", style: "Makeup + Peluquería", location: "Sevilla", price_display: "Desde 350€", rating: 4.9, reviews: 234, badge: null, description: "Pack completo makeup + peinado para novia y séquito." },
    { name: "Glamour & Arte Nupcial", style: "Glam · Editorial", location: "Sevilla", price_display: "Desde 300€", rating: 4.8, reviews: 167, badge: null, description: "Especialistas en novias morenas. Estilo editorial." },
  ],
  invitations: [
    { name: "Papel & Tinta Bodas", style: "Artesanal · Letterpress", location: "Sevilla", price_display: "Desde 180€", rating: 4.9, reviews: 145, badge: null, description: "Letterpress artesanal. Diseño personalizado incluido." },
    { name: "Invitaciones Únicas SVQ", style: "Moderno · Minimalista", location: "Sevilla", price_display: "Desde 120€", rating: 4.8, reviews: 89, badge: null, description: "Diseños modernos. Entrega en 10 días laborables." },
    { name: "Detallería Nupcial", style: "Detalles + Invitaciones", location: "Sevilla", price_display: "Desde 200€", rating: 4.9, reviews: 112, badge: null, description: "Pack invitaciones + detalles para invitados." },
  ],
  planner: [
    { name: "Bodas con Alma · Sevilla", style: "Full planning · Coordinación", location: "Sevilla", price_display: "Desde 2.500€", rating: 5.0, reviews: 89, badge: null, description: "Wedding planner full service. Desde el primer día." },
    { name: "Eventos & Sueños", style: "Day coordination", location: "Sevilla", price_display: "Desde 800€", rating: 4.9, reviews: 134, badge: null, description: "Coordinación del día. Para que disfrutéis sin preocupaciones." },
    { name: "The Wedding Studio Sevilla", style: "Luxury · Destination", location: "Sevilla", price_display: "Desde 3.500€", rating: 4.9, reviews: 67, badge: null, description: "Especialistas en bodas de lujo y destination weddings." },
  ],
};

function VendorCard({ vendor, imageUrl }: { vendor: any; imageUrl?: string }) {
  return (
    <View style={styles.card}>
      {imageUrl && (
        <Image
          source={{ uri: imageUrl }}
          style={styles.cardImage}
          resizeMode="cover"
        />
      )}
      <View style={styles.cardBody}>
        <View style={styles.cardTop}>
          <View style={{ flex: 1 }}>
            <Text style={styles.vendorName}>{vendor.name}</Text>
            <Text style={styles.vendorStyle}>{vendor.style}</Text>
          </View>
          <View style={{ alignItems: 'flex-end' }}>
            <Text style={styles.rating}>⭐ {vendor.rating}</Text>
            <Text style={styles.reviews}>{vendor.reviews} op.</Text>
          </View>
        </View>
        <Text style={styles.description}>{vendor.description}</Text>
        <View style={styles.cardBottom}>
          <Text style={styles.price}>{vendor.price_display}</Text>
          {vendor.badge && <Text style={styles.badge}>{vendor.badge}</Text>}
        </View>
        <Text style={styles.location}>📍 {vendor.location}</Text>
      </View>
    </View>
  );
}

export default function BrowseScreen() {
  const [activeCategory, setActiveCategory] = useState("venue");
  const vendors = VENDORS[activeCategory] || [];

  const heroImg = (CATEGORY_IMAGES[activeCategory] || [])[0];

  return (
    <View style={styles.container}>
      {/* Hero banner */}
      {heroImg && (
        <View style={styles.hero}>
          <Image source={{ uri: heroImg }} style={styles.heroImage} resizeMode="cover" />
          <View style={styles.heroOverlay}>
            <Text style={styles.heroEmoji}>{CATEGORIES.find(c => c.id === activeCategory)?.emoji}</Text>
            <Text style={styles.heroTitle}>{CATEGORIES.find(c => c.id === activeCategory)?.label}</Text>
          </View>
        </View>
      )}
      {!heroImg && <Text style={styles.header}>Proveedores</Text>}

      {/* Category tabs */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.tabScroll}
        contentContainerStyle={styles.tabContainer}
      >
        {CATEGORIES.map(cat => (
          <TouchableOpacity
            key={cat.id}
            style={[styles.tab, activeCategory === cat.id && styles.tabActive]}
            onPress={() => setActiveCategory(cat.id)}
          >
            <Text style={styles.tabEmoji}>{cat.emoji}</Text>
            <Text style={[styles.tabLabel, activeCategory === cat.id && styles.tabLabelActive]}>
              {cat.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Vendor list */}
      <ScrollView style={styles.list} contentContainerStyle={styles.listContent}>
        {vendors.map((v, i) => {
          const imgs = CATEGORY_IMAGES[activeCategory] || [];
          const imgUrl = imgs[i % imgs.length];
          return <VendorCard key={i} vendor={v} imageUrl={imgUrl} />;
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f8fafc" },
  header: { fontSize: 22, fontWeight: "800", color: "#0f172a", paddingHorizontal: 16, paddingTop: 56, paddingBottom: 10 },
  hero: { width: '100%', height: 180, position: 'relative' },
  heroImage: { width: '100%', height: 180 },
  heroOverlay: { position: 'absolute', bottom: 0, left: 0, right: 0, padding: 16, backgroundColor: 'rgba(0,0,0,0.38)' },
  heroEmoji: { fontSize: 28, marginBottom: 2 },
  heroTitle: { fontSize: 22, fontWeight: '800', color: '#ffffff' },
  tabScroll: { maxHeight: 56, flexGrow: 0 },
  tabContainer: { paddingHorizontal: 12, paddingBottom: 8, flexDirection: 'row' },
  tab: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 6, marginRight: 8, borderRadius: 20, backgroundColor: '#ffffff', borderWidth: 1, borderColor: '#e2e8f0' },
  tabActive: { backgroundColor: '#2563eb', borderColor: '#2563eb' },
  tabEmoji: { fontSize: 14, marginRight: 4 },
  tabLabel: { fontSize: 12, fontWeight: '600', color: '#64748b' },
  tabLabelActive: { color: '#ffffff' },
  list: { flex: 1 },
  listContent: { padding: 12, paddingBottom: 32 },
  card: { backgroundColor: '#ffffff', borderRadius: 16, marginBottom: 14, borderWidth: 1, borderColor: '#e2e8f0', shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.08, shadowRadius: 6, elevation: 3, overflow: 'hidden' },
  cardImage: { width: '100%', height: 160 },
  cardBody: { padding: 14 },
  cardTop: { flexDirection: 'row', marginBottom: 6 },
  vendorName: { fontSize: 14, fontWeight: '700', color: '#0f172a', marginBottom: 2 },
  vendorStyle: { fontSize: 12, color: '#64748b' },
  rating: { fontSize: 13, fontWeight: '700', color: '#f59e0b' },
  reviews: { fontSize: 11, color: '#94a3b8', marginTop: 1 },
  description: { fontSize: 12, color: '#475569', lineHeight: 18, marginBottom: 8 },
  cardBottom: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  price: { fontSize: 13, fontWeight: '700', color: '#2563eb' },
  badge: { fontSize: 11, color: '#d97706' },
  location: { fontSize: 11, color: '#94a3b8', marginTop: 4 },
});
