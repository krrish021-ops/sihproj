import React from 'react';
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
