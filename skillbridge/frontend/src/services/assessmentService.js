import api from './api';

export const startAssessment = async (userId) => {
  const payload = { user_id: Number(userId), userId: Number(userId) };
  try {
    const res = await api.post('/api/assessment/start', payload);
    return res.data;
  } catch (e) {
    const res = await api.post('/assessment/start', payload);
    return res.data;
  }
};

export const submitAnswer = async (state, answer) => {
  const payload = { 
    state: state, 
    answer: String(answer).trim() 
  };
  try {
    const res = await api.post('/api/assessment/submit', payload);
    return res.data;
  } catch (e) {
    const res = await api.post('/assessment/submit', payload);
    return res.data;
  }
};

const assessmentService = { startAssessment, submitAnswer };
export default assessmentService;
