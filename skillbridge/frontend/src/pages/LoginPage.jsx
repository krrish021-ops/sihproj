// Login Page
import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { motion } from 'framer-motion'
import { login } from '../services/authService'
import { setUser, setToken } from '../store/slices/authSlice'
import toast from 'react-hot-toast'

const LoginPage = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const [formData, setFormData] = useState({ email: '', password: '', role: 'student' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await login(formData)
      dispatch(setUser(response.user))
      dispatch(setToken(response.access_token))
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      toast.success('Login successful!')

      if (response.user.role === 'student') navigate('/student/dashboard')
      else if (response.user.role === 'recruiter') navigate('/recruiter/dashboard')
      else navigate('/academician/dashboard')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed')
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
        <h2 className="text-2xl font-display font-bold text-center mb-6">Welcome back</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">I am a</label>
            <select name="role" value={formData.role} onChange={(e) => setFormData({...formData, role: e.target.value})} className="input">
              <option value="student">Student</option>
              <option value="recruiter">Recruiter</option>
              <option value="academician">Academician</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input type="email" name="email" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} className="input" required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input type="password" name="password" value={formData.password} onChange={(e) => setFormData({...formData, password: e.target.value})} className="input" required />
          </div>
          <button type="submit" disabled={loading} className="btn btn-primary w-full">
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
        <p className="text-center mt-4 text-sm text-ink/70">
          Don't have an account? <Link to="/signup" className="text-blueprint font-semibold">Sign up</Link>
        </p>
      </motion.div>
    </div>
  )
}

export default LoginPage
