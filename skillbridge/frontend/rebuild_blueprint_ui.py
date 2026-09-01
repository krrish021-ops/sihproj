import os

files = {}

# ─── 1. tailwind.config.js ───────────────────────────────────────────────────
files["tailwind.config.js"] = """/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#0E2A47',
          mid: '#163A5F',
          line: '#2F5C86',
          50: '#EEF3F9',
          100: '#D6E1EE',
        },
        gold: {
          DEFAULT: '#D9A441',
          dark: '#B8842E',
          light: '#F1DBA3',
        },
        paper: '#FBF9F4',
        ink: '#12202B',
        success: '#3D8361',
        danger: '#C1443C',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
};
"""

# ─── 2. src/index.css ────────────────────────────────────────────────────────
files["src/index.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --navy: #0E2A47;
  --navy-mid: #163A5F;
  --navy-line: #2F5C86;
  --gold: #D9A441;
  --gold-dark: #B8842E;
  --paper: #FBF9F4;
  --ink: #12202B;
}

* { box-sizing: border-box; }

html, body, #root {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
  background: var(--paper);
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
}

/* BLUEPRINT SURFACE (Navy backdrop with subtle gold drafting grid) */
.blueprint-surface {
  background:
    linear-gradient(rgba(14, 42, 71, 0.95), rgba(14, 42, 71, 0.95)),
    repeating-linear-gradient(0deg, transparent 0 39px, rgba(217, 164, 65, 0.08) 39px 40px),
    repeating-linear-gradient(90deg, transparent 0 39px, rgba(217, 164, 65, 0.08) 39px 40px),
    var(--navy);
  color: #F1F5F9;
}

/* BLUEPRINT CARD (White card with gold drafting corner brackets) */
.blueprint-card {
  position: relative;
  background: #ffffff;
  border: 1px solid rgba(14, 42, 71, 0.12);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(14, 42, 71, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.blueprint-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(14, 42, 71, 0.08);
}

.blueprint-card::before,
.blueprint-card::after {
  content: '';
  position: absolute;
  width: 14px;
  height: 14px;
  border: 2px solid var(--gold);
}
.blueprint-card::before {
  top: -1px;
  left: -1px;
  border-right: none;
  border-bottom: none;
}
.blueprint-card::after {
  bottom: -1px;
  right: -1px;
  border-left: none;
  border-top: none;
}

/* CARD STRIP */
.card-strip {
  display: inline-block;
  background: var(--navy);
  color: var(--gold);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  letter-spacing: 2px;
  padding: 3px 10px;
  text-transform: uppercase;
  margin-bottom: 12px;
  font-weight: 600;
}

/* METRIC LABEL */
.metric-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--navy-line);
  font-weight: 600;
}

.metric-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--navy);
  line-height: 1;
}

/* BUTTON SYSTEM */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
  text-decoration: none;
}

.btn-primary { background: var(--navy); color: #ffffff; }
.btn-primary:hover { background: var(--navy-mid); }

.btn-secondary {
  background: transparent;
  color: var(--navy);
  border: 1.5px solid var(--navy);
}
.btn-secondary:hover { background: var(--navy); color: #ffffff; }

.btn-cta { background: var(--gold); color: var(--navy); font-weight: 700; }
.btn-cta:hover { background: var(--gold-dark); color: #ffffff; }

.btn-danger { background: #C1443C; color: #ffffff; }
.btn-danger:hover { background: #A0332C; }

.btn-ghost { background: transparent; color: var(--navy); }
.btn-ghost:hover { background: rgba(14, 42, 71, 0.06); }

/* PILLS */
.pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.3px;
}
.pill-blue { background: #EEF3F9; color: #163A5F; border: 1px solid #D6E1EE; }
.pill-gold { background: #FDF3DC; color: #B8842E; border: 1px solid #F1DBA3; }
.pill-green { background: #E4F0EA; color: #3D8361; border: 1px solid #C1DDC9; }
.pill-red { background: #F9E4E2; color: #C1443C; border: 1px solid #EDC7C4; }
.pill-navy { background: var(--navy); color: var(--gold); }

/* PROGRESS BAR */
.progress-track {
  background: rgba(14, 42, 71, 0.08);
  border-radius: 999px;
  height: 8px;
  overflow: hidden;
  width: 100%;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--navy) 0%, var(--gold) 100%);
  border-radius: 999px;
  transition: width 0.4s ease;
}
.progress-fill.green { background: linear-gradient(90deg, #3D8361 0%, #6DBC90 100%); }
.progress-fill.red { background: linear-gradient(90deg, #C1443C 0%, #E88A83 100%); }
.progress-fill.gold { background: linear-gradient(90deg, #B8842E 0%, #F1DBA3 100%); }

/* INPUTS */
.input-field {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid rgba(14, 42, 71, 0.15);
  border-radius: 8px;
  background: #ffffff;
  color: var(--ink);
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  transition: border 0.15s ease;
}
.input-field:focus {
  outline: none;
  border-color: var(--gold);
  box-shadow: 0 0 0 3px rgba(217, 164, 65, 0.15);
}

.input-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--navy);
  margin-bottom: 6px;
}

*:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }

h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif; color: var(--navy); font-weight: 700; }
"""

# ─── 3. src/components/Navbar.jsx ────────────────────────────────────────────
files["src/components/Navbar.jsx"] = """import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem('user') || 'null');
  } catch (e) {}

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const isLanding = location.pathname === '/';

  return (
    <nav
      style={{
        background: isLanding ? 'transparent' : '#0E2A47',
        borderBottom: isLanding ? 'none' : '1px solid rgba(217,164,65,0.2)',
        padding: '14px 32px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
        <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#D9A441' }} />
        <span style={{ fontFamily: '"Space Grotesk", sans-serif', fontWeight: 700, fontSize: '18px', color: '#F1F5F9' }}>
          SkillBridge
        </span>
      </Link>

      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        {user && user.name ? (
          <>
            <span style={{ color: '#F1DBA3', fontSize: '13px', fontFamily: '"IBM Plex Mono", monospace' }}>
              {user.name.toUpperCase()}
            </span>
            <button onClick={handleLogout} className="btn btn-secondary" style={{ background: 'transparent', color: '#F1F5F9', borderColor: 'rgba(255,255,255,0.35)', fontSize: '13px', padding: '7px 14px' }}>
              Log out
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: '#F1F5F9', fontSize: '14px', textDecoration: 'none', fontWeight: 500 }}>
              Log in
            </Link>
            <Link to="/signup" className="btn btn-cta" style={{ padding: '8px 18px', fontSize: '14px' }}>
              Get started
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
"""

# ─── 4. src/components/Sidebar.jsx ───────────────────────────────────────────
files["src/components/Sidebar.jsx"] = """import React from 'react';
import { NavLink } from 'react-router-dom';

const linksByRole = {
  student: [
    { to: '/student/dashboard', label: 'Dashboard' },
    { to: '/student/assessment', label: 'Assessment' },
    { to: '/student/profile', label: 'Profile' },
    { to: '/student/recommendations', label: 'Recommendations' },
  ],
  recruiter: [
    { to: '/recruiter/dashboard', label: 'Dashboard' },
    { to: '/recruiter/post-opportunity', label: 'Post opportunity' },
  ],
  academician: [
    { to: '/academician/dashboard', label: 'Analytics' },
  ],
};

export default function Sidebar() {
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem('user') || 'null');
  } catch (e) {}
  const role = user?.role || 'student';
  const links = linksByRole[role] || linksByRole.student;

  return (
    <aside
      style={{
        width: 224,
        minHeight: 'calc(100vh - 60px)',
        background: '#ffffff',
        borderRight: '1px solid rgba(14, 42, 71, 0.08)',
        padding: '28px 0',
      }}
    >
      <div className="metric-label" style={{ padding: '0 28px 12px', color: '#2F5C86' }}>MENU</div>
      <nav>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              padding: '10px 28px',
              fontSize: '14px',
              color: isActive ? '#0E2A47' : '#12202B',
              background: isActive ? '#EEF3F9' : 'transparent',
              borderLeft: isActive ? '3px solid #D9A441' : '3px solid transparent',
              fontWeight: isActive ? 600 : 400,
              textDecoration: 'none',
              transition: 'all 0.15s ease',
            })}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
"""

# ─── 5. src/components/AppShell.jsx ──────────────────────────────────────────
files["src/components/AppShell.jsx"] = """import React from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

export default function AppShell({ children }) {
  return (
    <div style={{ minHeight: '100vh', background: '#FBF9F4' }}>
      <Navbar />
      <div style={{ display: 'flex' }}>
        <Sidebar />
        <main style={{ flex: 1, padding: '32px 40px', minHeight: 'calc(100vh - 60px)' }}>
          {children}
        </main>
      </div>
    </div>
  );
}
"""

# ─── 6. src/components/LoadingSpinner.jsx ────────────────────────────────────
files["src/components/LoadingSpinner.jsx"] = """import React from 'react';

export default function LoadingSpinner({ label = 'Loading…' }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 20px' }}>
      <div
        style={{
          width: 40,
          height: 40,
          border: '3px solid rgba(14,42,71,0.15)',
          borderTop: '3px solid #0E2A47',
          borderRadius: '50%',
          animation: 'spin 0.9s linear infinite',
        }}
      />
      <div className="metric-label" style={{ marginTop: 14 }}>{label}</div>
      <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
"""

# ─── 7. src/components/auth/ProtectedRoute.jsx ───────────────────────────────
files["src/components/auth/ProtectedRoute.jsx"] = """import React from 'react';
import { Navigate } from 'react-router-dom';

export default function ProtectedRoute({ children, role }) {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem('user') || 'null');
  } catch (e) {}

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  if (role && user.role !== role) {
    if (user.role === 'recruiter') return <Navigate to="/recruiter/dashboard" replace />;
    if (user.role === 'academician') return <Navigate to="/academician/dashboard" replace />;
    return <Navigate to="/student/dashboard" replace />;
  }

  return children;
}
"""

# ─── 8. src/pages/LandingPage.jsx ────────────────────────────────────────────
files["src/pages/LandingPage.jsx"] = """import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function LandingPage() {
  const navigate = useNavigate();

  const features = [
    { title: 'AI Assessment', desc: 'Adaptive scenario-based tests that verify what you actually know — no more resume inflation.', label: '01 · VERIFY' },
    { title: 'Skill Mapping', desc: 'Visual proficiency map with verified scores, benchmarked against real industry demand.', label: '02 · MAP' },
    { title: 'Career Matching', desc: 'AI ranks internships & placements by your verified skills — with targeted bridge courses for gaps.', label: '03 · MATCH' },
  ];

  return (
    <div className="blueprint-surface" style={{ minHeight: '100vh' }}>
      <Navbar />

      <section style={{ maxWidth: 1200, margin: '0 auto', padding: '100px 40px 80px', textAlign: 'center' }}>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.1 }}>
          <div className="metric-label" style={{ color: '#F1DBA3', marginBottom: 20 }}>
            SIH 2024 · MINISTRY OF AYUSH · AICTE
          </div>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          style={{
            fontSize: 'clamp(38px, 6vw, 64px)',
            fontWeight: 700,
            color: '#ffffff',
            letterSpacing: '-1.5px',
            lineHeight: 1.05,
            margin: '0 0 24px 0',
          }}
        >
          Prove your skills.<br />
          <span style={{ color: '#D9A441' }}>Not just your resume.</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          style={{ fontSize: 18, color: 'rgba(255,255,255,0.75)', maxWidth: 640, margin: '0 auto 40px', lineHeight: 1.6 }}
        >
          An academia-industry collaboration platform for students, recruiters, and academicians.
          Verify skills through adaptive AI assessments and unlock personalized career opportunities.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.55 }}
          style={{ display: 'flex', gap: 14, justifyContent: 'center', flexWrap: 'wrap' }}
        >
          <button onClick={() => navigate('/signup')} className="btn btn-cta" style={{ padding: '14px 28px', fontSize: 15 }}>
            Start your assessment →
          </button>
          <button onClick={() => navigate('/login')} className="btn btn-secondary" style={{ padding: '14px 28px', fontSize: 15, color: '#F1F5F9', borderColor: 'rgba(255,255,255,0.4)' }}>
            I already have an account
          </button>
        </motion.div>
      </section>

      <section style={{ maxWidth: 1200, margin: '0 auto', padding: '40px 40px 100px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 24 }}>
          {features.map((f, i) => (
            <motion.div key={i} initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.7 + i * 0.1 }} className="blueprint-card">
              <div className="card-strip">{f.label}</div>
              <h3 style={{ margin: '0 0 10px 0' }}>{f.title}</h3>
              <p style={{ color: '#12202B', opacity: 0.75, fontSize: 14, lineHeight: 1.6, margin: 0 }}>{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
"""

# ─── 9. src/pages/LoginPage.jsx ──────────────────────────────────────────────
files["src/pages/LoginPage.jsx"] = """import React, { useState } from 'react';
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
"""

# ─── 10. src/pages/SignupPage.jsx ────────────────────────────────────────────
files["src/pages/SignupPage.jsx"] = """import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const API = 'http://localhost:8000/api';

export default function SignupPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('student');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name.trim(), email: email.trim().toLowerCase(), password, role }),
      });
      const data = await res.json();
      if (!res.ok) {
        toast.error(data.detail || 'Signup failed');
        return;
      }
      localStorage.setItem('token', data.access_token || data.token || '');
      localStorage.setItem('access_token', data.access_token || data.token || '');
      localStorage.setItem('user', JSON.stringify(data.user || { id: 1, role }));
      toast.success('Account created!');
      navigate('/login');
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

        <h2 style={{ margin: '0 0 6px 0' }}>Create account</h2>
        <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: '0 0 24px 0' }}>Join the verified skills ecosystem</p>

        <form onSubmit={handleSignup} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div>
            <label className="input-label">Full name</label>
            <input required type="text" className="input-field" value={name} onChange={(e) => setName(e.target.value)} placeholder="Rahul Sharma" />
          </div>

          <div>
            <label className="input-label">Email</label>
            <input required type="email" className="input-field" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
          </div>

          <div>
            <label className="input-label">Password</label>
            <input required type="password" className="input-field" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="At least 6 characters" />
          </div>

          <div>
            <label className="input-label">Join as</label>
            <select className="input-field" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="student">Student</option>
              <option value="recruiter">Recruiter</option>
              <option value="academician">Academician</option>
            </select>
          </div>

          <button type="submit" className="btn btn-cta" disabled={loading} style={{ padding: 12, fontSize: 15, marginTop: 8 }}>
            {loading ? 'Creating account…' : 'Sign up →'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: 20, fontSize: 13, color: '#12202B', opacity: 0.7 }}>
          Already registered? <Link to="/login" style={{ color: '#B8842E', fontWeight: 600, textDecoration: 'none' }}>Log in</Link>
        </p>
      </motion.div>
    </div>
  );
}
"""

# ─── 11. src/pages/StudentDashboard.jsx ──────────────────────────────────────
files["src/pages/StudentDashboard.jsx"] = """import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import AppShell from '../components/AppShell';
import LoadingSpinner from '../components/LoadingSpinner';

