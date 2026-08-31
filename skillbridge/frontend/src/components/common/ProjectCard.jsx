// Project Card Component
import React from 'react'
import { motion } from 'framer-motion'

const ProjectCard = ({ project }) => {
  return (
    <motion.div
      whileHover={{ y: -3 }}
      className="blueprint-card rounded-lg overflow-hidden cursor-pointer"
    >
      <div className="bg-blueprint-surface blueprint-surface h-24 flex items-center justify-center">
        <span className="metric-label text-gold uppercase">Project</span>
      </div>
      <div className="p-4">
        <h3 className="font-display font-bold text-base mb-1">{project.title}</h3>
        {project.description && (
          <p className="text-sm text-ink/60 mb-3 line-clamp-2">{project.description}</p>
        )}

        {project.skills_taught?.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-3">
            {project.skills_taught.map((skill, i) => (
              <span key={i} className="pill bg-blueprint-50 text-blueprint">{skill}</span>
            ))}
          </div>
        )}

        <div className="flex justify-between items-center text-xs text-ink/50 mb-3">
          <span>{project.difficulty || 'Beginner'}</span>
          <span>{project.estimated_hours || 10} hrs</span>
        </div>

        <button className="btn btn-secondary w-full text-sm">Start project</button>
      </div>
    </motion.div>
  )
}

export default ProjectCard
