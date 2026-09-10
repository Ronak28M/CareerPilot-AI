import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import './CareerRoadmap.css'

const PHASE_LABELS = {
  phase_1: { label: 'Phase 1', period: '0–3 Months', color: '#3b82d4', bg: '#eff6ff' },
  phase_2: { label: 'Phase 2', period: '3–6 Months', color: '#7c5cd8', bg: '#f5f3ff' },
  phase_3: { label: 'Phase 3', period: '6–12 Months', color: '#10b981', bg: '#f0fdf4' },
}

export default function CareerRoadmap() {
  const { analysisResult, progressData, profile } = useApp()
  const navigate = useNavigate()
  const [activePhase, setActivePhase] = useState('phase_1')

  if (!analysisResult) {
    return (
      <div className="page-content">
        <div className="empty-state">
          <div style={{ fontSize: 56 }}>🗺️</div>
          <h3>No roadmap generated yet</h3>
          <p>Complete your career assessment to get a personalized roadmap.</p>
          <button className="btn btn-primary" style={{ marginTop: 20 }} onClick={() => navigate('/assessment')}>
            Start Assessment
          </button>
        </div>
      </div>
    )
  }

  const roadmap = analysisResult.roadmap || {}

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h1 className="section-title">🗺️ Career Learning Roadmap</h1>
          <p className="section-subtitle">
            Personalized 12-month plan for {profile?.name || 'you'} → {analysisResult.top_career}
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/progress')}>Update Progress</button>
          <button className="btn btn-primary btn-sm" onClick={() => navigate('/chat')}>Ask AI</button>
        </div>
      </div>

      {/* Immediate action */}
      {roadmap.immediate_next_action && (
        <div className="immediate-action">
          <span>⚡</span>
          <div>
            <strong>Start Today</strong>
            <p>{roadmap.immediate_next_action}</p>
          </div>
        </div>
      )}

      {/* Phase tabs */}
      <div className="phase-tabs">
        {Object.entries(PHASE_LABELS).map(([key, meta]) => (
          <button
            key={key}
            className={`phase-tab ${activePhase === key ? 'active' : ''}`}
            style={activePhase === key ? { borderColor: meta.color, color: meta.color, background: meta.bg } : {}}
            onClick={() => setActivePhase(key)}
          >
            <span className="phase-tab-label">{meta.label}</span>
            <span className="phase-tab-period">{meta.period}</span>
          </button>
        ))}
      </div>

      {/* Phase content */}
      {Object.entries(PHASE_LABELS).map(([key, meta]) => {
        const phase = roadmap[key] || {}
        if (key !== activePhase) return null
        return (
          <div key={key} className="phase-content">
            <div className="phase-header" style={{ background: meta.bg, borderColor: meta.color }}>
              <div>
                <h2 style={{ color: meta.color }}>{meta.label}: {phase.focus || meta.period}</h2>
                <p>{phase.duration} · {phase.weekly_plan || `~${(Number(profile?.learning_hours) || 2) * 7} hrs/week`}</p>
              </div>
              <div className="phase-outcome-badge" style={{ background: meta.color }}>
                {phase.expected_outcome || 'Build skills'}
              </div>
            </div>

            <div className="phase-body">
              <PhaseSection title="📚 Skills to Learn" items={phase.skills_to_learn} color={meta.color} />
              <PhaseSection title="📖 Topics to Study" items={phase.topics} color={meta.color} />
              <PhaseSection title="💡 Practice Activities" items={phase.practice_activities} color={meta.color} />
              <PhaseSection title="🛠️ Projects to Build" items={phase.projects} color={meta.color} highlight />
              <PhaseSection title="🏅 Certifications" items={phase.certifications} color={meta.color} />
            </div>
          </div>
        )
      })}

      {/* Timeline overview */}
      <div className="card timeline-overview">
        <h2 style={{ marginBottom: 20 }}>📅 12-Month Timeline Overview</h2>
        <div className="timeline">
          {Object.entries(PHASE_LABELS).map(([key, meta]) => {
            const phase = roadmap[key] || {}
            return (
              <div key={key} className="timeline-phase">
                <div className="timeline-marker" style={{ background: meta.color }} />
                <div className="timeline-content">
                  <div className="timeline-period" style={{ color: meta.color }}>{meta.period}</div>
                  <div className="timeline-focus">{phase.focus || meta.label}</div>
                  <div className="timeline-outcome">{phase.expected_outcome}</div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

function PhaseSection({ title, items, color, highlight }) {
  if (!items || items.length === 0) return null
  return (
    <div className={`phase-section ${highlight ? 'phase-section-highlight' : ''}`}
      style={highlight ? { borderColor: color, background: `${color}08` } : {}}>
      <h3>{title}</h3>
      <ul className="phase-list">
        {items.map((item, i) => (
          <li key={i} style={{ '--bullet-color': color }}>{item}</li>
        ))}
      </ul>
    </div>
  )
}
