// Navbar Component
import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { logout } from '../../store/slices/authSlice'

const Navbar = () => {
  const { user } = useSelector(state => state.auth)
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <nav className="bg-blueprint border-b border-blueprint-line/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link to="/" className="flex items-center gap-2 text-white font-display font-bold text-xl tracking-tight">
            <span className="w-2 h-2 rounded-full bg-gold" />
            SkillBridge
          </Link>

          <div className="flex items-center gap-4">
            {user ? (
              <>
                <span className="hidden sm:inline text-blueprint-100 text-sm">{user.full_name}</span>
                <button onClick={handleLogout} className="btn btn-secondary !border-blueprint-line !text-white text-sm py-2 px-4">
                  Log out
                </button>
              </>
            ) : (
              <Link to="/login" className="text-white/80 hover:text-white text-sm font-medium">
                Log in
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
