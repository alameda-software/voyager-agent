/**
 * Auth store — JWT + user profile persisted in localStorage
 */

export interface UserProfile {
  id: number;
  email: string;
  display_name: string | null;
  role: 'superadmin' | 'vendor' | 'user';
  partner_name: string | null;
  wedding_date: string | null;
  city: string | null;
  budget: number | null;
}

const TOKEN_KEY = 'livegate_token';
const USER_KEY = 'livegate_user';

function storage() {
  return typeof window !== 'undefined' ? localStorage : null;
}

export function getToken(): string | null {
  return storage()?.getItem(TOKEN_KEY) ?? null;
}

export function getUser(): UserProfile | null {
  try {
    const raw = storage()?.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function saveAuth(token: string, user: UserProfile) {
  storage()?.setItem(TOKEN_KEY, token);
  storage()?.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  storage()?.removeItem(TOKEN_KEY);
  storage()?.removeItem(USER_KEY);
}

export function isLoggedIn(): boolean {
  return !!getToken();
}

export function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
