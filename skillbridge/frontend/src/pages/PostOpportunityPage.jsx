import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import AppShell from '../components/AppShell';

const API = 'http://localhost:8000/api';
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

export default function PostOpportunityPage() {
  const [form, setForm] = useState({
    title: '', company_name: '', location: 'Remote', opportunity_type: 'internship',
    stipend: 20000, duration: '3 months', required_skills: '', description: '',
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const update = (k, v) => setForm(prev => ({ ...prev, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API}/recruiter/opportunities`, {
        method: 'POST', headers: getHeaders(),
        body: JSON.stringify({ ...form, stipend: Number(form.stipend) }),
      });
      if (res.ok) {
        toast.success('Opportunity posted!');
        navigate('/recruiter/dashboard');
      } else {
        toast.error('Failed to post');
      }
    } catch (e) { toast.error('Connection error'); }
    finally { setLoading(false); }
  };

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} style={{ maxWidth: 640, margin: '0 auto' }}>
        <div style={{ marginBottom: 20 }}>
          <div className="metric-label" style={{ marginBottom: 6 }}>NEW LISTING</div>
          <h1 style={{ margin: 0 }}>Post opportunity</h1>
        </div>

        <form onSubmit={handleSubmit} className="blueprint-card" style={{ padding: 32 }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div>
              <label className="input-label">Role title</label>
              <input required className="input-field" value={form.title} onChange={e => update('title', e.target.value)} placeholder="e.g. Python Backend Intern" />
            </div>
            <div>
              <label className="input-label">Company name</label>
              <input required className="input-field" value={form.company_name} onChange={e => update('company_name', e.target.value)} placeholder="e.g. TechCorp India" />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div>
                <label className="input-label">Location</label>
                <input className="input-field" value={form.location} onChange={e => update('location', e.target.value)} />
              </div>
              <div>
                <label className="input-label">Type</label>
                <select className="input-field" value={form.opportunity_type} onChange={e => update('opportunity_type', e.target.value)}>
                  <option value="internship">Internship</option>
                  <option value="placement">Placement (Full-Time)</option>
                </select>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div>
                <label className="input-label">Stipend (₹/mo)</label>
                <input type="number" className="input-field" value={form.stipend} onChange={e => update('stipend', e.target.value)} />
              </div>
              <div>
                <label className="input-label">Duration</label>
                <input className="input-field" value={form.duration} onChange={e => update('duration', e.target.value)} />
              </div>
            </div>
            <div>
              <label className="input-label">Required skills (comma-separated)</label>
              <input required className="input-field" value={form.required_skills} onChange={e => update('required_skills', e.target.value)} placeholder="Python, FastAPI, SQL, Docker" />
            </div>
            <div>
              <label className="input-label">Description</label>
              <textarea rows={4} className="input-field" value={form.description} onChange={e => update('description', e.target.value)} placeholder="Role responsibilities and requirements…" />
            </div>
            <button type="submit" disabled={loading} className="btn btn-cta" style={{ padding: 12, fontSize: 15 }}>
              {loading ? 'Publishing…' : 'Post opportunity →'}
            </button>
          </div>
        </form>
      </motion.div>
    </AppShell>
  );
}
