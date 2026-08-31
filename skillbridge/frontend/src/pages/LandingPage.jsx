// Landing Page
import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'

const features = [
  {
    title: 'AI assessment',
    copy: 'Adaptive, question-by-question assessments that adjust difficulty to what you actually know.',
  },
  {
    title: 'Skill mapping',
    copy: 'A clear, scored breakdown of your strengths and gaps across every skill you list.',
  },
  {
    title: 'Career matching',
    copy: 'Ranked internships, jobs, courses, and projects matched against your live skill map.',
  },
]

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-paper">
      <nav className="bg-blueprint">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <span className="flex items-center gap-2 text-white font-display font-bold text-xl">
            <span className="w-2 h-2 rounded-full bg-gold" />
            SkillBridge
          </span>
          <div className="flex gap-3 items-center">
            <Link to="/login" className="text-white/80 hover:text-white text-sm font-medium">Log in</Link>
            <Link to="/signup" className="btn btn-cta text-sm py-2.5 px-5">Get started</Link>
          </div>
        </div>
      </nav>

      <section className="blueprint-surface py-24 md:py-32 relative overflow-hidden">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-left relative">
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl md:text-6xl font-display font-bold text-white leading-tight max-w-3xl"
          >
            Prove your skills.
            <br />Not just your resume.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-lg text-blueprint-100 mt-6 max-w-xl"
          >
            SkillBridge assesses what you can actually do, maps your skill gaps, and
            connects you to internships, jobs, courses, and projects worth your time.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-8"
          >
            <Link to="/signup" className="btn btn-cta text-base">
              Start your assessment
            </Link>
          </motion.div>
        </div>
      </section>

      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl md:text-3xl font-display font-bold mb-12 max-w-xl">
            Built for students, recruiters, and academicians who want signal over noise.
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((f) => (
              <div key={f.title} className="blueprint-card rounded-lg p-6">
                <h3 className="font-display font-bold text-lg mb-2">{f.title}</h3>
                <p className="text-ink/65 text-sm leading-relaxed">{f.copy}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default LandingPage
