// Assessment Service
import api from './api';

export const startAssessment = async (userId) => {
  const response = await api.post('/assessment/start', { user_id: userId });
  return response.data;
};

export const submitAnswer = async (data) => {
  const response = await api.post('/assessment/submit', data);
  return response.data;
};