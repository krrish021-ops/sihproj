import React, { useState, useEffect } from 'react';
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
