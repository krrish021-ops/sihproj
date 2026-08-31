// Profile Page
import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { motion } from 'framer-motion'
import { getStudentProfile, updateStudentProfile, addSkills } from '../services/studentService'
import AppShell from '../components/layout/AppShell'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ProfileSetup from '../components/student/ProfileSetup'
import SkillEntry from '../components/student/SkillEntry'
import toast from 'react-hot-toast'

const ProfilePage = () => {
  const { user } = useSelector(state => state.auth)
  const [profile, setProfile] = useState({})
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const data = await getStudentProfile(user.id)
      setProfile(data.profile)
      setSkills(data.skills)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleProfileSave = async (formData) => {
    try {
      await updateStudentProfile(user.id, formData)
      toast.success('Profile updated!')
      fetchProfile()
    } catch (error) {
      toast.error('Failed to update profile')
    }
  }

  const handleSkillsSave = async ({ skills: newSkills, projects }) => {
    try {
      await addSkills(user.id, { skills: newSkills, projects })
      toast.success('Skills added!')
      fetchProfile()
    } catch (error) {
      toast.error('Failed to add skills')
    }
  }

  if (loading) return <AppShell><LoadingSpinner label="Loading profile…" /></AppShell>

  return (
    <AppShell>
      <div className="max-w-2xl mx-auto p-8 space-y-8">
        <div>
          <h1 className="text-2xl font-display font-bold mb-1">Your profile</h1>
          <p className="text-ink/60 text-sm">
            {profile.full_name} · {profile.email}
          </p>
        </div>

        {skills.length > 0 && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="blueprint-card rounded-xl p-6">
            <h2 className="text-lg font-display font-bold mb-4">Current skills</h2>
            <div className="flex flex-wrap gap-2">
              {skills.map((skill, i) => (
                <span key={i} className="pill bg-blueprint-50 text-blueprint">
                  {skill.skill_name} · {skill.proficiency}%
                </span>
              ))}
            </div>
          </motion.div>
        )}

        <ProfileSetup initialData={profile} onSave={handleProfileSave} />
        <SkillEntry onSave={handleSkillsSave} />
      </div>
    </AppShell>
  )
}

export default ProfilePage
