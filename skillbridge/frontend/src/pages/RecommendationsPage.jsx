// Recommendations Page
import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import { getRecommendations, applyToOpportunity } from '../services/studentService'
import AppShell from '../components/layout/AppShell'
import LoadingSpinner from '../components/common/LoadingSpinner'
import CourseCard from '../components/common/CourseCard'
import InternshipCard from '../components/common/InternshipCard'
import ProjectCard from '../components/common/ProjectCard'
import toast from 'react-hot-toast'

const RecommendationsPage = () => {
  const { user } = useSelector(state => state.auth)
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchRecommendations = async () => {
    try {
      const data = await getRecommendations(user.id)
      setRecommendations(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApply = async (opportunity) => {
    try {
      await applyToOpportunity(opportunity.id, user.id)
      toast.success(`Applied to ${opportunity.title}`)
    } catch (error) {
      toast.error('Failed to apply')
    }
  }

  if (loading) return <AppShell><LoadingSpinner label="Finding your matches…" /></AppShell>

  return (
    <AppShell>
      <div className="max-w-6xl mx-auto p-8">
        <h1 className="text-2xl font-display font-bold mb-8">Your recommendations</h1>

        {recommendations?.skill_gaps?.length > 0 && (
          <div className="bg-gold-light/40 border border-gold/30 rounded-lg p-4 mb-8">
            <p className="font-display font-bold text-sm mb-2">Skill gaps to close</p>
            <div className="flex flex-wrap gap-2">
              {recommendations.skill_gaps.map(skill => (
                <span key={skill} className="pill bg-white text-gold-dark border border-gold/40">{skill}</span>
              ))}
            </div>
          </div>
        )}

        <div className="space-y-10">
          {recommendations?.courses?.length > 0 && (
            <div>
              <h2 className="text-lg font-display font-bold mb-4">Courses</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {recommendations.courses.map(course => (
                  <CourseCard key={course.id} course={course} />
                ))}
              </div>
            </div>
          )}

          {recommendations?.internships?.length > 0 && (
            <div>
              <h2 className="text-lg font-display font-bold mb-4">Internships</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {recommendations.internships.map(intern => (
                  <InternshipCard key={intern.id} internship={intern} onApply={handleApply} />
                ))}
              </div>
            </div>
          )}

          {recommendations?.jobs?.length > 0 && (
            <div>
              <h2 className="text-lg font-display font-bold mb-4">Jobs</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {recommendations.jobs.map(job => (
                  <InternshipCard key={job.id} internship={job} onApply={handleApply} />
                ))}
              </div>
            </div>
          )}

          {recommendations?.projects?.length > 0 && (
            <div>
              <h2 className="text-lg font-display font-bold mb-4">Projects</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {recommendations.projects.map(project => (
                  <ProjectCard key={project.id} project={project} />
                ))}
              </div>
            </div>
          )}

          {recommendations &&
            !recommendations.courses?.length &&
            !recommendations.internships?.length &&
            !recommendations.jobs?.length &&
            !recommendations.projects?.length && (
            <p className="text-ink/50 text-sm">
              No matches yet — complete an assessment to get personalized recommendations.
            </p>
          )}
        </div>
      </div>
    </AppShell>
  )
}

export default RecommendationsPage
