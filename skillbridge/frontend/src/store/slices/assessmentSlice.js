// Assessment Slice
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  currentQuestion: null,
  assessmentState: null,
  skillReport: null,
  loading: false,
  complete: false,
};

const assessmentSlice = createSlice({
  name: 'assessment',
  initialState,
  reducers: {
    setCurrentQuestion: (state, action) => {
      state.currentQuestion = action.payload;
    },
    setAssessmentState: (state, action) => {
      state.assessmentState = action.payload;
    },
    setSkillReport: (state, action) => {
      state.skillReport = action.payload;
    },
    setComplete: (state, action) => {
      state.complete = action.payload;
    },
  },
});

export const { setCurrentQuestion, setAssessmentState, setSkillReport, setComplete } = assessmentSlice.actions;
export default assessmentSlice.reducer;