// Student Dashboard
import React from 'react'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import AppShell from '../components/layout/AppShell'

const actions = [
  { to: '/student/assessment', title: 'Take assessment', copy: 'Evaluate your skills' },
  { to: '/student/profile', title: 'Update profile', copy: 'Add your skills' },
  { to: '/student/recommendations', title: 'Recommendations', copy: 'View matches' },
]

const StudentDashboard = () => {
  const { user } = useSelector(state => state.auth)

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-8">
        <motion.h1
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-2xl font-display font-bold mb-8"
        >
          Welcome, {user?.full_name?.split(' ')[0]}
        </motion.h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {actions.map((a) => (
            <Link key={a.to} to={a.to} className="blueprint-card rounded-xl p-6 hover:-translate-y-0.5 transition-transform">
              <h3 className="font-display font-bold text-lg">{a.title}</h3>
              <p className="text-ink/60 text-sm mt-1">{a.copy}</p>
            </Link>
          ))}
        </div>
      </div>
    </AppShell>
  )
}

export default StudentDashboard
