import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import './Navbar.css'

const NAV_ITEMS = [
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/recommendations', label: 'Careers' },
  { path: '/skill-gap', label: 'Skill Gap' },
  { path: '/roadmap', label: 'Roadmap' },
  { path: '/comparison', label: 'Compare' },
  { path: '/chat', label: 'AI Chat' },
  { path: '/progress', label: 'Progress' },
]

export default function Navbar() {
  const { profile } = useApp()
  const location = useLocation()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <nav className="navbar">
      <div className="navbar-inner container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🚀</span>
          <span className="brand-name">CareerPilot <span className="brand-ai">AI</span></span>
        </Link>

        <button className="nav-toggle" onClick={() => setMenuOpen(v => !v)} aria-label="Menu">
          <span /><span /><span />
        </button>

        <ul className={`nav-links ${menuOpen ? 'open' : ''}`}>
          {NAV_ITEMS.map(item => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>

        <div className="nav-actions">
          {profile ? (
            <div className="nav-user">
              <div className="avatar">{profile.name?.[0]?.toUpperCase() || 'S'}</div>
              <span className="nav-username">{profile.name}</span>
            </div>
          ) : (
            <button className="btn btn-primary btn-sm" onClick={() => navigate('/assessment')}>
              Start Assessment
            </button>
          )}
        </div>
      </div>
    </nav>
  )
}