const API = 'http://localhost:8000/api';

function getUserId() {
  try { return JSON.parse(localStorage.getItem('user') || '{}').id || 1; } catch (e) { return 1; }
}
function getUserName() {
  try { return (JSON.parse(localStorage.getItem('user') || '{}').name || 'Student').split(' ')[0]; } catch (e) { return 'Student'; }
}
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState('internships');
  const [internships, setInternships] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [gapCourses, setGapCourses] = useState([]);
  const [careerAdvice, setCareerAdvice] = useState('');
  const [dashboard, setDashboard] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const userId = getUserId();
  const firstName = getUserName();

  useEffect(() => { fetchData(); }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [i, r, g, d] = await Promise.all([
        fetch(`${API}/student/internships`, { headers: getHeaders() }).then(x => x.ok ? x.json() : []).catch(() => []),
        fetch(`${API}/student/recommendations/${userId}`, { headers: getHeaders() }).then(x => x.ok ? x.json() : {}).catch(() => ({})),
        fetch(`${API}/student/gap-courses/${userId}`, { headers: getHeaders() }).then(x => x.ok ? x.json() : {}).catch(() => ({})),
        fetch(`${API}/student/dashboard/${userId}`, { headers: getHeaders() }).then(x => x.ok ? x.json() : {}).catch(() => ({})),
      ]);
      setInternships(Array.isArray(i) ? i : []);
      setRecommendations(r.recommended_internships || r.matched_opportunities || []);
      setGapCourses(r.gap_courses || r.bridge_courses || g.gap_courses || []);
      setCareerAdvice(r.career_advice || '');
      setDashboard(d || {});
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const handleApply = async (oppId) => {
    try {
      const res = await fetch(`${API}/student/apply/${oppId}/${userId}`, {
        method: 'POST', headers: getHeaders(),
        body: JSON.stringify({ cover_letter: 'Applying via SkillBridge' }),
      });
      const data = await res.json();
      toast.success(data.message || 'Application submitted');
    } catch (e) { toast.success('Application submitted'); }
  };

  const tabs = [
    { key: 'internships', label: 'All Internships', count: internships.length },
    { key: 'recommendations', label: 'Recommended', count: recommendations.length },
    { key: 'gap', label: 'Gap Courses', count: gapCourses.length },
  ];

  if (loading) return <AppShell><LoadingSpinner label="Loading your dashboard…" /></AppShell>;

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <div style={{ marginBottom: 24 }}>
          <div className="metric-label" style={{ marginBottom: 6 }}>STUDENT PORTAL</div>
          <h1 style={{ margin: 0 }}>Welcome, {firstName}</h1>
          <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: '6px 0 0 0' }}>
            Verify your skills. Explore opportunities. Close your gaps.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 16, marginBottom: 28 }}>
          <StatCard label="TOTAL SKILLS" value={dashboard.total_skills ?? 0} />
          <StatCard label="VERIFIED SKILLS" value={dashboard.verified_skills ?? 0} accent />
          <StatCard label="ASSESSMENTS" value={dashboard.assessments_taken ?? 0} />
          <StatCard label="APPLICATIONS" value={dashboard.total_applications ?? 0} />
          <StatCard label="OPEN OPPORTUNITIES" value={internships.length} />
        </div>

        <div style={{ display: 'flex', gap: 10, marginBottom: 30, flexWrap: 'wrap' }}>
          <button className="btn btn-cta" onClick={() => navigate('/student/assessment')}>Take an assessment</button>
          <button className="btn btn-secondary" onClick={() => navigate('/student/profile')}>Update profile</button>
          <button className="btn btn-secondary" onClick={() => navigate('/student/recommendations')}>Full recommendations</button>
        </div>

        <div style={{ display: 'flex', gap: 4, borderBottom: '1px solid rgba(14,42,71,0.1)', marginBottom: 24 }}>
          {tabs.map((tab) => {
            const active = activeTab === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                style={{
                  padding: '12px 20px',
                  background: 'transparent',
                  border: 'none',
                  borderBottom: active ? '2px solid #D9A441' : '2px solid transparent',
                  color: active ? '#0E2A47' : '#12202B',
                  fontWeight: active ? 700 : 500,
                  fontSize: 14,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                }}
              >
                {tab.label}
                <span className={active ? 'pill pill-navy' : 'pill pill-blue'} style={{ fontSize: 10 }}>{tab.count}</span>
              </button>
            );
          })}
        </div>

        {activeTab === 'internships' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 20 }}>
            {internships.map((opp) => <InternshipCard key={opp.id} opp={opp} onApply={handleApply} />)}
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div>
            {careerAdvice && (
              <div className="blueprint-card" style={{ marginBottom: 24, background: 'linear-gradient(135deg, #FDF3DC, #FFFFFF)' }}>
                <div className="card-strip">AI STRATEGY</div>
                <h3 style={{ margin: '0 0 10px 0' }}>Personalized career guidance</h3>
                <p style={{ color: '#12202B', opacity: 0.8, fontSize: 14, lineHeight: 1.6, whiteSpace: 'pre-line', margin: 0 }}>{careerAdvice}</p>
              </div>
            )}
            {recommendations.length === 0 ? (
              <EmptyState message="Take an assessment to unlock ranked recommendations." />
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 20 }}>
                {recommendations.map((opp) => <RecommendationCard key={opp.id} opp={opp} onApply={handleApply} />)}
              </div>
            )}
          </div>
        )}

        {activeTab === 'gap' && (
          <div>
            {gapCourses.length === 0 ? (
              <EmptyState message="No skill gaps detected. You are aligned with market demand." />
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: 20 }}>
                {gapCourses.map((gap, i) => <GapCourseCard key={i} gap={gap} />)}
              </div>
            )}
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

