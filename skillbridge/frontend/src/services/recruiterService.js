// Recruiter Service
import api from './api';

export const getRecruiterDashboard = async (userId) => {
  const response = await api.get(`/recruiter/dashboard/${userId}`);
  return response.data;
};

export const postOpportunity = async (userId, opportunityData) => {
  const response = await api.post(`/recruiter/opportunity/${userId}`, opportunityData);
  return response.data;
};

export const getCandidateRecommendations = async (opportunityId) => {
  const response = await api.get(`/recruiter/candidates/${opportunityId}`);
  return response.data;
};

export const updateApplicationStatus = async (applicationId, status) => {
  const response = await api.put(`/recruiter/application/${applicationId}/status`, { status });
  return response.data;
};