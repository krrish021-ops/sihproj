import React from 'react';

export default function LoadingSpinner({ label = 'Loading…' }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 20px' }}>
      <div
        style={{
          width: 40,
          height: 40,
          border: '3px solid rgba(14,42,71,0.15)',
          borderTop: '3px solid #0E2A47',
          borderRadius: '50%',
          animation: 'spin 0.9s linear infinite',
        }}
      />
      <div className="metric-label" style={{ marginTop: 14 }}>{label}</div>
      <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
