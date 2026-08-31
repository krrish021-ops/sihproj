// Internship Card Component
import React from 'react'
import { motion } from 'framer-motion'

const InternshipCard = ({ internship, onApply }) => {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      className="blueprint-card rounded-lg p-5"
    >
      <div className="flex justify-between items-start mb-3 gap-3">
        <div>
          <h3 className="font-display font-bold text-base text-ink">{internship.title}</h3>
          <p className="text-sm text-ink/60">{internship.company}</p>
        </div>
        {internship.match_score !== undefined && (
          <span className="pill bg-success/10 text-success shrink-0">{internship.match_score}% match</span>
        )}
      </div>

      <div className="space-y-1.5 mb-4 text-sm text-ink/70">
        {internship.location && <p>📍 {internship.location}</p>}
        {internship.stipend && <p>💰 {internship.stipend}</p>}
        {internship.duration && <p>⏱ {internship.duration}</p>}
      </div>

      {internship.matched_skills?.length > 0 && (
        <div className="mb-3">
          <p className="metric-label uppercase mb-1.5">Matched skills</p>
          <div className="flex flex-wrap gap-1.5">
            {internship.matched_skills.map((skill, i) => (
              <span key={i} className="pill bg-success/10 text-success">✓ {skill}</span>
            ))}
          </div>
        </div>
      )}

      {internship.missing_skills?.length > 0 && (
        <div className="mb-4">
          <p className="metric-label uppercase mb-1.5">Skills to improve</p>
          <div className="flex flex-wrap gap-1.5">
            {internship.missing_skills.map((skill, i) => (
              <span key={i} className="pill bg-danger/10 text-danger">✗ {skill}</span>
            ))}
          </div>
        </div>
      )}

      <button onClick={() => onApply?.(internship)} className="btn btn-primary w-full text-sm">Apply now</button>
    </motion.div>
  )
}

export default InternshipCard
