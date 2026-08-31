// Store
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import studentReducer from './slices/studentSlice';
import recruiterReducer from './slices/recruiterSlice';
import assessmentReducer from './slices/assessmentSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    student: studentReducer,
    recruiter: recruiterReducer,
    assessment: assessmentReducer,
  },
});