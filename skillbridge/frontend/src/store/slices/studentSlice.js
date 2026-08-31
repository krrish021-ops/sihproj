// Student Slice
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  profile: null,
  skills: [],
  recommendations: null,
  loading: false,
  error: null,
};

const studentSlice = createSlice({
  name: 'student',
  initialState,
  reducers: {
    setProfile: (state, action) => {
      state.profile = action.payload;
    },
    setSkills: (state, action) => {
      state.skills = action.payload;
    },
    setRecommendations: (state, action) => {
      state.recommendations = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
  },
});

export const { setProfile, setSkills, setRecommendations, setLoading } = studentSlice.actions;
export default studentSlice.reducer;