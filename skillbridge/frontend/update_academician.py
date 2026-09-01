import os

files = {}

files["src/pages/AcademicianDashboard.jsx"] = """import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import AppShell from '../components/AppShell';
import LoadingSpinner from '../components/LoadingSpinner';

const API = 'http://localhost:8000/api';
const getHeaders = () => {
  const t = localStorage.getItem('token') || localStorage.getItem('access_token') || '';
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${t}` };
};

export default function AcademicianDashboard() {
  const [data, setData] = useState(null);
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [studentDetail, setStudentDetail] = useState(null);
  const [activeView, setActiveView] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/academician/dashboard`, { headers: getHeaders() }).then(r => r.ok ? r.json() : {}),
      fetch(`${API}/academician/students`, { headers: getHeaders() }).then(r => r.ok ? r.json() : { students: [] }),
    ])
      .then(([dashData, studData]) => {
        setData(dashData);
        setStudents(studData.students || []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleSelectStudent = async (studentId) => {
    setDetailLoading(true);
    setSelectedStudent(studentId);
    setActiveView('student-detail');
    try {
      const res = await fetch(`${API}/academician/students/${studentId}`, { headers: getHeaders() });
      const detail = await res.json();
      setStudentDetail(detail);
    } catch (e) {
      console.error(e);
    } finally {
      setDetailLoading(false);
    }
  };

  const filteredStudents = students.filter(s =>
    s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.skill_names.some(sk => sk.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  if (loading) return <AppShell><LoadingSpinner label="Loading department analytics..." /></AppShell>;
  if (!data) return <AppShell><div>No data</div></AppShell>;

  return (
    <AppShell>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>

        {/* VIEW TOGGLE */}
        <div style={{ display: 'flex', gap: 4, borderBottom: '1px solid rgba(14,42,71,0.1)', marginBottom: 24 }}>
          {[
            { key: 'overview', label: 'Department Overview' },
            { key: 'students', label: `Student Roster (${students.length})` },
          ].map(tab => (
            <button key={tab.key} onClick={() => { setActiveView(tab.key); setSelectedStudent(null); }}
              style={{ padding: '12px 20px', background: 'transparent', border: 'none', borderBottom: activeView === tab.key ? '2px solid #D9A441' : '2px solid transparent', color: activeView === tab.key ? '#0E2A47' : '#12202B', fontWeight: activeView === tab.key ? 700 : 500, fontSize: 14, cursor: 'pointer' }}>
              {tab.label}
            </button>
          ))}
          {selectedStudent && (
            <button onClick={() => setActiveView('student-detail')}
              style={{ padding: '12px 20px', background: 'transparent', border: 'none', borderBottom: activeView === 'student-detail' ? '2px solid #D9A441' : '2px solid transparent', color: '#0E2A47', fontWeight: 700, fontSize: 14, cursor: 'pointer' }}>
              Student Detail
            </button>
          )}
        </div>

        {/* OVERVIEW TAB */}
        {activeView === 'overview' && (
          <div>
            <div style={{ marginBottom: 24 }}>
              <div className="metric-label" style={{ marginBottom: 6 }}>DEPARTMENT ANALYTICS</div>
              <h1 style={{ margin: 0 }}>{data.institution || 'Institution'} - {data.department || 'Department'}</h1>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 16, marginBottom: 30 }}>
              <StatCard label="COHORT STUDENTS" value={data.total_students ?? 0} />
              <StatCard label="PLACEMENT RATE" value={`${data.placement_rate ?? 0}%`} accent />
              <StatCard label="OFFERS" value={data.total_placed ?? 0} />
              <StatCard label="ASSESSMENTS" value={data.assessments_completed ?? 0} />
              <StatCard label="AVG SCORE" value={`${data.avg_assessment_score ?? 0}%`} />
            </div>

            <h2 style={{ marginBottom: 16, fontSize: 20 }}>Skill Gap Matrix</h2>
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
                  <p style={{ marginTop: 8, marginBottom: 0, fontSize: 12, color: '#12202B', opacity: 0.7 }}>
                    <strong>Action:</strong> {gap.recommended_action}
                  </p>
                </div>
              ))}
            </div>

            <h2 style={{ marginBottom: 16, fontSize: 20 }}>Skill Distribution</h2>
            <div className="blueprint-card" style={{ padding: 20 }}>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                {(data.skill_distribution || []).map((s, i) => (
                  <div key={i} style={{ background: '#FBF9F4', padding: '10px 14px', borderRadius: 8, border: '1px solid rgba(14,42,71,0.08)' }}>
                    <div style={{ fontSize: 13, fontWeight: 600, color: '#0E2A47' }}>{s.skill_name}</div>
                    <div style={{ fontSize: 11, color: '#2F5C86', marginTop: 2 }}>{s.student_count} students ({s.verified_count} verified)</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* STUDENT ROSTER TAB */}
        {activeView === 'students' && (
          <div>
            <div style={{ marginBottom: 24 }}>
              <div className="metric-label" style={{ marginBottom: 6 }}>STUDENT ROSTER</div>
              <h1 style={{ margin: 0 }}>All Students ({students.length})</h1>
              <p style={{ color: '#12202B', opacity: 0.6, fontSize: 14, margin: '4px 0 0 0' }}>
                Click any student to view their detailed skill progress, assessment history, and placement status.
              </p>
            </div>

            <div style={{ marginBottom: 20 }}>
              <input
                type="text"
                placeholder="Search by name, email, or skill..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="input-field"
                style={{ maxWidth: 400 }}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))', gap: 16 }}>
              {filteredStudents.map(s => (
                <div key={s.id} className="blueprint-card" style={{ cursor: 'pointer' }} onClick={() => handleSelectStudent(s.id)}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                      <div style={{ width: 44, height: 44, borderRadius: '50%', background: '#0E2A47', color: '#D9A441', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 18, fontFamily: '"Space Grotesk", sans-serif' }}>
                        {s.name[0].toUpperCase()}
                      </div>
                      <div>
                        <h3 style={{ margin: 0, fontSize: 15 }}>{s.name}</h3>
                        <p style={{ color: '#2F5C86', fontSize: 12, margin: '2px 0 0 0' }}>{s.email}</p>
                      </div>
                    </div>
                    <span className={`pill ${s.latest_application_status === 'offered' || s.latest_application_status === 'accepted' ? 'pill-green' : s.latest_application_status === 'not_applied' ? 'pill-gold' : 'pill-blue'}`}>
                      {s.latest_application_status.replace('_', ' ')}
                    </span>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8, marginTop: 16, paddingTop: 12, borderTop: '1px solid rgba(14,42,71,0.08)' }}>
                    <MiniStat label="CGPA" value={s.cgpa || '—'} />
                    <MiniStat label="Skills" value={`${s.verified_skills}/${s.total_skills}`} color={s.verified_skills > 0 ? '#3D8361' : '#C1443C'} />
                    <MiniStat label="Tests" value={s.assessments_taken} />
                    <MiniStat label="Avg Score" value={`${s.avg_assessment_score}%`} color={s.avg_assessment_score >= 70 ? '#3D8361' : s.avg_assessment_score >= 50 ? '#B8842E' : '#C1443C'} />
                  </div>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 10 }}>
                    {s.skill_names.slice(0, 5).map((sk, i) => (
                      <span key={i} className="pill pill-blue" style={{ fontSize: 10 }}>{sk}</span>
                    ))}
                    {s.skill_names.length > 5 && <span className="pill pill-gold" style={{ fontSize: 10 }}>+{s.skill_names.length - 5}</span>}
                  </div>
                </div>
              ))}
            </div>

            {filteredStudents.length === 0 && (
              <div className="blueprint-card" style={{ textAlign: 'center', padding: 40 }}>
                <p style={{ color: '#12202B', opacity: 0.6, margin: 0 }}>No students match your search.</p>
              </div>
            )}
          </div>
        )}

        {/* STUDENT DETAIL TAB */}
        {activeView === 'student-detail' && (
          <div>
            <button onClick={() => setActiveView('students')} className="btn btn-ghost" style={{ marginBottom: 16, padding: '6px 10px' }}>
              ← Back to Student Roster
            </button>

            {detailLoading ? (
              <LoadingSpinner label="Loading student progress..." />
            ) : studentDetail ? (
              <StudentDetailView detail={studentDetail} />
            ) : (
              <div className="blueprint-card" style={{ textAlign: 'center', padding: 40 }}>
                <p style={{ color: '#12202B', opacity: 0.6 }}>Select a student to view details.</p>
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

function MiniStat({ label, value, color }) {
  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ fontSize: 14, fontWeight: 700, color: color || '#0E2A47', fontFamily: '"Space Grotesk", sans-serif' }}>{value}</div>
      <div className="metric-label" style={{ fontSize: 9 }}>{label}</div>
    </div>
  );
}

function StudentDetailView({ detail }) {
  const { student, profile, skills, assessments, applications, projects, overall_progress } = detail;

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
      {/* Student Header */}
      <div className="blueprint-card" style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
        <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
          <div style={{ width: 64, height: 64, borderRadius: '50%', background: '#0E2A47', color: '#D9A441', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 28, fontFamily: '"Space Grotesk", sans-serif' }}>
            {student.name[0].toUpperCase()}
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: 24 }}>{student.name}</h1>
            <p style={{ color: '#2F5C86', fontSize: 13, margin: '4px 0 0 0' }}>
              {profile.college} · {profile.department} · Year {profile.year_of_study} · CGPA {profile.cgpa}
            </p>
            <p style={{ color: '#94a3b8', fontSize: 12, margin: '2px 0 0 0' }}>{student.email}</p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: 12 }}>
          <div style={{ textAlign: 'center', padding: '8px 16px', background: '#FBF9F4', borderRadius: 8 }}>
            <div className="metric-label">VERIFICATION</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: '#3D8361', fontFamily: '"Space Grotesk"' }}>{overall_progress.skill_verification_rate}%</div>
          </div>
          <div style={{ textAlign: 'center', padding: '8px 16px', background: '#FBF9F4', borderRadius: 8 }}>
            <div className="metric-label">AVG SCORE</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: '#0E2A47', fontFamily: '"Space Grotesk"' }}>{overall_progress.avg_assessment_score}%</div>
          </div>
          <div style={{ textAlign: 'center', padding: '8px 16px', background: '#FBF9F4', borderRadius: 8 }}>
            <div className="metric-label">STATUS</div>
            <span className={`pill ${overall_progress.placement_status === 'Placed' ? 'pill-green' : overall_progress.placement_status === 'In Progress' ? 'pill-gold' : 'pill-blue'}`} style={{ fontSize: 12, marginTop: 4 }}>
              {overall_progress.placement_status}
            </span>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 20 }}>

        {/* Skills Progress */}
        <div className="blueprint-card">
          <div className="card-strip">SKILL PROFICIENCY</div>
          <h3 style={{ margin: '0 0 16px 0', fontSize: 16 }}>Verified vs Self-Rated</h3>
          {skills.length === 0 ? (
            <p style={{ color: '#94a3b8', fontSize: 13 }}>No skills added yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {skills.map(s => (
                <div key={s.id}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4, alignItems: 'center' }}>
                    <span style={{ fontSize: 13, fontWeight: 600, color: '#0E2A47' }}>{s.skill_name}</span>
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                      {s.is_verified ? (
                        <span className="pill pill-green" style={{ fontSize: 10 }}>Verified {s.verified_rating}/10</span>
                      ) : (
                        <span className="pill pill-gold" style={{ fontSize: 10 }}>Self {s.self_rating}/10</span>
                      )}
                      {s.assessment_attempts > 0 && (
                        <span className="pill pill-blue" style={{ fontSize: 10 }}>{s.assessment_attempts} tests</span>
                      )}
                    </div>
                  </div>
                  <div className="progress-track" style={{ height: 6 }}>
                    <div className={`progress-fill ${s.is_verified ? 'green' : 'gold'}`} style={{ width: `${(s.is_verified ? s.verified_rating : s.self_rating) * 10}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Assessment History */}
        <div className="blueprint-card">
          <div className="card-strip">ASSESSMENT HISTORY</div>
          <h3 style={{ margin: '0 0 16px 0', fontSize: 16 }}>Test Results ({assessments.length} taken)</h3>
          {assessments.length === 0 ? (
            <p style={{ color: '#94a3b8', fontSize: 13 }}>No assessments completed yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {assessments.slice(0, 8).map(a => (
                <div key={a.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 12px', background: '#FBF9F4', borderRadius: 8, border: '1px solid rgba(14,42,71,0.06)' }}>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: '#0E2A47' }}>{a.skill_name}</div>
                    <div style={{ fontSize: 11, color: '#94a3b8' }}>{a.correct_answers}/{a.total_questions} correct · {a.verified_level}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: 18, fontWeight: 700, color: a.score >= 70 ? '#3D8361' : a.score >= 50 ? '#B8842E' : '#C1443C', fontFamily: '"Space Grotesk"' }}>
                      {a.score}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Applications */}
        <div className="blueprint-card">
          <div className="card-strip">APPLICATION TRACKER</div>
          <h3 style={{ margin: '0 0 16px 0', fontSize: 16 }}>Placement Pipeline ({applications.length} sent)</h3>
          {applications.length === 0 ? (
            <p style={{ color: '#94a3b8', fontSize: 13 }}>No applications submitted yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {applications.slice(0, 6).map(a => (
                <div key={a.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 12px', background: '#FBF9F4', borderRadius: 8, border: '1px solid rgba(14,42,71,0.06)' }}>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: '#0E2A47' }}>{a.opportunity_title}</div>
                    <div style={{ fontSize: 11, color: '#94a3b8' }}>{a.company_name} · Match {a.match_score}%</div>
                  </div>
                  <span className={`pill ${a.status === 'offered' || a.status === 'accepted' ? 'pill-green' : a.status === 'rejected' ? 'pill-red' : a.status === 'shortlisted' || a.status === 'interviewed' ? 'pill-gold' : 'pill-blue'}`}>
                    {a.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Projects */}
        <div className="blueprint-card">
          <div className="card-strip">PROJECTS</div>
          <h3 style={{ margin: '0 0 16px 0', fontSize: 16 }}>Portfolio ({projects.length} projects)</h3>
          {projects.length === 0 ? (
            <p style={{ color: '#94a3b8', fontSize: 13 }}>No projects added yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {projects.map(p => (
                <div key={p.id} style={{ padding: '10px 12px', background: '#FBF9F4', borderRadius: 8, border: '1px solid rgba(14,42,71,0.06)' }}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: '#0E2A47' }}>{p.title}</div>
                  <div style={{ fontSize: 11, color: '#94a3b8', marginTop: 2 }}>{p.tech_stack}</div>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </motion.div>
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

print("🚀 Academician dashboard updated with Student Roster & Progress Tracker.")
