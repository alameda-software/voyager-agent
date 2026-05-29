function getApiUrl(): string {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return "http://localhost:8000";
    } else if (hostname.includes("leafgate.es")) {
      return `${protocol}//api.leafgate.es`;
    } else {
      return `${protocol}//${hostname}:8000`;
    }
  }
  return "http://localhost:8000";
}

export const API_URL = getApiUrl();

export const config = {
  apiUrl: process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000",
  theme: {
    primary: "#6c63ff",
    background: "#0f0f23",
    surface: "#1a1a2e",
    text: "#ffffff",
    textSecondary: "#888888",
  },
};
