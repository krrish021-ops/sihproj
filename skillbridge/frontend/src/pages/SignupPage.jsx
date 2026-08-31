// Signup Page
import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { register } from '../services/authService'
import toast from 'react-hot-toast'

const SignupPage = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '', password: '', full_name: '', role: 'student'
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await register(formData)
      toast.success('Account created! Please log in.')
      navigate('/login')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen blueprint-surface flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-xl p-8 w-full max-w-md"
      >
        <h2 className="text-2xl font-display font-bold text-center mb-6">Create account</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Full name</label>
            <input type="text" value={formData.full_name} onChange={(e) => setFormData({...formData, full_name: e.target.value})} className="input" required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input type="email" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} className="input" required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input type="password" value={formData.password} onChange={(e) => setFormData({...formData, password: e.target.value})} className="input" required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Join as</label>
            <select value={formData.role} onChange={(e) => setFormData({...formData, role: e.target.value})} className="input">
              <option value="student">Student</option>
              <option value="recruiter">Recruiter</option>
              <option value="academician">Academician</option>
            </select>
          </div>
          <button type="submit" disabled={loading} className="btn btn-primary w-full">
            {loading ? 'Creating…' : 'Create account'}
          </button>
        </form>
        <p className="text-center mt-4 text-sm text-ink/70">
          Already have an account? <Link to="/login" className="text-blueprint font-semibold">Sign in</Link>
        </p>
      </motion.div>
    </div>
  )
}

export default SignupPage
