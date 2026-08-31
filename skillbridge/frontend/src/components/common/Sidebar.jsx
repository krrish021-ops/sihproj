// Sidebar Component
import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const Sidebar = ({ role }) => {
  const location = useLocation()

  const menuItems = {
    student: [
      { path: '/student/dashboard', label: 'Dashboard' },
      { path: '/student/assessment', label: 'Assessment' },
      { path: '/student/profile', label: 'Profile' },
      { path: '/student/recommendations', label: 'Recommendations' },
    ],
    recruiter: [
      { path: '/recruiter/dashboard', label: 'Dashboard' },
      { path: '/recruiter/post-opportunity', label: 'Post Opportunity' },
    ],
    academician: [
      { path: '/academician/dashboard', label: 'Dashboard' },
    ],
  }

  return (
    <aside className="w-56 shrink-0 bg-white border-r border-blueprint/10 min-h-[calc(100vh-4rem)]">
      <nav className="p-3">
        <p className="metric-label px-3 pt-2 pb-3 uppercase">Menu</p>
        {menuItems[role]?.map(item => {
          const active = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`relative flex items-center px-3 py-2.5 rounded-md mb-1 text-sm font-medium transition-colors ${
                active
                  ? 'bg-blueprint-50 text-blueprint'
                  : 'text-ink/70 hover:bg-blueprint-50 hover:text-blueprint'
              }`}
            >
              {active && <span className="absolute left-0 top-1/2 -translate-y-1/2 h-5 w-0.5 bg-gold rounded-full" />}
              {item.label}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}

export default Sidebar
