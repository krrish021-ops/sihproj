import api from './api';

export const getStudentRecommendations = async (userId) => {
  try {
    const res = await api.get(`/api/student/recommendations/${userId}`);
    return res.data;
  } catch (e) {
    try {
      const res = await api.get(`/student/recommendations/${userId}`);
      return res.data;
    } catch (err) {
      return { internships: [], courses: [], jobs: [], ai_analysis: '' };
    }
  }
};
export const getRecommendations = getStudentRecommendations;
export const fetchRecommendations = getStudentRecommendations;

export const getStudentDashboard = async (userId) => {
  try {
    const res = await api.get(`/api/student/dashboard/${userId}`);
    return res.data;
  } catch (e) {
    try {
      const res = await api.get(`/student/dashboard/${userId}`);
      return res.data;
    } catch (err) {
      return {};
    }
  }
};
export const getDashboard = getStudentDashboard;
export const getStudentStats = getStudentDashboard;

export const getStudentProfile = async (userId) => {
  try {
    const res = await api.get(`/api/student/profile/${userId}`);
    return res.data;
  } catch (e) {
    try {
      const res = await api.get(`/student/profile/${userId}`);
      return res.data;
    } catch (err) {
      return {};
    }
  }
};
export const getProfile = getStudentProfile;

export const updateStudentProfile = async (userId, data) => {
  try {
    const res = await api.put(`/api/student/profile/${userId}`, data);
    return res.data;
  } catch (e) {
    const res = await api.put(`/student/profile/${userId}`, data);
    return res.data;
  }
};
export const updateProfile = updateStudentProfile;

export const addStudentSkill = async (userId, data) => {
  try {
    const res = await api.post(`/api/student/skills/${userId}`, data);
    return res.data;
  } catch (e) {
    const res = await api.post(`/student/skills/${userId}`, data);
    return res.data;
  }
};
export const addStudentSkills = addStudentSkill;
export const addSkills = addStudentSkill;
export const addSkill = addStudentSkill;
export const saveSkills = addStudentSkill;

export const applyToOpportunity = async (opportunityId, userId) => {
  try {
    const res = await api.post(`/api/student/apply/${opportunityId}/${userId}`);
    return res.data;
  } catch (e) {
    const res = await api.post(`/student/apply/${opportunityId}/${userId}`);
    return res.data;
  }
};
export const applyOpportunity = applyToOpportunity;
export const apply = applyToOpportunity;

export const syncLiveInternships = async (userId) => {
  try {
    const res = await api.post(`/api/student/sync-live/${userId}`);
    return res.data;
  } catch (e) {
    const res = await api.post(`/student/sync-live/${userId}`);
    return res.data;
  }
};
export const syncLive = syncLiveInternships;

const studentService = {
  getStudentRecommendations,
  getRecommendations,
  fetchRecommendations,
  getStudentDashboard,
  getDashboard,
  getStudentStats,
  getStudentProfile,
  getProfile,
  updateStudentProfile,
  updateProfile,
  addStudentSkill,
  addStudentSkills,
  addSkills,
  addSkill,
  saveSkills,
  applyToOpportunity,
  applyOpportunity,
  apply,
  syncLiveInternships,
  syncLive,
};

export default studentService;