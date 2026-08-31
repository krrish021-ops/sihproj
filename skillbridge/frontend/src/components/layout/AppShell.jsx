// AppShell — shared authenticated layout: top nav + role sidebar
import React from 'react'
import { useSelector } from 'react-redux'
import Navbar from '../common/Navbar'
import Sidebar from '../common/Sidebar'

const AppShell = ({ children }) => {
  const { user } = useSelector(state => state.auth)

  return (
    <div className="min-h-screen bg-paper">
      <Navbar />
      <div className="flex">
        {user?.role && <Sidebar role={user.role} />}
        <main className="flex-1 min-w-0">{children}</main>
      </div>
    </div>
  )
}

export default AppShell
