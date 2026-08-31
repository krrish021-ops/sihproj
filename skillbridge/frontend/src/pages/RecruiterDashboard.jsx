import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { getRecruiterDashboard } from '../services/recruiterService'
import AppShell from '../components/layout/AppShell'
import LoadingSpinner from '../components/common/LoadingSpinner'

const RecruiterDashboard = () => {
  const { user } = useSelector(state => state.auth)
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboard()
  }, [])

  const fetchDashboard = async () => {
    try {
      const data = await getRecruiterDashboard(user.id)
      setDashboard(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <AppShell><LoadingSpinner label="Loading dashboard…" /></AppShell>

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-display font-bold">Recruiter dashboard</h1>
            <p className="text-ink/60 text-sm mt-1">{dashboard?.company_name || 'Company'}</p>
          </div>
          <Link to="/recruiter/post-opportunity" className="btn btn-cta text-sm">
            + Post opportunity
          </Link>
        </div>

        {dashboard?.opportunities?.length > 0 ? (
          <div className="space-y-4">
            {dashboard.opportunities.map(opp => (
              <div key={opp.id} className="blueprint-card rounded-xl p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="text-lg font-display font-bold">{opp.title}</h3>
                    <span className="metric-label uppercase">{opp.type}</span>
                  </div>
                  <Link to={`/recruiter/candidates/${opp.id}`} className="btn btn-primary text-sm">
                    View candidates
                  </Link>
                </div>
                <div className="grid grid-cols-3 gap-4 mt-5 text-center">
                  <div>
                    <p className="text-xl font-display font-bold">{opp.total_applications}</p>
                    <p className="metric-label uppercase">Applications</p>
                  </div>
                  <div>
                    <p className="text-xl font-display font-bold text-success">{opp.shortlisted_count}</p>
                    <p className="metric-label uppercase">Shortlisted</p>
                  </div>
                  <div>
                    <p className="text-xl font-display font-bold text-danger">{opp.rejected_count}</p>
                    <p className="metric-label uppercase">Rejected</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-ink/50 text-sm">No opportunities posted yet.</p>
        )}
      </div>
    </AppShell>
  )
}

export default RecruiterDashboard
