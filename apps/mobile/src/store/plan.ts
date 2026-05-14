/**
 * Trip Plan Store - persists selected items from chat to a trip plan.
 * Uses simple in-memory state + localStorage for web persistence.
 */

export type PlanItemType = 'flight' | 'hotel' | 'car' | 'vendor' | 'tour';

export interface PlanItem {
  id: string;
  type: PlanItemType;
  data: any;
  preferred: boolean;
  addedAt: string;
  conversationId?: number;
}

export interface TripPlan {
  id: string;
  title: string;
  domain: 'voyager' | 'wedding';
  items: PlanItem[];
  createdAt: string;
  updatedAt: string;
}

const STORAGE_KEY = 'voyager_trip_plans';

function loadPlans(): TripPlan[] {
  try {
    const raw = typeof window !== 'undefined' ? localStorage.getItem(STORAGE_KEY) : null;
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function savePlans(plans: TripPlan[]) {
  try {
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(plans));
    }
  } catch {}
}

export function getPlans(): TripPlan[] {
  return loadPlans();
}

export function getPlanByConversation(conversationId: number): TripPlan | null {
  const plans = loadPlans();
  return plans.find(p => p.items.some(i => i.conversationId === conversationId)) || null;
}

export function getOrCreatePlan(conversationId: number, title: string, domain: 'voyager' | 'wedding'): TripPlan {
  const plans = loadPlans();
  let plan = plans.find(p => p.id === `conv-${conversationId}`);
  if (!plan) {
    plan = {
      id: `conv-${conversationId}`,
      title,
      domain,
      items: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    plans.push(plan);
    savePlans(plans);
  }
  return plan;
}

export function addItemToPlan(conversationId: number, title: string, domain: 'voyager' | 'wedding', item: Omit<PlanItem, 'id' | 'addedAt' | 'preferred'>): TripPlan {
  const plans = loadPlans();
  let plan = plans.find(p => p.id === `conv-${conversationId}`);
  if (!plan) {
    plan = {
      id: `conv-${conversationId}`,
      title,
      domain,
      items: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    plans.push(plan);
  }

  const newItem: PlanItem = {
    ...item,
    id: `${item.type}-${Date.now()}`,
    preferred: plan.items.filter(i => i.type === item.type).length === 0, // First of type = preferred
    addedAt: new Date().toISOString(),
    conversationId,
  };

  plan.items.push(newItem);
  plan.updatedAt = new Date().toISOString();
  savePlans(plans);
  return plan;
}

export function setPreferred(planId: string, itemId: string): void {
  const plans = loadPlans();
  const plan = plans.find(p => p.id === planId);
  if (!plan) return;
  const type = plan.items.find(i => i.id === itemId)?.type;
  plan.items = plan.items.map(i => ({
    ...i,
    preferred: i.type === type ? i.id === itemId : i.preferred,
  }));
  plan.updatedAt = new Date().toISOString();
  savePlans(plans);
}

export function removeItem(planId: string, itemId: string): void {
  const plans = loadPlans();
  const plan = plans.find(p => p.id === planId);
  if (!plan) return;
  plan.items = plan.items.filter(i => i.id !== itemId);
  plan.updatedAt = new Date().toISOString();
  savePlans(plans);
}

export function getPlanSummary(plan: TripPlan) {
  const flights = plan.items.filter(i => i.type === 'flight');
  const hotels = plan.items.filter(i => i.type === 'hotel');
  const cars = plan.items.filter(i => i.type === 'car');
  const vendors = plan.items.filter(i => i.type === 'vendor');
  const preferredFlight = flights.find(i => i.preferred);
  const totalEstimate = [
    preferredFlight?.data?.price_per_person || 0,
    hotels.find(i => i.preferred)?.data?.price_per_night || 0,
    cars.find(i => i.preferred)?.data?.price_per_day || 0,
  ].reduce((a, b) => a + b, 0);
  return { flights, hotels, cars, vendors, preferredFlight, totalEstimate };
}