function EmptyState({ message }) {
  return (
    <div className="blueprint-card" style={{ textAlign: 'center', padding: '48px 24px' }}>
      <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: 0 }}>{message}</p>
    </div>
  );
}

function InternshipCard({ opp, onApply }) {
  return (
    <div className="blueprint-card">
      <div className="card-strip">{(opp.opportunity_type || 'INTERNSHIP').toUpperCase()}</div>
      <h3 style={{ margin: '0 0 4px 0', fontSize: 16 }}>{opp.title}</h3>
      <p style={{ color: '#2F5C86', fontSize: 13, margin: '0 0 12px 0', fontWeight: 500 }}>{opp.company_name} · {opp.location}</p>
      <div style={{ display: 'flex', gap: 12, fontSize: 12, color: '#12202B', opacity: 0.7, marginBottom: 12 }}>
        <span>💰 ₹{opp.stipend?.toLocaleString() || '—'}/mo</span>
        <span>⏱ {opp.duration}</span>
      </div>
      <p style={{ color: '#12202B', opacity: 0.75, fontSize: 13, lineHeight: 1.5, margin: '0 0 14px 0' }}>
        {opp.description?.slice(0, 120)}…
      </p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5, marginBottom: 16 }}>
        {(opp.required_skills || '').split(',').slice(0, 4).map((s, i) => (
          <span key={i} className="pill pill-blue">{s.trim()}</span>
        ))}
      </div>
      <button className="btn btn-primary" onClick={() => onApply(opp.id)} style={{ width: '100%' }}>Apply now</button>
    </div>
  );
}

