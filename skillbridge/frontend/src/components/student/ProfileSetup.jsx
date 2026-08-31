// Profile Setup Component
import React, { useState } from 'react'
import { motion } from 'framer-motion'

const ProfileSetup = ({ initialData, onSave }) => {
  const [formData, setFormData] = useState({
    phone: initialData?.phone || '',
    location: initialData?.location || '',
    bio: initialData?.bio || '',
    education: initialData?.education || '',
    institution: initialData?.institution || '',
    linkedin_url: initialData?.linkedin_url || '',
    portfolio_url: initialData?.portfolio_url || ''
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave?.(formData)
  }

  return (
    <motion.form
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      onSubmit={handleSubmit}
      className="blueprint-card rounded-xl p-8 space-y-6"
    >
      <div>
        <h2 className="text-xl font-display font-bold">Complete your profile</h2>
        <p className="text-ink/60 text-sm mt-1">
          This information helps us match you with better opportunities
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-semibold mb-2">Phone number</label>
          <input type="tel" name="phone" value={formData.phone} onChange={handleChange} className="input" placeholder="+91 98765 43210" />
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Location</label>
          <input type="text" name="location" value={formData.location} onChange={handleChange} className="input" placeholder="City, State" />
        </div>
      </div>

      <div>
        <label className="block text-sm font-semibold mb-2">Bio</label>
        <textarea name="bio" value={formData.bio} onChange={handleChange} className="input" rows="3" placeholder="Tell us about yourself..." />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-semibold mb-2">Education</label>
          <input type="text" name="education" value={formData.education} onChange={handleChange} className="input" placeholder="e.g., B.Tech Computer Science" />
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Institution</label>
          <input type="text" name="institution" value={formData.institution} onChange={handleChange} className="input" placeholder="e.g., IIT Delhi" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-semibold mb-2">LinkedIn URL</label>
          <input type="url" name="linkedin_url" value={formData.linkedin_url} onChange={handleChange} className="input" placeholder="https://linkedin.com/in/username" />
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Portfolio URL</label>
          <input type="url" name="portfolio_url" value={formData.portfolio_url} onChange={handleChange} className="input" placeholder="https://yourportfolio.com" />
        </div>
      </div>

      <button type="submit" className="btn btn-primary w-full">
        Save profile
      </button>
    </motion.form>
  )
}

export default ProfileSetup
