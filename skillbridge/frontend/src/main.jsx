import React from 'react';
import ReactDOM from 'react-dom/client';
import { Toaster } from 'react-hot-toast';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
    <Toaster
      position="top-right"
      toastOptions={{
        style: {
          background: '#0E2A47',
          color: '#F1F5F9',
          fontFamily: 'Inter, sans-serif',
          fontSize: 13,
          border: '1px solid rgba(217,164,65,0.3)',
        },
      }}
    />
  </React.StrictMode>
);