function RecommendationCard({ opp, onApply }) {
  const score = opp.match_percentage || opp.match_score || 50;
  return (
    <div className="blueprint-card" style={{ position: 'relative' }}>
      <div style={{ position: 'absolute', top: 16, right: 16 }}>
        <span className="pill pill-green" style={{ fontSize: 12, padding: '4px 10px' }}>{score}% match</span>
      </div>
      <div className="card-strip">RECOMMENDED</div>
      <h3 style={{ margin: '0 0 4px 0', fontSize: 16, paddingRight: 80 }}>{opp.title}</h3>
      <p style={{ color: '#2F5C86', fontSize: 13, margin: '0 0 10px 0', fontWeight: 500 }}>{opp.company_name} · {opp.location}</p>
      <div style={{ display: 'flex', gap: 12, fontSize: 12, color: '#12202B', opacity: 0.7, marginBottom: 12 }}>
        <span>💰 ₹{opp.stipend?.toLocaleString() || '—'}/mo</span>
        <span>⏱ {opp.duration}</span>
      </div>
      <div className="progress-track" style={{ marginBottom: 12 }}>
        <div className="progress-fill green" style={{ width: `${score}%` }} />
      </div>
      {opp.missing_skills?.length > 0 && (
        <div style={{ marginBottom: 14 }}>
          <div className="metric-label" style={{ marginBottom: 6, color: '#C1443C' }}>SKILLS TO IMPROVE</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
            {opp.missing_skills.slice(0, 4).map((s, i) => (
              <span key={i} className="pill pill-red">✗ {s}</span>
            ))}
          </div>
        </div>
      )}
      <button className="btn btn-primary" onClick={() => onApply(opp.id)} style={{ width: '100%' }}>Apply now</button>
    </div>
  );
}

function GapCourseCard({ gap }) {
  return (
    <div className="blueprint-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
        <div>
          <div className="card-strip">SKILL GAP</div>
          <h3 style={{ margin: 0, fontSize: 16 }}>{gap.weak_skill || gap.skill}</h3>
        </div>
        {gap.current_rating > 0 && (
          <span className="pill pill-red" style={{ fontSize: 11 }}>{gap.current_rating}/10</span>
        )}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 14 }}>
        {(gap.courses || []).map((c, i) => (
          <a
            key={i}
            href={c.youtube_url || c.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              padding: 12,
              background: '#FBF9F4',
              border: '1px solid rgba(14,42,71,0.08)',
              borderRadius: 8,
              textDecoration: 'none',
              transition: 'border 0.15s ease',
            }}
            onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#D9A441'; }}
            onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(14,42,71,0.08)'; }}
          >
            <div style={{ background: '#C1443C', color: '#fff', width: 32, height: 32, borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, flexShrink: 0 }}>▶</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <p style={{ margin: 0, fontSize: 13, fontWeight: 600, color: '#0E2A47', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{c.title}</p>
              <p style={{ margin: '2px 0 0 0', fontSize: 11, color: '#2F5C86' }}>{c.provider} · {c.duration}</p>
            </div>
            <span style={{ fontSize: 11, color: '#B8842E', fontWeight: 700 }}>OPEN ↗</span>
          </a>
        ))}
      </div>
    </div>
  );
}
"""

# ─── 12. src/pages/RecommendationsPage.jsx ───────────────────────────────────
files["src/pages/RecommendationsPage.jsx"] = """import React, { useState, useEffect } from 'react';
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

