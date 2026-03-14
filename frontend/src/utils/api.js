import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL; // Uses Vite proxy in development

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: (data) => api.post("/auth/login", data),
  register: (data) => api.post("/auth/register", data),
  me: () => api.get("/auth/me"),
  logout: () => api.post("/auth/logout"),
};

export const urlApi = {
  list: () => api.get("/urls/"),
  create: (data) => api.post("/urls/", data),
  get: (code) => api.get(`/urls/${code}`),
  update: (code, data) => api.put(`/urls/${code}`, data),
  delete: (code) => api.delete(`/urls/${code}`),
};

export const analyticsApi = {
  top: (limit = 10) => api.get(`/analytics/top?limit=${limit}`),
  getClickCount: (id) => api.get(`/analytics/${id}`),
  getCountries: (id) => api.get(`/analytics/${id}/countries`),
  getDevices: (code) => api.get(`/analytics/${code}/devices`),
  getTimeline: (code) => api.get(`/analytics/${code}/timeline`),
};

export default api;
