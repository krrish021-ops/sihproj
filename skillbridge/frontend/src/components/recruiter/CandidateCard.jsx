// Candidate Card Component
import React from 'react'
import { motion } from 'framer-motion'

const CandidateCard = ({ candidate, onShortlist, onReject }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="blueprint-card rounded-xl p-6"
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-blueprint rounded-full flex items-center justify-center text-white font-display font-bold text-lg">
            {candidate.name?.charAt(0) || '?'}
          </div>
          <div>
            <h3 className="font-display font-bold text-base">{candidate.name}</h3>
            <p className="text-sm text-ink/60">{candidate.email}</p>
          </div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-display font-bold text-success">{candidate.match_score}%</div>
          <p className="metric-label uppercase">Match</p>
        </div>
      </div>

      {candidate.education && (
        <p className="text-sm text-ink/60 mb-3">🎓 {candidate.education}</p>
      )}

      <div className="mb-4">
        <p className="metric-label uppercase mb-1.5">Skills</p>
        <div className="flex flex-wrap gap-1.5">
          {candidate.skills?.map((skill, i) => (
            <span key={i} className="pill bg-blueprint-50 text-blueprint">
              {skill.skill_name}: {skill.proficiency}%
            </span>
          ))}
        </div>
      </div>

      {candidate.matched_skills?.length > 0 && (
        <div className="mb-3">
          <p className="metric-label uppercase text-success mb-1.5">Matched skills</p>
          <div className="flex flex-wrap gap-1.5">
            {candidate.matched_skills.map((skill, i) => (
              <span key={i} className="pill bg-success/10 text-success">{skill}</span>
            ))}
          </div>
        </div>
      )}

      {candidate.missing_skills?.length > 0 && (
        <div className="mb-4">
          <p className="metric-label uppercase text-danger mb-1.5">Missing skills</p>
          <div className="flex flex-wrap gap-1.5">
            {candidate.missing_skills.map((skill, i) => (
              <span key={i} className="pill bg-danger/10 text-danger">{skill}</span>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-2">
        <button onClick={() => onShortlist?.(candidate.id)} className="btn btn-primary flex-1 text-sm">
          Shortlist
        </button>
        <button onClick={() => onReject?.(candidate.id)} className="btn btn-danger flex-1 text-sm">
          Reject
        </button>
      </div>
    </motion.div>
  )
}

export default CandidateCard