export default function RecommendationsPage() {
  const [data, setData] = useState({ recommended_internships: [], gap_courses: [], career_advice: '', skill_gaps: [] });
  const [loading, setLoading] = useState(true);
  const userId = getUserId();

  useEffect(() => {
    fetch(`${API}/student/recommendations/${userId}`, { headers: getHeaders() })
      .then(r => r.ok ? r.json() : {})
      .then(res => setData({
        recommended_internships: res.recommended_internships || res.matched_opportunities || [],
        gap_courses: res.gap_courses || res.bridge_courses || [],
        career_advice: res.career_advice || '',
        skill_gaps: res.skill_gaps || [],
      }))
      .catch(e => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  const handleApply = async (oppId) => {
    try {
      const res = await fetch(`${API}/student/apply/${oppId}/${userId}`, {
        method: 'POST', headers: getHeaders(),
        body: JSON.stringify({ cover_letter: 'Applying via SkillBridge Recommendations' }),
      });
      const d = await res.json();
      toast.success(d.message || 'Applied successfully');
    } catch (e) { toast.success('Application submitted'); }
  };

  if (loading) return <AppShell><LoadingSpinner label="Finding your matches…" /></AppShell>;

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ marginBottom: 24 }}>
          <div className="metric-label" style={{ marginBottom: 6 }}>PERSONALIZED FOR YOU</div>
          <h1 style={{ margin: 0 }}>Your recommendations</h1>
        </div>

        {data.skill_gaps.length > 0 && (
          <div className="blueprint-card" style={{ marginBottom: 24, background: 'linear-gradient(135deg, #FDF3DC, #FFFFFF)' }}>
            <div className="card-strip">SKILL GAPS TO CLOSE</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 10 }}>
              {data.skill_gaps.slice(0, 8).map((s, i) => (
                <span key={i} className="pill pill-gold">{s.name} · {s.effective_rating}/10</span>
              ))}
            </div>
          </div>
        )}

        {data.career_advice && (
          <div className="blueprint-card" style={{ marginBottom: 30 }}>
            <div className="card-strip">AI ADVISORY</div>
            <h3 style={{ margin: '0 0 8px 0' }}>Career strategy</h3>
            <p style={{ color: '#12202B', opacity: 0.8, fontSize: 14, lineHeight: 1.6, margin: 0, whiteSpace: 'pre-line' }}>{data.career_advice}</p>
          </div>
        )}

        <h2 style={{ marginBottom: 16, fontSize: 20 }}>Internships matched to you</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 20, marginBottom: 36 }}>
          {data.recommended_internships.map((opp) => {
            const score = opp.match_percentage || opp.match_score || 50;
            return (
              <div key={opp.id} className="blueprint-card" style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', top: 16, right: 16 }}>
                  <span className="pill pill-green">{score}% match</span>
                </div>
                <div className="card-strip">INTERNSHIP</div>
                <h3 style={{ margin: '0 0 4px 0', fontSize: 16, paddingRight: 80 }}>{opp.title}</h3>
                <p style={{ color: '#2F5C86', fontSize: 13, margin: '0 0 12px 0' }}>{opp.company_name} · {opp.location}</p>
                <div className="progress-track" style={{ marginBottom: 12 }}>
                  <div className="progress-fill green" style={{ width: `${score}%` }} />
                </div>
                {opp.missing_skills?.length > 0 && (
                  <div style={{ marginBottom: 14 }}>
                    <div className="metric-label" style={{ marginBottom: 6, color: '#C1443C' }}>SKILLS TO IMPROVE</div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                      {opp.missing_skills.slice(0, 4).map((s, i) => <span key={i} className="pill pill-red">✗ {s}</span>)}
                    </div>
                  </div>
                )}
                <button className="btn btn-primary" onClick={() => handleApply(opp.id)} style={{ width: '100%' }}>Apply now</button>
              </div>
            );
          })}
        </div>

        <h2 style={{ marginBottom: 16, fontSize: 20 }}>Free courses to close your gaps</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 20 }}>
          {data.gap_courses.map((gap, i) => (
            <div key={i} className="blueprint-card">
              <div className="card-strip">COURSE · {(gap.weak_skill || gap.skill).toUpperCase()}</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 12 }}>
                {(gap.courses || []).map((c, ci) => (
                  <a key={ci} href={c.youtube_url || c.url} target="_blank" rel="noopener noreferrer"
                    style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 12, background: '#FBF9F4', border: '1px solid rgba(14,42,71,0.08)', borderRadius: 8, textDecoration: 'none' }}>
                    <div style={{ background: '#C1443C', color: '#fff', width: 32, height: 32, borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>▶</div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ margin: 0, fontSize: 13, fontWeight: 600, color: '#0E2A47' }}>{c.title}</p>
                      <p style={{ margin: '2px 0 0 0', fontSize: 11, color: '#2F5C86' }}>{c.provider} · {c.duration}</p>
                    </div>
                    <span style={{ fontSize: 11, color: '#B8842E', fontWeight: 700 }}>OPEN ↗</span>
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </AppShell>
  );
}
"""

# ─── 13. src/pages/AssessmentPage.jsx ────────────────────────────────────────
files["src/pages/AssessmentPage.jsx"] = """import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import AppShell from '../components/AppShell';

const API = 'http://localhost:8000/api';
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

const SKILLS = ['Python', 'Machine Learning', 'React', 'FastAPI', 'SQL', 'Docker', 'AWS', 'JavaScript', 'Computer Vision', 'Cybersecurity', 'Ayurveda Informatics'];

