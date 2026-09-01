import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import AppShell from '../components/AppShell';
import LoadingSpinner from '../components/LoadingSpinner';

const API = 'http://localhost:8000/api';
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

export default function RecruiterDashboard() {
  const [data, setData] = useState({ opportunities: [] });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API}/recruiter/dashboard`, { headers: getHeaders() })
      .then(r => r.ok ? r.json() : {})
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <AppShell><LoadingSpinner label="Loading recruiter dashboard…" /></AppShell>;

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16, marginBottom: 24 }}>
          <div>
            <div className="metric-label" style={{ marginBottom: 6 }}>RECRUITER PORTAL</div>
            <h1 style={{ margin: 0 }}>{data.company_name || 'Company'}</h1>
            <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: '4px 0 0 0' }}>Manage opportunities and review verified candidates.</p>
          </div>
          <button className="btn btn-cta" onClick={() => navigate('/recruiter/post-opportunity')}>
            + Post opportunity
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16, marginBottom: 30 }}>
          <StatCard label="TOTAL OPPORTUNITIES" value={data.total_opportunities ?? 0} />
          <StatCard label="ACTIVE POSTINGS" value={data.active_opportunities ?? 0} accent />
          <StatCard label="TOTAL APPLICANTS" value={data.total_applications ?? 0} />
        </div>

        <h2 style={{ marginBottom: 16, fontSize: 20 }}>My opportunities</h2>
        {(data.opportunities || []).length === 0 ? (
          <div className="blueprint-card" style={{ textAlign: 'center', padding: 40 }}>
            <p style={{ color: '#12202B', opacity: 0.6, margin: 0 }}>No opportunities posted yet.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 20 }}>
            {(data.opportunities || []).map(opp => (
              <div key={opp.id} className="blueprint-card">
                <div className="card-strip">OPPORTUNITY</div>
                <h3 style={{ margin: '0 0 6px 0', fontSize: 16 }}>{opp.title}</h3>
                <div style={{ display: 'flex', gap: 6, marginBottom: 16 }}>
                  <span className="pill pill-blue">{opp.status}</span>
                  <span className="pill pill-gold">{opp.applicant_count || 0} applicants</span>
                </div>
                <button className="btn btn-primary" onClick={() => navigate(`/recruiter/candidates/${opp.id}`)} style={{ width: '100%' }}>
                  View AI-ranked candidates →
                </button>
              </div>
            ))}
          </div>
        )}
      </motion.div>
    </AppShell>
  );
}

function StatCard({ label, value, accent }) {
  return (
    <div className="blueprint-card" style={{ padding: 18 }}>
      <div className="metric-label">{label}</div>
      <div className="metric-value" style={{ marginTop: 6, color: accent ? '#B8842E' : '#0E2A47' }}>{value}</div>
    </div>
  );
}
