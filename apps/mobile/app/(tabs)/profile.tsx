import { useState } from "react";
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, TextInput } from "react-native";

const PHASES = [
  {
    months: "12+ meses antes",
    emoji: "📅",
    color: "#7c3aed",
    tasks: [
      "Fijar la fecha de boda",
      "Definir el presupuesto total",
      "Reservar venue/hacienda",
      "Elegir wedding planner (opcional)",
      "Lista de invitados preliminar",
    ],
  },
  {
    months: "9-12 meses antes",
    emoji: "📸",
    color: "#2563eb",
    tasks: [
      "Contratar fotógrafo y videógrafo",
      "Confirmar menú con catering",
      "Reservar música / DJ",
      "Buscar vestido de novia",
      "Consulta inicial con florista",
    ],
  },
  {
    months: "6-9 meses antes",
    emoji: "💌",
    color: "#0891b2",
    tasks: [
      "Encargar invitaciones",
      "Confirmar transporte (coche + bus invitados)",
      "Reservar hotel noche de bodas",
      "Elegir pastel de boda",
      "Reservar maquillaje y peluquería",
    ],
  },
  {
    months: "3-6 meses antes",
    emoji: "💍",
    color: "#db2777",
    tasks: [
      "Enviar invitaciones y confirmar asistencias",
      "Organizar seating plan",
      "Planificar luna de miel",
      "Traje del novio",
      "Detalles para invitados",
    ],
  },
  {
    months: "1-3 meses antes",
    emoji: "🌸",
    color: "#d97706",
    tasks: [
      "Confirmar todos los proveedores",
      "Entrega de arras y anillos",
      "Coordinación final con planner",
      "Ensayo de ceremonia",
      "Despedidas de soltero/a",
    ],
  },
  {
    months: "El gran día ✨",
    emoji: "🎉",
    color: "#16a34a",
    tasks: [
      "¡Despertad con calma!",
      "Maquillaje y peinado",
      "Fotos previas con fotógrafo",
      "Ceremonia",
      "Aperitivo · Banquete · Barra libre · ¡A bailar!",
    ],
  },
];

export default function CalendarScreen() {
  const [checked, setChecked] = useState<Set<string>>(new Set());
  const [weddingDate, setWeddingDate] = useState("");

  const toggle = (key: string) => {
    setChecked(prev => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  };

  const totalTasks = PHASES.reduce((sum, p) => sum + p.tasks.length, 0);
  const completedTasks = checked.size;
  const progress = Math.round((completedTasks / totalTasks) * 100);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.header}>📅 Calendario</Text>

      {/* Wedding date input */}
      <View style={styles.dateBox}>
        <Text style={styles.dateLabel}>Fecha de boda</Text>
        <TextInput
          style={styles.dateInput}
          value={weddingDate}
          onChangeText={setWeddingDate}
          placeholder="ej. 14 de junio de 2026"
          placeholderTextColor="#94a3b8"
        />
      </View>

      {/* Progress bar */}
      <View style={styles.progressBox}>
        <View style={styles.progressHeader}>
          <Text style={styles.progressLabel}>Progreso del plan</Text>
          <Text style={styles.progressPct}>{progress}%</Text>
        </View>
        <View style={styles.progressTrack}>
          <View style={[styles.progressFill, { width: `${progress}%` as any }]} />
        </View>
        <Text style={styles.progressSub}>{completedTasks} de {totalTasks} tareas completadas</Text>
      </View>

      {/* Timeline phases */}
      {PHASES.map((phase, pi) => (
        <View key={pi} style={styles.phase}>
          <View style={[styles.phaseHeader, { borderLeftColor: phase.color }]}>
            <Text style={styles.phaseEmoji}>{phase.emoji}</Text>
            <Text style={[styles.phaseTitle, { color: phase.color }]}>{phase.months}</Text>
          </View>
          {phase.tasks.map((task, ti) => {
            const key = `${pi}-${ti}`;
            const done = checked.has(key);
            return (
              <TouchableOpacity
                key={ti}
                style={styles.taskRow}
                onPress={() => toggle(key)}
                activeOpacity={0.7}
              >
                <View style={[styles.checkbox, done && { backgroundColor: phase.color, borderColor: phase.color }]}>
                  {done && <Text style={styles.checkmark}>✓</Text>}
                </View>
                <Text style={[styles.taskText, done && styles.taskDone]}>{task}</Text>
              </TouchableOpacity>
            );
          })}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f8fafc" },
  content: { padding: 16, paddingTop: 56, paddingBottom: 40 },
  header: { fontSize: 22, fontWeight: "800", color: "#0f172a", marginBottom: 16 },
  dateBox: { backgroundColor: '#ffffff', borderRadius: 14, padding: 14, marginBottom: 14, borderWidth: 1, borderColor: '#e2e8f0' },
  dateLabel: { fontSize: 11, fontWeight: '700', color: '#64748b', textTransform: 'uppercase', marginBottom: 6 },
  dateInput: { fontSize: 15, color: '#0f172a', fontWeight: '600' },
  progressBox: { backgroundColor: '#ffffff', borderRadius: 14, padding: 14, marginBottom: 20, borderWidth: 1, borderColor: '#e2e8f0' },
  progressHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  progressLabel: { fontSize: 13, fontWeight: '600', color: '#475569' },
  progressPct: { fontSize: 13, fontWeight: '800', color: '#2563eb' },
  progressTrack: { height: 8, backgroundColor: '#f1f5f9', borderRadius: 4, overflow: 'hidden', marginBottom: 6 },
  progressFill: { height: 8, backgroundColor: '#2563eb', borderRadius: 4 },
  progressSub: { fontSize: 11, color: '#94a3b8' },
  phase: { marginBottom: 20 },
  phaseHeader: { flexDirection: 'row', alignItems: 'center', borderLeftWidth: 3, paddingLeft: 10, marginBottom: 10 },
  phaseEmoji: { fontSize: 18, marginRight: 8 },
  phaseTitle: { fontSize: 14, fontWeight: '700' },
  taskRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 8, paddingLeft: 13, borderBottomWidth: 1, borderBottomColor: '#f1f5f9' },
  checkbox: { width: 20, height: 20, borderRadius: 6, borderWidth: 1.5, borderColor: '#cbd5e1', alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  checkmark: { fontSize: 11, color: '#ffffff', fontWeight: '800' },
  taskText: { fontSize: 13, color: '#374151', flex: 1, lineHeight: 18 },
  taskDone: { textDecorationLine: 'line-through', color: '#94a3b8' },
});