export default function AssessmentPage() {
  const [phase, setPhase] = useState('start');
  const [skill, setSkill] = useState('Python');
  const [difficulty, setDifficulty] = useState('intermediate');
  const [data, setData] = useState(null);
  const [answers, setAnswers] = useState({});
  const [currentQ, setCurrentQ] = useState(0);
  const [timeLeft, setTimeLeft] = useState(60);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (phase !== 'test') return;
    const timer = setInterval(() => setTimeLeft(t => Math.max(0, t - 1)), 1000);
    return () => clearInterval(timer);
  }, [phase, currentQ]);

  const handleStart = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/assessment/start`, {
        method: 'POST', headers: getHeaders(),
        body: JSON.stringify({ skill_name: skill, difficulty }),
      });
      const d = await res.json();
      setData(d);
      setCurrentQ(0);
      setAnswers({});
      setTimeLeft(60);
      setPhase('test');
    } catch (e) { toast.error('Failed to start assessment'); }
    finally { setLoading(false); }
  };

  const handleAnswer = (option) => {
    if (!data?.questions?.[currentQ]) return;
    const qId = data.questions[currentQ].id;
    setAnswers(prev => ({ ...prev, [qId]: option }));
  };

  const handleNext = () => {
    if (currentQ < data.questions.length - 1) {
      setCurrentQ(currentQ + 1);
      setTimeLeft(60);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    const formatted = data.questions.map(q => ({ question_id: q.id, selected_option: answers[q.id] || 'a' }));
    try {
      const res = await fetch(`${API}/assessment/submit`, {
        method: 'POST', headers: getHeaders(),
        body: JSON.stringify({ skill_name: skill, answers: formatted, time_taken_seconds: 120 }),
      });
      const r = await res.json();
      setResult(r);
      setPhase('result');
      toast.success('Assessment complete!');
    } catch (e) { toast.error('Submission failed'); }
    finally { setLoading(false); }
  };

  return (
    <AppShell>
      <AnimatePresence mode="wait">
        {phase === 'start' && (
          <motion.div key="start" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} style={{ maxWidth: 640, margin: '20px auto' }}>
            <div className="blueprint-card" style={{ padding: 36 }}>
              <div className="card-strip">SKILL ASSESSMENT</div>
              <h1 style={{ margin: '0 0 8px 0', fontSize: 28 }}>Adaptive skill verification</h1>
              <p style={{ color: '#12202B', opacity: 0.7, fontSize: 14, margin: '0 0 24px 0', lineHeight: 1.6 }}>
                5 production scenario-based questions. One at a time. 60 seconds each. Powered by Groq Llama-3.3-70B.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                <div>
                  <label className="input-label">Target skill</label>
                  <select className="input-field" value={skill} onChange={e => setSkill(e.target.value)}>
                    {SKILLS.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
                <div>
                  <label className="input-label">Difficulty</label>
                  <select className="input-field" value={difficulty} onChange={e => setDifficulty(e.target.value)}>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate (Production Level)</option>
                    <option value="advanced">Advanced (Principal Engineer)</option>
                  </select>
                </div>
                <button className="btn btn-cta" onClick={handleStart} disabled={loading} style={{ padding: 12, fontSize: 15, marginTop: 8 }}>
                  {loading ? 'Generating questions…' : 'Start assessment →'}
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {phase === 'test' && data && (
          <motion.div key="test" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} style={{ maxWidth: 800, margin: '10px auto' }}>
            <div style={{ marginBottom: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <div className="metric-label">QUESTION {currentQ + 1} OF {data.questions.length}</div>
                <div className="metric-label" style={{ color: timeLeft <= 10 ? '#C1443C' : '#0E2A47' }}>⏱ {timeLeft}s</div>
              </div>
              <div className="progress-track">
                <div className="progress-fill" style={{ width: `${((currentQ + 1) / data.questions.length) * 100}%` }} />
              </div>
            </div>

            <AnimatePresence mode="wait">
              <motion.div key={currentQ} initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -30 }} transition={{ duration: 0.25 }} className="blueprint-card" style={{ padding: 32 }}>
                <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
                  <span className="pill pill-blue">{skill}</span>
                  <span className="pill pill-gold">{difficulty}</span>
                </div>

                {data.questions[currentQ].scenario && (
                  <div style={{ background: '#FBF9F4', border: '1px solid rgba(14,42,71,0.08)', padding: 14, borderRadius: 8, marginBottom: 16 }}>
                    <div className="metric-label" style={{ color: '#B8842E', marginBottom: 6 }}>PRODUCTION SCENARIO</div>
                    <p style={{ fontSize: 13, color: '#12202B', opacity: 0.85, lineHeight: 1.5, margin: 0 }}>{data.questions[currentQ].scenario}</p>
                  </div>
                )}

                <h3 style={{ fontSize: 17, lineHeight: 1.5, margin: '0 0 20px 0', color: '#0E2A47' }}>
                  {data.questions[currentQ].question_text}
                </h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {['a', 'b', 'c', 'd'].map(opt => {
                    const qId = data.questions[currentQ].id;
                    const isSelected = answers[qId] === opt;
                    return (
                      <button
                        key={opt}
                        onClick={() => handleAnswer(opt)}
                        style={{
                          display: 'flex',
                          gap: 12,
                          alignItems: 'flex-start',
                          padding: '12px 16px',
                          background: isSelected ? '#EEF3F9' : '#ffffff',
                          border: isSelected ? '2px solid #D9A441' : '1.5px solid rgba(14,42,71,0.12)',
                          borderRadius: 8,
                          cursor: 'pointer',
                          textAlign: 'left',
                          fontSize: 14,
                          lineHeight: 1.5,
                          color: '#12202B',
                          transition: 'all 0.15s ease',
                        }}
                      >
                        <span style={{
                          width: 28, height: 28, borderRadius: '50%',
                          background: isSelected ? '#D9A441' : '#EEF3F9',
                          color: isSelected ? '#0E2A47' : '#2F5C86',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          fontWeight: 700, fontSize: 12, flexShrink: 0,
                        }}>{opt.toUpperCase()}</span>
                        <span>{data.questions[currentQ][`option_${opt}`]}</span>
                      </button>
                    );
                  })}
                </div>

                <button onClick={handleNext} disabled={loading} className="btn btn-primary" style={{ width: '100%', marginTop: 24, padding: 12 }}>
                  {currentQ < data.questions.length - 1 ? 'Submit answer →' : (loading ? 'Evaluating…' : 'Finish & get results →')}
                </button>
              </motion.div>
            </AnimatePresence>
          </motion.div>
        )}

        {phase === 'result' && result && (
          <motion.div key="result" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} style={{ maxWidth: 720, margin: '20px auto' }}>
            <div className="blueprint-card" style={{ padding: 40, textAlign: 'center' }}>
              <div className="card-strip">SKILL REPORT</div>

              <div style={{
                width: 140, height: 140,
                margin: '20px auto 24px',
                border: '4px solid #D9A441',
                borderRadius: '50%',
                display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center',
                background: '#FBF9F4',
              }}>
                <div style={{ fontFamily: '"Space Grotesk", sans-serif', fontSize: 42, fontWeight: 700, color: '#0E2A47', lineHeight: 1 }}>
                  {result.score}%
                </div>
                <div className="metric-label" style={{ marginTop: 4 }}>OVERALL</div>
              </div>

              <h2 style={{ margin: '0 0 8px 0' }}>{result.skill_name} · {result.verified_level}</h2>
              <p style={{ color: '#12202B', opacity: 0.7, fontSize: 14, margin: '0 0 24px 0' }}>
                Verified rating: <strong style={{ color: '#B8842E' }}>{result.verified_rating}/10</strong>
              </p>

              <div style={{ display: 'flex', gap: 10, justifyContent: 'center', flexWrap: 'wrap' }}>
                <button onClick={() => { setPhase('start'); setResult(null); }} className="btn btn-secondary">Take another</button>
                <button onClick={() => navigate('/student/recommendations')} className="btn btn-cta">View personalized recommendations →</button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </AppShell>
  );
}
"""

# ─── 14. src/pages/ProfilePage.jsx ───────────────────────────────────────────
files["src/pages/ProfilePage.jsx"] = """import React, { useState, useEffect } from 'react';
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
"""

# ─── 15. src/pages/RecruiterDashboard.jsx ────────────────────────────────────
files["src/pages/RecruiterDashboard.jsx"] = """import React, { useState, useEffect } from 'react';
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
"""

# ─── 16. src/pages/PostOpportunityPage.jsx ───────────────────────────────────
files["src/pages/PostOpportunityPage.jsx"] = """import React, { useState } from 'react';
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
"""

# ─── 17. src/pages/CandidateRecommendationsPage.jsx ──────────────────────────
files["src/pages/CandidateRecommendationsPage.jsx"] = """import React, { useState, useEffect } from 'react';
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
"""

# ─── 18. src/pages/AcademicianDashboard.jsx ──────────────────────────────────
files["src/pages/AcademicianDashboard.jsx"] = """import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import AppShell from '../components/AppShell';
import LoadingSpinner from '../components/LoadingSpinner';

const API = 'http://localhost:8000/api';
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

export default function AcademicianDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/academician/dashboard`, { headers: getHeaders() })
      .then(r => r.ok ? r.json() : {})
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <AppShell><LoadingSpinner label="Loading department analytics…" /></AppShell>;
  if (!data) return <AppShell><div>No data</div></AppShell>;

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ marginBottom: 24 }}>
          <div className="metric-label" style={{ marginBottom: 6 }}>DEPARTMENT ANALYTICS · NAAC/NIRF ALIGNED</div>
          <h1 style={{ margin: 0 }}>{data.institution || 'Institution'} · {data.department || 'Department'}</h1>
          <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: '4px 0 0 0' }}>
            Live cohort skill mapping, market demand alignment, and predictive capacity building.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 16, marginBottom: 30 }}>
          <StatCard label="COHORT STUDENTS" value={data.total_students ?? 0} />
          <StatCard label="PLACEMENT RATE" value={`${data.placement_rate ?? 0}%`} accent />
          <StatCard label="OFFERS EXTENDED" value={data.total_placed ?? 0} />
          <StatCard label="ASSESSMENTS TAKEN" value={data.assessments_completed ?? 0} />
          <StatCard label="AVG SCORE" value={`${data.avg_assessment_score ?? 0}%`} />
        </div>

        <h2 style={{ marginBottom: 16, fontSize: 20 }}>Skill Gap Matrix vs Industry Demand</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 16, marginBottom: 30 }}>
          {(data.skill_gaps || []).map((gap, i) => (
            <div key={i} className="blueprint-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                <div>
                  <div className="card-strip">SKILL GAP</div>
                  <h3 style={{ margin: 0, fontSize: 16 }}>{gap.skill_name}</h3>
                </div>
                <span className={`pill ${gap.gap_severity === 'Critical' ? 'pill-red' : 'pill-gold'}`}>{gap.gap_severity}</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
                  <span style={{ color: '#2F5C86' }}>Industry demand</span>
                  <strong style={{ color: '#0E2A47' }}>{gap.industry_demand}</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12 }}>
                  <span style={{ color: '#2F5C86' }}>Students proficient</span>
                  <strong style={{ color: '#0E2A47' }}>{gap.students_with_skill}</strong>
                </div>
              </div>
              <p style={{ marginTop: 12, marginBottom: 0, fontSize: 12, color: '#12202B', opacity: 0.7, lineHeight: 1.4 }}>
                <strong>Action:</strong> {gap.recommended_action}
              </p>
            </div>
          ))}
        </div>

        <h2 style={{ marginBottom: 16, fontSize: 20 }}>Cohort skill distribution</h2>
        <div className="blueprint-card" style={{ padding: 20 }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {(data.skill_distribution || []).map((s, i) => (
              <div key={i} style={{ background: '#FBF9F4', padding: '10px 14px', borderRadius: 8, border: '1px solid rgba(14,42,71,0.08)' }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: '#0E2A47' }}>{s.skill_name}</div>
                <div style={{ fontSize: 11, color: '#2F5C86', marginTop: 2 }}>
                  {s.student_count} students · {s.verified_count} verified
                </div>
              </div>
            ))}
          </div>
        </div>
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
"""

# ─── 19. src/App.jsx ─────────────────────────────────────────────────────────
files["src/App.jsx"] = """import React from 'react';
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
"""

# ─── 20. src/main.jsx ────────────────────────────────────────────────────────
files["src/main.jsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { Toaster } from 'react-hot-toast';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
    <Toaster
      position="top-right"
      toastOptions={{
        style: {
          background: '#0E2A47',
          color: '#F1F5F9',
          fontFamily: 'Inter, sans-serif',
          fontSize: 13,
          border: '1px solid rgba(217,164,65,0.3)',
        },
      }}
    />
  </React.StrictMode>
);
"""

# Write all files cleanly
for path, content in files.items():
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Written: {path}")

print("\n🚀 All files successfully written.")
