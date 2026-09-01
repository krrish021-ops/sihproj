import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem('user') || 'null');
  } catch (e) {}

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const isLanding = location.pathname === '/';

  return (
    <nav
      style={{
        background: isLanding ? 'transparent' : '#0E2A47',
        borderBottom: isLanding ? 'none' : '1px solid rgba(217,164,65,0.2)',
        padding: '14px 32px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
        <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#D9A441' }} />
        <span style={{ fontFamily: '"Space Grotesk", sans-serif', fontWeight: 700, fontSize: '18px', color: '#F1F5F9' }}>
          SkillBridge
        </span>
      </Link>

      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        {user && user.name ? (
          <>
            <span style={{ color: '#F1DBA3', fontSize: '13px', fontFamily: '"IBM Plex Mono", monospace' }}>
              {user.name.toUpperCase()}
            </span>
            <button onClick={handleLogout} className="btn btn-secondary" style={{ background: 'transparent', color: '#F1F5F9', borderColor: 'rgba(255,255,255,0.35)', fontSize: '13px', padding: '7px 14px' }}>
              Log out
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: '#F1F5F9', fontSize: '14px', textDecoration: 'none', fontWeight: 500 }}>
              Log in
            </Link>
            <Link to="/signup" className="btn btn-cta" style={{ padding: '8px 18px', fontSize: '14px' }}>
              Get started
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
