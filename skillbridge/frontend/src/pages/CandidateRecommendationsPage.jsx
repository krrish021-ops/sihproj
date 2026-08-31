// Candidate Recommendations Page
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getCandidateRecommendations } from '../services/recruiterService'
import AppShell from '../components/layout/AppShell'
import LoadingSpinner from '../components/common/LoadingSpinner'
import CandidateCard from '../components/recruiter/CandidateCard'
import toast from 'react-hot-toast'

const CandidateRecommendationsPage = () => {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [decisions, setDecisions] = useState({})

  useEffect(() => {
    fetchCandidates()
  }, [id])

  const fetchCandidates = async () => {
    try {
      const response = await getCandidateRecommendations(id)
      setData(response)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleShortlist = (candidateId) => {
    setDecisions(prev => ({ ...prev, [candidateId]: 'shortlisted' }))
    toast.success('Candidate shortlisted')
  }

  const handleReject = (candidateId) => {
    setDecisions(prev => ({ ...prev, [candidateId]: 'rejected' }))
    toast('Candidate rejected', { icon: '✕' })
  }

  if (loading) return <AppShell><LoadingSpinner label="Ranking candidates…" /></AppShell>

  return (
    <AppShell>
      <div className="max-w-5xl mx-auto p-8">
        <h1 className="text-2xl font-display font-bold mb-8">Recommended candidates</h1>

        {data?.insights && (
          <div className="blueprint-card rounded-lg p-5 mb-8 grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-xl font-display font-bold">{data.insights.total_candidates}</p>
              <p className="metric-label uppercase">Total candidates</p>
            </div>
            <div>
              <p className="text-xl font-display font-bold text-success">{data.insights.shortlisted_count}</p>
              <p className="metric-label uppercase">Shortlisted</p>
            </div>
            <div>
              <p className="text-xl font-display font-bold text-blueprint">{data.insights.match_rate}%</p>
              <p className="metric-label uppercase">Match rate</p>
            </div>
          </div>
        )}

        {data?.ranked_candidates?.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {data.ranked_candidates.map(candidate => (
              <div key={candidate.id} className="relative">
                {decisions[candidate.id] && (
                  <span className={`absolute top-4 right-4 z-10 pill ${
                    decisions[candidate.id] === 'shortlisted' ? 'bg-success text-white' : 'bg-danger text-white'
                  }`}>
                    {decisions[candidate.id]}
                  </span>
                )}
                <CandidateCard candidate={candidate} onShortlist={handleShortlist} onReject={handleReject} />
              </div>
            ))}
          </div>
        ) : (
          <p className="text-ink/50 text-sm">No matching candidates yet.</p>
        )}
      </div>
    </AppShell>
  )
}

export default CandidateRecommendationsPage
