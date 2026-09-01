import axios from 'axios';

const API_BASE = 'http://localhost:8000/api'\;

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ─── AUTH ───
export const login = (data) => api.post('/auth/login', data);
export const register = (data) => api.post('/auth/register', data);

// ─── STUDENT: 3 SECTIONS ───

// SECTION 1: All Internships
export const getAllInternships = () => api.get('/student/internships');

// SECTION 2: Recommendations (based on assessment)
export const getRecommendations = (userId) => api.get(`/student/recommendations/${userId}`);

// SECTION 3: Gap Courses (YouTube)
export const getGapCourses = (userId) => api.get(`/student/gap-courses/${userId}`);

// Profile
export const getProfile = (userId) => api.get(`/student/profile/${userId}`);
export const updateProfile = (userId, data) => api.put(`/student/profile/${userId}`, data);
export const addSkill = (userId, data) => api.post(`/student/skills/${userId}`, data);
export const getDashboard = (userId) => api.get(`/student/dashboard/${userId}`);

// Apply
export const applyToInternship = (oppId, userId, data) => api.post(`/student/apply/${oppId}/${userId}`, data);

// Assessment
export const startAssessment = (data) => api.post('/assessment/start', data);
export const submitAssessment = (data) => api.post('/assessment/submit', data);

export default api;
