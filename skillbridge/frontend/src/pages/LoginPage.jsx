import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const API = 'http://localhost:8000/api';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('student');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim(), password }),
      });
      const data = await res.json();
      if (!res.ok) {
        toast.error(data.detail || 'Login failed');
        return;
      }
      localStorage.setItem('token', data.access_token || data.token || '');
      localStorage.setItem('access_token', data.access_token || data.token || '');
      localStorage.setItem('user', JSON.stringify(data.user || { id: 1, role }));
      toast.success(`Welcome back, ${data.user?.name || 'User'}`);

      const userRole = data.user?.role || role;
      if (userRole === 'recruiter') navigate('/recruiter/dashboard');
      else if (userRole === 'academician') navigate('/academician/dashboard');
      else navigate('/student/dashboard');
    } catch (err) {
      toast.error('Cannot connect to backend on :8000');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="blueprint-surface" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20 }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="blueprint-card" style={{ width: '100%', maxWidth: 440, padding: 36 }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'none', marginBottom: 24 }}>
          <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#D9A441' }} />
          <span style={{ fontFamily: '"Space Grotesk", sans-serif', fontWeight: 700, fontSize: 18, color: '#0E2A47' }}>SkillBridge</span>
        </Link>

        <h2 style={{ margin: '0 0 6px 0' }}>Welcome back</h2>
        <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: '0 0 24px 0' }}>Sign in to access your dashboard</p>

        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div>
            <label className="input-label">Role</label>
            <select className="input-field" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="student">Student</option>
              <option value="recruiter">Recruiter</option>
              <option value="academician">Academician</option>
            </select>
          </div>

          <div>
            <label className="input-label">Email address</label>
            <input required type="email" className="input-field" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
          </div>

          <div>
            <label className="input-label">Password</label>
            <input required type="password" className="input-field" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading} style={{ padding: 12, fontSize: 15, marginTop: 8 }}>
            {loading ? 'Signing in…' : 'Log in →'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: 20, fontSize: 13, color: '#12202B', opacity: 0.7 }}>
          Don't have an account? <Link to="/signup" style={{ color: '#B8842E', fontWeight: 600, textDecoration: 'none' }}>Sign up</Link>
        </p>
      </motion.div>
    </div>
  );
}
