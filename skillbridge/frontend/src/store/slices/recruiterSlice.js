// Recruiter Slice
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  opportunities: [],
  candidates: [],
  loading: false,
  error: null,
};

const recruiterSlice = createSlice({
  name: 'recruiter',
  initialState,
  reducers: {
    setOpportunities: (state, action) => {
      state.opportunities = action.payload;
    },
    setCandidates: (state, action) => {
      state.candidates = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
  },
});

export const { setOpportunities, setCandidates, setLoading } = recruiterSlice.actions;
export default recruiterSlice.reducer;