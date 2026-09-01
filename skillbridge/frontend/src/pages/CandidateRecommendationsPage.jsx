import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import AppShell from '../components/AppShell';
import LoadingSpinner from '../components/LoadingSpinner';

const API = 'http://localhost:8000/api';
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

export default function CandidateRecommendationsPage() {
  const { id } = useParams();
  const [data, setData] = useState({ ranked_candidates: [] });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API}/recruiter/opportunities/${id}/candidates`, { headers: getHeaders() })
      .then(r => r.ok ? r.json() : {})
      .then(setData)
      .finally(() => setLoading(false));
  }, [id]);

  const updateStatus = async (appId, status) => {
    await fetch(`${API}/recruiter/applications/${appId}/status`, {
      method: 'PUT', headers: getHeaders(),
      body: JSON.stringify({ status }),
    });
    toast.success(`Marked as ${status}`);
  };

  if (loading) return <AppShell><LoadingSpinner label="Ranking candidates…" /></AppShell>;

  const candidates = data.ranked_candidates || [];

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <button onClick={() => navigate('/recruiter/dashboard')} className="btn btn-ghost" style={{ marginBottom: 12, padding: '6px 10px' }}>← Back</button>

        <div style={{ marginBottom: 24 }}>
          <div className="metric-label" style={{ marginBottom: 6 }}>AI RANKING</div>
          <h1 style={{ margin: 0 }}>{data.opportunity_title || 'Candidates'}</h1>
          <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: '4px 0 0 0' }}>
            Ranked by verified skill assessment scores (+25% weight for verified proficiency).
          </p>
        </div>

        {candidates.length === 0 ? (
          <div className="blueprint-card" style={{ textAlign: 'center', padding: 40 }}>
            <p style={{ color: '#12202B', opacity: 0.6, margin: 0 }}>No applicants yet.</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {candidates.map((c, i) => (
              <CandidateCard key={i} c={c} updateStatus={updateStatus} />
            ))}
          </div>
        )}
      </motion.div>
    </AppShell>
  );
}

function CandidateCard({ c, updateStatus }) {
  const initial = (c.student_name || '?')[0].toUpperCase();
  return (
    <div className="blueprint-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
        <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
          <div style={{ width: 56, height: 56, borderRadius: '50%', background: '#0E2A47', color: '#D9A441', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 22, fontFamily: '"Space Grotesk", sans-serif' }}>
            {initial}
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
              <span className="pill pill-navy">#{c.rank || 1}</span>
              <h3 style={{ margin: 0, fontSize: 17 }}>{c.student_name}</h3>
              <span className="pill pill-green">{c.recommendation || 'Recommended'}</span>
            </div>
            <p style={{ color: '#2F5C86', fontSize: 12, margin: 0 }}>
              {c.college} · CGPA {c.cgpa} · {c.assessments_completed || c.assessments_taken || 0} tests taken
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 20, alignItems: 'center' }}>
          <div style={{ textAlign: 'right' }}>
            <div className="metric-label">MATCH SCORE</div>
            <div className="metric-value" style={{ color: '#3D8361', fontSize: 24, marginTop: 2 }}>{c.match_score || c.total_score}%</div>
          </div>
          <div style={{ display: 'flex', gap: 6 }}>
            <button onClick={() => updateStatus(c.application_id, 'shortlisted')} className="btn btn-primary" style={{ fontSize: 12, padding: '6px 12px' }}>Shortlist</button>
            <button onClick={() => updateStatus(c.application_id, 'offered')} className="btn btn-cta" style={{ fontSize: 12, padding: '6px 12px' }}>Offer</button>
            <button onClick={() => updateStatus(c.application_id, 'rejected')} className="btn btn-danger" style={{ fontSize: 12, padding: '6px 12px' }}>Reject</button>
          </div>
        </div>
      </div>
    </div>
  );
}
