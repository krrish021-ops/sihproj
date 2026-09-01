import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import StudentDashboard from './pages/StudentDashboard';
import RecruiterDashboard from './pages/RecruiterDashboard';
import AcademicianDashboard from './pages/AcademicianDashboard';
import AssessmentPage from './pages/AssessmentPage';
import ProfilePage from './pages/ProfilePage';
import RecommendationsPage from './pages/RecommendationsPage';
import PostOpportunityPage from './pages/PostOpportunityPage';
import CandidateRecommendationsPage from './pages/CandidateRecommendationsPage';
import ProtectedRoute from './components/auth/ProtectedRoute';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        <Route path="/student/dashboard" element={<ProtectedRoute role="student"><StudentDashboard /></ProtectedRoute>} />
        <Route path="/student/assessment" element={<ProtectedRoute role="student"><AssessmentPage /></ProtectedRoute>} />
        <Route path="/student/profile" element={<ProtectedRoute role="student"><ProfilePage /></ProtectedRoute>} />
        <Route path="/student/recommendations" element={<ProtectedRoute role="student"><RecommendationsPage /></ProtectedRoute>} />

        <Route path="/recruiter/dashboard" element={<ProtectedRoute role="recruiter"><RecruiterDashboard /></ProtectedRoute>} />
        <Route path="/recruiter/post-opportunity" element={<ProtectedRoute role="recruiter"><PostOpportunityPage /></ProtectedRoute>} />
        <Route path="/recruiter/candidates/:id" element={<ProtectedRoute role="recruiter"><CandidateRecommendationsPage /></ProtectedRoute>} />

        <Route path="/academician/dashboard" element={<ProtectedRoute role="academician"><AcademicianDashboard /></ProtectedRoute>} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
