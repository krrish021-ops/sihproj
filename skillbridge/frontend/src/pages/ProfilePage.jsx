import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import AppShell from '../components/AppShell';
import LoadingSpinner from '../components/LoadingSpinner';

const API = 'http://localhost:8000/api';
function getUserId() { try { return JSON.parse(localStorage.getItem('user') || '{}').id || 1; } catch (e) { return 1; } }
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newSkill, setNewSkill] = useState('');
  const [rating, setRating] = useState(5);
  const userId = getUserId();

  const fetchProfile = () => {
    fetch(`${API}/student/profile/${userId}`, { headers: getHeaders() })
      .then(r => r.json())
      .then(setProfile)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchProfile(); }, []);

  const handleAddSkill = async (e) => {
    e.preventDefault();
    if (!newSkill.trim()) return;
    await fetch(`${API}/student/skills/${userId}`, {
      method: 'POST', headers: getHeaders(),
      body: JSON.stringify({ skill_name: newSkill.trim(), self_rating: Number(rating) }),
    });
    toast.success(`Added ${newSkill}`);
    setNewSkill('');
    fetchProfile();
  };

  if (loading) return <AppShell><LoadingSpinner label="Loading profile…" /></AppShell>;
  if (!profile) return <AppShell><div>Profile not found</div></AppShell>;

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ marginBottom: 24 }}>
          <div className="metric-label" style={{ marginBottom: 6 }}>YOUR IDENTITY</div>
          <h1 style={{ margin: 0 }}>My Profile</h1>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: 20 }}>
          <div className="blueprint-card">
            <div className="card-strip">PERSONAL DETAILS</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 12 }}>
              <Row label="Name" value={profile.user?.name} />
              <Row label="Email" value={profile.user?.email} />
              <Row label="College" value={profile.profile?.college} />
              <Row label="Department" value={profile.profile?.department} />
              <Row label="Year" value={profile.profile?.year_of_study || '—'} />
              <Row label="CGPA" value={profile.profile?.cgpa || '—'} />
            </div>
          </div>

          <div className="blueprint-card">
            <div className="card-strip">SKILL MAP</div>

            <form onSubmit={handleAddSkill} style={{ display: 'flex', gap: 8, marginTop: 14, marginBottom: 18 }}>
              <input type="text" className="input-field" placeholder="Add a skill" value={newSkill} onChange={e => setNewSkill(e.target.value)} style={{ flex: 1 }} />
              <select className="input-field" value={rating} onChange={e => setRating(e.target.value)} style={{ width: 90 }}>
                {[1,2,3,4,5,6,7,8,9,10].map(n => <option key={n} value={n}>{n}/10</option>)}
              </select>
              <button className="btn btn-cta" type="submit">Add</button>
            </form>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {(profile.skills || []).map(s => (
                <div key={s.id} style={{ background: '#FBF9F4', padding: 12, borderRadius: 8, border: '1px solid rgba(14,42,71,0.08)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, alignItems: 'center' }}>
                    <strong style={{ fontSize: 14 }}>{s.skill_name}</strong>
                    {s.is_verified ? (
                      <span className="pill pill-green">Verified · {s.verified_rating}/10</span>
                    ) : (
                      <span className="pill pill-gold">Self · {s.self_rating}/10</span>
                    )}
                  </div>
                  <div className="progress-track" style={{ height: 6 }}>
                    <div className={`progress-fill ${s.is_verified ? 'green' : 'gold'}`} style={{ width: `${(s.is_verified ? s.verified_rating : s.self_rating) * 10}%` }} />
                  </div>
                </div>
              ))}
              {(profile.skills || []).length === 0 && (
                <p style={{ color: '#12202B', opacity: 0.6, fontSize: 13 }}>No skills added yet.</p>
              )}
            </div>
          </div>
        </div>
      </motion.div>
    </AppShell>
  );
}

function Row({ label, value }) {
  return (
    <div>
      <div className="metric-label" style={{ marginBottom: 2 }}>{label}</div>
      <div style={{ fontSize: 14, color: '#0E2A47', fontWeight: 500 }}>{value || '—'}</div>
    </div>
  );
}
