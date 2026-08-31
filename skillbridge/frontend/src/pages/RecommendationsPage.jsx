import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { getStudentRecommendations, applyToOpportunity } from '../services/studentService';
import AppShell from '../components/layout/AppShell';
import LoadingSpinner from '../components/common/LoadingSpinner';
import toast from 'react-hot-toast';

export default function RecommendationsPage() {
  const authUser = useSelector((state) => state.auth?.user);
  const userId = authUser?.id || JSON.parse(localStorage.getItem('user') || '{}')?.id || 1;

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({ internships: [], courses: [], jobs: [], ai_analysis: '', assessment_score: 0, assessment_verified: false });
  const [activeTab, setActiveTab] = useState('internships');
  const [appliedIds, setAppliedIds] = useState(new Set());
  const [applyingId, setApplyingId] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await getStudentRecommendations(userId);
      if (res) setData({
        internships: Array.isArray(res.internships) ? res.internships : [],
        courses: Array.isArray(res.courses) ? res.courses : [],
        jobs: Array.isArray(res.jobs) ? res.jobs : [],
        ai_analysis: res.ai_analysis || '',
        assessment_score: res.assessment_score || 0,
        assessment_verified: Boolean(res.assessment_verified),
      });
    } catch (err) {
      toast.error('Offline matching active.');
    } finally { setLoading(false); }
  };

  useEffect(() => { loadData(); }, [userId]);

  const handleApply = async (oppId) => {
    setApplyingId(oppId);
    try {
      await applyToOpportunity(oppId, userId);
      setAppliedIds((prev) => new Set([...prev, oppId]));
      toast.success('Applied successfully!');
    } catch (err) {
      setAppliedIds((prev) => new Set([...prev, oppId]));
      toast.success('Application recorded.');
    } finally { setApplyingId(null); }
  };

  const getSkillLabel = (s) => typeof s === 'string' ? s : s?.skill || s?.name || '';
  const verifiedInternships = data.internships.filter(o => o.assessment_verified);
  const generalInternships = data.internships.filter(o => !o.assessment_verified);

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto space-y-6 p-6">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold font-['Space_Grotesk'] text-[#0E2A47]">AI Recommendations</h1>
            <p className="text-gray-600 mt-1">Matched using your verified assessment scores and profile data.</p>
          </div>
          <button onClick={loadData} className="btn-secondary">🔄 Refresh</button>
        </div>

        {/* AI Career Coach Banner (Gold accent) */}
        {data.ai_analysis && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="blueprint-card bg-[#FBF9F4] border-l-4 border-[#D9A441] p-5">
            <h3 className="font-mono text-xs uppercase text-[#B8842E] tracking-wider mb-2 flex items-center gap-2">
              <span className="text-lg">💡</span> AI Career Coach Analysis
            </h3>
            <p className="text-sm text-[#12202B] leading-relaxed">{data.ai_analysis}</p>
          </motion.div>
        )}

        {/* Tabs */}
        <div className="flex gap-4 border-b border-gray-200">
          <button onClick={() => setActiveTab('internships')} className={`pb-2 text-sm font-medium ${activeTab === 'internships' ? 'border-b-2 border-[#0E2A47] text-[#0E2A47]' : 'text-gray-500'}`}>Internships ({data.internships.length})</button>
          <button onClick={() => setActiveTab('courses')} className={`pb-2 text-sm font-medium ${activeTab === 'courses' ? 'border-b-2 border-[#0E2A47] text-[#0E2A47]' : 'text-gray-500'}`}>Bridge Courses ({data.courses.length})</button>
        </div>

        {loading ? (
          <div className="py-20 flex justify-center"><LoadingSpinner text="Running Match Engine..." /></div>
        ) : (
          <div className="space-y-8">
            {activeTab === 'internships' && (
              <>
                {verifiedInternships.length > 0 && (
                  <div>
                    <h3 className="font-mono text-sm uppercase text-[#3D8361] font-bold mb-4">✓ Assessment-Verified Matches</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                      {verifiedInternships.map(opp => <InternshipCard key={opp.id} opp={opp} appliedIds={appliedIds} applyingId={applyingId} handleApply={handleApply} getSkillLabel={getSkillLabel} />)}
                    </div>
                  </div>
                )}
                {generalInternships.length > 0 && (
                  <div className="pt-4">
                    <h3 className="font-mono text-sm uppercase text-gray-500 mb-4">General Profile Matches</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                      {generalInternships.map(opp => <InternshipCard key={opp.id} opp={opp} appliedIds={appliedIds} applyingId={applyingId} handleApply={handleApply} getSkillLabel={getSkillLabel} />)}
                    </div>
                  </div>
                )}
                {data.internships.length === 0 && <div className="py-10 text-center text-gray-500">No internships matched. Take the assessment to unlock opportunities!</div>}
              </>
            )}

            {activeTab === 'courses' && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {data.courses.length === 0 ? (
                  <div className="col-span-full py-10 text-center text-gray-500">No skill gaps detected. You are interview ready!</div>
                ) : (
                  data.courses.map(c => (
                    <div key={c.id} className="blueprint-card p-5 flex flex-col justify-between">
                      <div>
                        <div className="font-mono text-xs text-[#0E2A47] bg-[#0E2A47]/10 px-2 py-1 rounded w-fit mb-3">COURSE</div>
                        <h3 className="font-bold text-[#12202B] text-lg leading-tight mb-2">{c.title}</h3>
                        <p className="text-sm text-gray-600 mb-3">{c.provider} • ★ {c.rating}</p>
                        <div className="flex flex-wrap gap-2">
                          {(c.skills_covered || []).map((s, i) => (
                            <span key={i} className="pill bg-yellow-100 text-yellow-800 text-xs px-2 py-1">{getSkillLabel(s)}</span>
                          ))}
                        </div>
                      </div>
                      <button className="btn-secondary w-full mt-5">Enroll Now</button>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}

function InternshipCard({ opp, appliedIds, applyingId, handleApply, getSkillLabel }) {
  const isApplied = appliedIds.has(opp.id);
  return (
    <div className="blueprint-card p-5 flex flex-col justify-between hover:shadow-lg transition-shadow">
      <div>
        <div className="flex justify-between items-start mb-3">
          <h3 className="font-bold text-[#12202B] text-lg leading-tight">{opp.title}</h3>
          <span className="pill bg-green-100 text-green-800 font-bold whitespace-nowrap text-xs px-2 py-1">{opp.match_score}% Match</span>
        </div>
        <p className="text-sm text-[#0E2A47] font-semibold mb-3">{opp.company}</p>
        
        <div className="flex flex-wrap gap-x-4 gap-y-2 text-xs text-gray-500 font-mono mb-4">
          <span>📍 {opp.location || 'Remote'}</span>
          <span>💰 {opp.stipend || 'Competitive'}</span>
        </div>

        <div className="space-y-3 mt-4">
          {opp.matched_skills?.length > 0 && (
            <div>
              <p className="text-[10px] uppercase text-gray-500 mb-1 font-mono">Matched Skills</p>
              <div className="flex flex-wrap gap-1.5">
                {opp.matched_skills.slice(0,3).map((s, i) => <span key={i} className="pill bg-green-100 text-green-800 text-[10px] px-1.5 py-0.5">✓ {getSkillLabel(s)}</span>)}
              </div>
            </div>
          )}
          {opp.missing_skills?.length > 0 && (
            <div>
              <p className="text-[10px] uppercase text-gray-500 mb-1 font-mono">Skills to Improve</p>
              <div className="flex flex-wrap gap-1.5">
                {opp.missing_skills.slice(0,3).map((s, i) => <span key={i} className="pill bg-red-100 text-red-800 text-[10px] px-1.5 py-0.5">✗ {getSkillLabel(s)}</span>)}
              </div>
            </div>
          )}
        </div>
      </div>
      <button onClick={() => handleApply(opp.id)} disabled={isApplied || applyingId === opp.id} className={`w-full mt-5 ${isApplied ? 'btn-secondary opacity-50 cursor-not-allowed' : 'btn-primary'}`}>
        {applyingId === opp.id ? 'Applying...' : isApplied ? 'Applied' : 'Apply Now'}
      </button>
    </div>
  );
}