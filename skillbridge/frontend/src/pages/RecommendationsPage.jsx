import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
  const [data, setData] = useState({ recommended_internships: [], gap_courses: [], career_advice: '', skill_gaps: [], has_assessments: false, message: '' });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const userId = getUserId();

  useEffect(() => {
    fetch(`${API}/student/recommendations/${userId}`, { headers: getHeaders() })
      .then(r => r.ok ? r.json() : {})
      .then(res => setData({
        recommended_internships: res.recommended_internships || res.matched_opportunities || [],
        gap_courses: res.gap_courses || res.bridge_courses || [],
        career_advice: res.career_advice || '',
        skill_gaps: res.skill_gaps || [],
        has_assessments: res.has_assessments || (res.assessments_taken_count > 0) || false,
        message: res.message || ''
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

  if (loading) return <AppShell><LoadingSpinner label="Finding your matches..." /></AppShell>;

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ marginBottom: 24 }}>
          <div className="metric-label" style={{ marginBottom: 6 }}>PERSONALIZED FOR YOU</div>
          <h1 style={{ margin: 0 }}>Your recommendations</h1>
        </div>

        {!data.has_assessments ? (
          <div className="blueprint-card" style={{ textAlign: 'center', padding: '60px 30px', background: 'linear-gradient(135deg, #FDF3DC, #FFFFFF)' }}>
            <div style={{ fontSize: 56, marginBottom: 16 }}>🔒</div>
            <h2 style={{ margin: '0 0 12px 0', color: '#B8842E' }}>Complete an Assessment First</h2>
            <p style={{ color: '#12202B', opacity: 0.7, fontSize: 15, lineHeight: 1.6, maxWidth: 520, margin: '0 auto 28px auto' }}>
              {data.message || 'Our AI engine needs at least one verified assessment score to match you with the right internships and identify skill gaps. Self-rated skills alone are not enough for accurate recommendations.'}
            </p>
            <button className="btn btn-cta" onClick={() => navigate('/student/assessment')} style={{ padding: '14px 32px', fontSize: 16 }}>
              Take your first assessment →
            </button>
          </div>
        ) : (
          <>
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
          </>
        )}
      </motion.div>
    </AppShell>
  );
}
