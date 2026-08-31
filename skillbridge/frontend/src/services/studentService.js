// Student Service
import api from './api';

export const getStudentDashboard = async (userId) => {
  const response = await api.get(`/student/dashboard/${userId}`);
  return response.data;
};

export const getStudentProfile = async (userId) => {
  const response = await api.get(`/student/profile/${userId}`);
  return response.data;
};

export const updateStudentProfile = async (userId, profileData) => {
  const response = await api.put(`/student/profile/${userId}`, profileData);
  return response.data;
};

export const addSkills = async (userId, skillsData) => {
  const response = await api.post(`/student/skills/${userId}`, skillsData);
  return response.data;
};

export const getRecommendations = async (userId) => {
  const response = await api.get(`/student/recommendations/${userId}`);
  return response.data;
};

export const applyToOpportunity = async (opportunityId, userId) => {
  const response = await api.post(`/student/apply/${opportunityId}/${userId}`);
  return response.data;
};