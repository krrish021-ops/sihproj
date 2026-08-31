// Protected Route Component
import React from 'react'
import { Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'

const ProtectedRoute = ({ children, role }) => {
  const { user, token } = useSelector(state => state.auth)

  if (!token || !user) {
    return <Navigate to="/login" replace />
  }

  if (role && user.role !== role) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute