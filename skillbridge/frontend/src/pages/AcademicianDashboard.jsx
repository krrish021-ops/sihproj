import React from 'react'
import { useSelector } from 'react-redux'
import AppShell from '../components/layout/AppShell'

const AcademicianDashboard = () => {
  const { user } = useSelector(state => state.auth)

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-8">
        <h1 className="text-2xl font-display font-bold mb-2">Academician dashboard</h1>
        <p className="text-ink/60">Welcome, {user?.full_name}</p>
      </div>
    </AppShell>
  )
}

export default AcademicianDashboard
