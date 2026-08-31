// Post Opportunity Component
import React, { useState } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

const PostOpportunity = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    type: 'internship',
    required_skills: [],
    location: '',
    stipend: '',
    duration: ''
  })
  const [skillInput, setSkillInput] = useState('')
  const [skillProficiency, setSkillProficiency] = useState(50)

  const addSkill = () => {
    if (skillInput.trim()) {
      setFormData({
        ...formData,
        required_skills: [
          ...formData.required_skills,
          { skill: skillInput.trim(), proficiency: skillProficiency }
        ]
      })
      setSkillInput('')
      setSkillProficiency(50)
    }
  }

  const removeSkill = (index) => {
    setFormData({
      ...formData,
      required_skills: formData.required_skills.filter((_, i) => i !== index)
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (formData.required_skills.length === 0) {
      toast.error('Add at least one required skill')
      return
    }
    onSubmit?.(formData)
  }

  return (
    <motion.form
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      onSubmit={handleSubmit}
      className="blueprint-card rounded-xl p-8 space-y-6"
    >
      <div>
        <h2 className="text-xl font-display font-bold mb-1">Post new opportunity</h2>
        <p className="text-ink/60 text-sm">Reach students whose verified skills match what you need</p>
      </div>

      <div>
        <label className="block text-sm font-semibold mb-2">Position title *</label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({...formData, title: e.target.value})}
          className="input"
          placeholder="e.g., Frontend Developer Intern"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-semibold mb-2">Description *</label>
        <textarea
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          className="input"
          rows="5"
          placeholder="Describe the role, responsibilities, and expectations..."
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-semibold mb-2">Type *</label>
          <select
            value={formData.type}
            onChange={(e) => setFormData({...formData, type: e.target.value})}
            className="input"
          >
            <option value="internship">Internship</option>
            <option value="job">Full-time job</option>
            <option value="project">Project-based</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Location</label>
          <input
            type="text"
            value={formData.location}
            onChange={(e) => setFormData({...formData, location: e.target.value})}
            className="input"
            placeholder="e.g., Bengaluru / Remote"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-semibold mb-2">Stipend/Salary</label>
          <input
            type="text"
            value={formData.stipend}
            onChange={(e) => setFormData({...formData, stipend: e.target.value})}
            className="input"
            placeholder="e.g., ₹25,000/month"
          />
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Duration</label>
          <input
            type="text"
            value={formData.duration}
            onChange={(e) => setFormData({...formData, duration: e.target.value})}
            className="input"
            placeholder="e.g., 3 months"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-semibold mb-2">Required skills *</label>
        <div className="flex gap-2 mb-3">
          <input
            type="text"
            value={skillInput}
            onChange={(e) => setSkillInput(e.target.value)}
            className="input flex-1"
            placeholder="e.g., Python"
          />
          <input
            type="number"
            value={skillProficiency}
            onChange={(e) => setSkillProficiency(e.target.value)}
            className="input w-24"
            min="0"
            max="100"
            placeholder="%"
          />
          <button type="button" onClick={addSkill} className="btn btn-secondary text-sm">
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.required_skills.map((skill, index) => (
            <span key={index} className="pill bg-blueprint-50 text-blueprint">
              {skill.skill} ({skill.proficiency}%)
              <button type="button" onClick={() => removeSkill(index)} className="text-danger hover:opacity-70 ml-1">
                ✕
              </button>
            </span>
          ))}
        </div>
      </div>

      <button type="submit" className="btn btn-cta w-full">
        Post opportunity
      </button>
    </motion.form>
  )
}

export default PostOpportunity
