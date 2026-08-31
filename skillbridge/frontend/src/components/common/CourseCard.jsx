// Course Card Component
import React from 'react'
import { motion } from 'framer-motion'

const CourseCard = ({ course }) => {
  return (
    <motion.div
      whileHover={{ y: -3 }}
      className="blueprint-card rounded-lg overflow-hidden cursor-pointer"
    >
      <div className="bg-blueprint-surface blueprint-surface h-24 flex items-center justify-center">
        <span className="metric-label text-gold uppercase">Course</span>
      </div>
      <div className="p-4">
        <h3 className="font-display font-bold text-base mb-1 line-clamp-2">{course.title}</h3>
        <p className="text-sm text-ink/60 mb-2">{course.provider || course.instructor}</p>

        {course.rating && (
          <div className="flex items-center gap-2 mb-2">
            <span className="text-gold">★</span>
            <span className="font-semibold text-sm">{course.rating}</span>
            {course.enrollment_count && (
              <span className="text-ink/40 text-xs">({course.enrollment_count.toLocaleString()})</span>
            )}
          </div>
        )}

        {course.match_score !== undefined && (
          <div className="mb-3">
            <div className="flex justify-between text-xs mb-1">
              <span className="text-ink/50">Match</span>
              <span className="font-semibold text-success">{course.match_score}%</span>
            </div>
            <div className="progress-track">
              <div className="h-full bg-success rounded" style={{ width: `${course.match_score}%` }} />
            </div>
          </div>
        )}

        <div className="flex items-center justify-between mt-3">
          {course.price !== undefined && <span className="font-display font-bold text-lg">₹{course.price}</span>}
          <button className="btn btn-primary text-xs py-2 px-3 ml-auto">Enroll</button>
        </div>
      </div>
    </motion.div>
  )
}

export default CourseCard
