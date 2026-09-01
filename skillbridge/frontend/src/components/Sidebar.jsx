import React from 'react';
import { NavLink } from 'react-router-dom';

const linksByRole = {
  student: [
    { to: '/student/dashboard', label: 'Dashboard' },
    { to: '/student/assessment', label: 'Assessment' },
    { to: '/student/profile', label: 'Profile' },
    { to: '/student/recommendations', label: 'Recommendations' },
  ],
  recruiter: [
    { to: '/recruiter/dashboard', label: 'Dashboard' },
    { to: '/recruiter/post-opportunity', label: 'Post opportunity' },
  ],
  academician: [
    { to: '/academician/dashboard', label: 'Analytics' },
  ],
};

export default function Sidebar() {
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem('user') || 'null');
  } catch (e) {}
  const role = user?.role || 'student';
  const links = linksByRole[role] || linksByRole.student;

  return (
    <aside
      style={{
        width: 224,
        minHeight: 'calc(100vh - 60px)',
        background: '#ffffff',
        borderRight: '1px solid rgba(14, 42, 71, 0.08)',
        padding: '28px 0',
      }}
    >
      <div className="metric-label" style={{ padding: '0 28px 12px', color: '#2F5C86' }}>MENU</div>
      <nav>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              padding: '10px 28px',
              fontSize: '14px',
              color: isActive ? '#0E2A47' : '#12202B',
              background: isActive ? '#EEF3F9' : 'transparent',
              borderLeft: isActive ? '3px solid #D9A441' : '3px solid transparent',
              fontWeight: isActive ? 600 : 400,
              textDecoration: 'none',
              transition: 'all 0.15s ease',
            })}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
