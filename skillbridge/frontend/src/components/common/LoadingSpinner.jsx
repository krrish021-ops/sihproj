// Loading Spinner Component
import React from 'react'

const LoadingSpinner = ({ label = 'Loading...' }) => {
  return (
    <div className="min-h-[60vh] flex items-center justify-center bg-paper">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-[3px] border-blueprint/15 border-t-blueprint mx-auto" />
        <p className="mt-4 metric-label">{label}</p>
      </div>
    </div>
  )
}

export default LoadingSpinner
