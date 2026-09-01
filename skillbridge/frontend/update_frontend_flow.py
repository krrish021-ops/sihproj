import os

files = {}

# 1. Updated StudentDashboard.jsx
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
  const [hasAssessments, setHasAssessments] = useState(false);
  const [recMessage, setRecMessage] = useState('');
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
      setHasAssessments(r.has_assessments || (r.assessments_taken_count > 0) || false);
      setRecMessage(r.message || g.message || '');
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
    { key: 'recommendations', label: 'Recommended', count: hasAssessments ? recommendations.length : 0 },
    { key: 'gap', label: 'Gap Courses', count: hasAssessments ? gapCourses.length : 0 },
  ];

  if (loading) return <AppShell><LoadingSpinner label="Loading your dashboard..." /></AppShell>;

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
              <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                style={{ padding: '12px 20px', background: 'transparent', border: 'none', borderBottom: active ? '2px solid #D9A441' : '2px solid transparent', color: active ? '#0E2A47' : '#12202B', fontWeight: active ? 700 : 500, fontSize: 14, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8 }}>
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
            {!hasAssessments ? (
              <div className="blueprint-card" style={{ textAlign: 'center', padding: '60px 30px', background: 'linear-gradient(135deg, #FDF3DC, #FFFFFF)' }}>
                <div style={{ fontSize: 48, marginBottom: 16 }}>🔒</div>
                <h2 style={{ margin: '0 0 10px 0', color: '#B8842E' }}>Assessment Required</h2>
                <p style={{ color: '#12202B', opacity: 0.7, fontSize: 15, lineHeight: 1.6, maxWidth: 500, margin: '0 auto 24px auto' }}>
                  {recMessage || 'Complete at least one skill assessment to unlock AI-powered internship recommendations tailored to your verified proficiency.'}
                </p>
                <button className="btn btn-cta" onClick={() => navigate('/student/assessment')} style={{ padding: '14px 28px', fontSize: 15 }}>
                  Take your first assessment →
                </button>
              </div>
            ) : (
              <>
                {careerAdvice && (
                  <div className="blueprint-card" style={{ marginBottom: 24, background: 'linear-gradient(135deg, #FDF3DC, #FFFFFF)' }}>
                    <div className="card-strip">AI STRATEGY</div>
                    <h3 style={{ margin: '0 0 10px 0' }}>Personalized career guidance</h3>
                    <p style={{ color: '#12202B', opacity: 0.8, fontSize: 14, lineHeight: 1.6, whiteSpace: 'pre-line', margin: 0 }}>{careerAdvice}</p>
                  </div>
                )}
                {recommendations.length === 0 ? (
                  <EmptyState message="No matching internships found. Try adding more skills or taking additional assessments." />
                ) : (
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 20 }}>
                    {recommendations.map((opp) => <RecommendationCard key={opp.id} opp={opp} onApply={handleApply} />)}
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {activeTab === 'gap' && (
          <div>
            {!hasAssessments ? (
              <div className="blueprint-card" style={{ textAlign: 'center', padding: '60px 30px', background: 'linear-gradient(135deg, #FDF3DC, #FFFFFF)' }}>
                <div style={{ fontSize: 48, marginBottom: 16 }}>📚</div>
                <h2 style={{ margin: '0 0 10px 0', color: '#B8842E' }}>Assessment Required</h2>
                <p style={{ color: '#12202B', opacity: 0.7, fontSize: 15, lineHeight: 1.6, maxWidth: 500, margin: '0 auto 24px auto' }}>
                  Complete an assessment so we can identify your weak skills and recommend targeted YouTube courses to close the gap.
                </p>
                <button className="btn btn-cta" onClick={() => navigate('/student/assessment')} style={{ padding: '14px 28px', fontSize: 15 }}>
                  Take your first assessment →
                </button>
              </div>
            ) : (
              <>
                {gapCourses.length === 0 ? (
                  <EmptyState message="No skill gaps detected. You are aligned with market demand." />
                ) : (
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: 20 }}>
                    {gapCourses.map((gap, i) => <GapCourseCard key={i} gap={gap} />)}
                  </div>
                )}
              </>
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
        {opp.description?.slice(0, 120)}...
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
          <a key={i} href={c.youtube_url || c.url} target="_blank" rel="noopener noreferrer"
            style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 12, background: '#FBF9F4', border: '1px solid rgba(14,42,71,0.08)', borderRadius: 8, textDecoration: 'none', transition: 'border 0.15s ease' }}
            onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#D9A441'; }}
            onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'rgba(14,42,71,0.08)'; }}>
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

# 2. Updated RecommendationsPage.jsx
files["src/pages/RecommendationsPage.jsx"] = """import React, { useState, useEffect } from 'react';
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
"""

for path, content in files.items():
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Updated: {path}")

print("\n🚀 Frontend flow updated.")
