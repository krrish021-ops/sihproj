// Skill Report Component
import React from 'react'
import { motion } from 'framer-motion'

const SkillReport = ({ report }) => {
  if (!report) return null

  const getSkillColor = (proficiency) => {
    if (proficiency >= 70) return 'bg-success'
    if (proficiency >= 50) return 'bg-gold'
    return 'bg-danger'
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      className="blueprint-card rounded-2xl p-8"
    >
      <div className="text-center mb-8">
        <h2 className="text-2xl font-display font-bold text-ink">Skill assessment report</h2>
        <p className="text-ink/60 mt-2">Here's your comprehensive skill analysis</p>
      </div>

      {/* Overall Score */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-32 h-32 rounded-full border-4 border-blueprint">
          <div>
            <p className="text-4xl font-display font-bold text-blueprint">{report.overall_score}%</p>
            <p className="metric-label uppercase mt-1">Overall score</p>
          </div>
        </div>
      </div>

      {/* Skill Breakdown */}
      <div className="mb-8">
        <h3 className="text-lg font-display font-bold mb-4">Skill breakdown</h3>
        <div className="space-y-4">
          {Object.entries(report.skills || {}).map(([skill, data]) => (
            <div key={skill}>
              <div className="flex justify-between mb-1">
                <span className="font-medium text-sm">{skill}</span>
                <span className="text-ink/60 text-sm">{data.proficiency}%</span>
              </div>
              <div className="progress-track">
                <div
                  className={`h-full rounded ${getSkillColor(data.proficiency)}`}
                  style={{ width: `${data.proficiency}%` }}
                />
              </div>
              <div className="flex justify-between mt-1">
                <span className="metric-label">
                  Confidence {Math.round((data.confidence || 0) * 100)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Strengths and Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="bg-success/5 border border-success/20 rounded-lg p-4">
          <h4 className="font-display font-bold text-success mb-2 text-sm uppercase tracking-wide">Strengths</h4>
          {report.strengths?.length > 0 ? (
            <ul className="list-disc list-inside text-success/90 text-sm space-y-1">
              {report.strengths.map((strength, i) => (
                <li key={i}>{strength}</li>
              ))}
            </ul>
          ) : (
            <p className="text-success/80 text-sm">Keep working on building your strengths!</p>
          )}
        </div>
        <div className="bg-danger/5 border border-danger/20 rounded-lg p-4">
          <h4 className="font-display font-bold text-danger mb-2 text-sm uppercase tracking-wide">Areas to improve</h4>
          {report.weaknesses?.length > 0 ? (
            <ul className="list-disc list-inside text-danger/90 text-sm space-y-1">
              {report.weaknesses.map((weakness, i) => (
                <li key={i}>{weakness}</li>
              ))}
            </ul>
          ) : (
            <p className="text-danger/80 text-sm">No major weaknesses identified!</p>
          )}
        </div>
      </div>

      {/* Recommendations */}
      {report.recommendations?.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-display font-bold mb-4">Recommendations</h3>
          <div className="space-y-3">
            {report.recommendations.map((rec, i) => (
              <div key={i} className="bg-blueprint-50 rounded-lg p-4">
                <p className="font-semibold text-blueprint text-sm">{rec.skill}</p>
                <p className="text-blueprint/80 text-sm mt-1">{rec.action}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={() => window.location.href = '/student/recommendations'}
        className="btn btn-primary w-full"
      >
        View personalized recommendations
      </button>
    </motion.div>
  )
}

export default SkillReport
