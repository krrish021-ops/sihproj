// Post Opportunity Page
import React from 'react'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { postOpportunity } from '../services/recruiterService'
import AppShell from '../components/layout/AppShell'
import PostOpportunity from '../components/recruiter/PostOpportunity'
import toast from 'react-hot-toast'

const PostOpportunityPage = () => {
  const { user } = useSelector(state => state.auth)
  const navigate = useNavigate()

  const handleSubmit = async (formData) => {
    try {
      await postOpportunity(user.id, formData)
      toast.success('Opportunity posted!')
      navigate('/recruiter/dashboard')
    } catch (error) {
      toast.error('Failed to post')
    }
  }

  return (
    <AppShell>
      <div className="max-w-2xl mx-auto p-8">
        <PostOpportunity onSubmit={handleSubmit} />
      </div>
    </AppShell>
  )
}

export default PostOpportunityPage
