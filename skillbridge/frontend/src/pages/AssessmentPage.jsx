import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { startAssessment, submitAnswer } from '../services/assessmentService';
import AppShell from '../components/layout/AppShell';
import toast from 'react-hot-toast';

export default function AssessmentPage() {
  const navigate = useNavigate();
  const userId = useSelector((state) => state.auth?.user?.id) || JSON.parse(localStorage.getItem('user') || '{}')?.id || 1;

  const [viewState, setViewState] = useState('intro');
  const [loading, setLoading] = useState(false);
  const [engineState, setEngineState] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [timeLeft, setTimeLeft] = useState(60);

  const handleStart = async () => {
    setLoading(true);
    try {
      const res = await startAssessment(userId);
      if (res && res.current_question) {
        setEngineState(res);
        setViewState('testing');
        setTimeLeft(60);
      }
    } catch (err) {
      toast.error('Failed to start assessment.');
    } finally { setLoading(false); }
  };

  useEffect(() => {
    let timer;
    if (viewState === 'testing' && timeLeft > 0 && !loading) {
      timer = setTimeout(() => setTimeLeft(prev => prev - 1), 1000);
    }
    return () => clearTimeout(timer);
  }, [viewState, timeLeft, loading]);

  const handleSubmit = async () => {
    if (!selectedOption) return toast.error('Please select an option.');
    setLoading(true);
    try {
      const res = await submitAnswer(engineState, selectedOption);
      if (res) {
        setEngineState(res);
        setSelectedOption('');
        setTimeLeft(60);
        if (res.status === 'completed') setViewState('completed');
      }
    } catch (err) {
      toast.error('Error submitting answer.');
    } finally { setLoading(false); }
  };

  const currQ = engineState?.current_question;
  const options = currQ?.options_array || [];
  const qNum = (engineState?.question_count || 0) + 1;

  return (
    <AppShell>
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        
        {viewState === 'intro' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="blueprint-card p-10 text-center max-w-2xl mx-auto mt-10">
            <h1 className="text-3xl font-bold font-['Space_Grotesk'] text-[#0E2A47] mb-4">Adaptive AI Assessment</h1>
            <p className="text-gray-600 mb-8">Prove your skills with 10 adaptive questions. Difficulty calibrates based on your answers to generate a verified skill report.</p>
            <button onClick={handleStart} disabled={loading} className="btn-cta text-lg px-8 py-3">
              {loading ? 'Initializing...' : 'Start Assessment'}
            </button>
          </motion.div>
        )}

        {viewState === 'testing' && currQ && (
          <div className="max-w-3xl mx-auto space-y-6 mt-6">
            <div className="flex justify-between items-center bg-white p-4 rounded shadow-sm border border-gray-100">
              <div className="flex items-center gap-3">
                <span className="font-mono text-sm font-bold text-[#0E2A47]">Question {qNum} of 10</span>
                <span className="pill bg-blue-100 text-blue-800 text-xs px-2 py-1">{currQ.skill}</span>
              </div>
              <div className={`font-mono font-bold ${timeLeft <= 10 ? 'text-[#C1443C] animate-pulse' : 'text-[#0E2A47]'}`}>
                ⏱ {timeLeft}s
              </div>
            </div>

            <div className="progress-track bg-gray-200 h-2 rounded-full w-full">
              <div className="progress-fill bg-[#D9A441] h-full rounded-full transition-all" style={{ width: `${(qNum/10)*100}%` }}></div>
            </div>

            <AnimatePresence mode="wait">
              <motion.div key={qNum} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="blueprint-card p-8">
                <h2 className="text-xl text-[#12202B] font-medium mb-6 leading-relaxed">{currQ.question}</h2>
                <div className="space-y-3">
                  {options.map((opt) => (
                    <button
                      key={opt.key}
                      onClick={() => setSelectedOption(opt.key)}
                      className={`w-full text-left p-4 rounded border-2 transition-all ${selectedOption === opt.key ? 'border-[#0E2A47] bg-[#0E2A47]/5 font-medium text-[#0E2A47]' : 'border-gray-200 hover:border-[#D9A441]/50 text-gray-700'}`}
                    >
                      <span className="uppercase font-mono mr-3 text-gray-400">{opt.key}.</span> {opt.text}
                    </button>
                  ))}
                </div>
                <div className="mt-8 pt-6 border-t border-gray-100 flex justify-end">
                  <button onClick={handleSubmit} disabled={loading || !selectedOption} className="btn-primary px-8">
                    {loading ? 'Evaluating...' : 'Submit Answer'}
                  </button>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        )}

        {viewState === 'completed' && (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="blueprint-card p-10 text-center max-w-2xl mx-auto mt-10">
            <div className="w-24 h-24 mx-auto border-4 border-[#0E2A47] rounded-full flex items-center justify-center mb-6">
              <span className="text-3xl font-bold text-[#0E2A47]">{engineState?.overall_score}%</span>
            </div>
            <h2 className="text-2xl font-bold font-['Space_Grotesk'] text-[#12202B] mb-2">Assessment Complete</h2>
            <p className="text-gray-600 mb-8">Your diagnostic report is ready and your skills have been verified.</p>
            
            <div className="bg-[#FBF9F4] p-6 rounded text-left mb-8 space-y-4">
              <h3 className="font-mono text-sm uppercase text-gray-500">Verified Proficiencies</h3>
              {Object.entries(engineState?.report?.skill_map || {}).map(([skill, data]) => {
                const prof = data.proficiency || data;
                return (
                  <div key={skill}>
                    <div className="flex justify-between text-sm mb-1"><span className="font-medium text-[#12202B]">{skill}</span><span className="font-mono text-[#0E2A47]">{prof}%</span></div>
                    <div className="progress-track bg-gray-200 h-1.5 rounded-full"><div className="progress-fill bg-[#3D8361] h-full rounded-full" style={{ width: `${prof}%` }}></div></div>
                  </div>
                );
              })}
            </div>

            <button onClick={() => navigate('/student/recommendations')} className="btn-cta w-full py-3 text-lg">
              View Verified Matches
            </button>
          </motion.div>
        )}

      </div>
    </AppShell>
  );
}