import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import './SkillGapAnalysis.css'

export default function SkillGapAnalysis() {
  const { analysisResult, profile } = useApp()
  const navigate = useNavigate()

  if (!analysisResult) {
    return (
      <div className="page-content">
        <div className="empty-state">
          <div style={{ fontSize: 56 }}>💻</div>
          <h3>No skill analysis yet</h3>
          <p>Complete your career assessment to see your skill gap analysis.</p>
          <button className="btn btn-primary" style={{ marginTop: 20 }} onClick={() => navigate('/assessment')}>
            Start Assessment
          </button>
        </div>
      </div>
    )
  }

  const skill = analysisResult.skill_analysis || {}
  const strong = skill.strong_skills || []
  const beginner = skill.beginner_skills || []
  const missing = skill.missing_skills || []
  const priority = skill.priority_skills || analysisResult.priority_skills || []
  const matchPct = skill.skill_match_percentage || 0
  const topCareer = analysisResult.top_career || 'your target career'

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h1 className="section-title">💻 Skill Gap Analysis</h1>
          <p className="section-subtitle">Your skill profile for {topCareer}</p>
        </div>
        <button className="btn btn-primary btn-sm" onClick={() => navigate('/roadmap')}>
          View Learning Roadmap
        </button>
      </div>

      {/* Match score */}
      <div className="skill-match-banner">
        <div className="skill-match-ring" style={{
          background: `conic-gradient(var(--primary) ${matchPct * 3.6}deg, #e2e8f0 0deg)`
        }}>
          <div className="skill-match-inner">
            <span className="skill-match-pct">{matchPct}%</span>
            <span className="skill-match-label">Skill Match</span>
          </div>
        </div>
        <div className="skill-match-info">
          <h2>Skill Match for {topCareer}</h2>
          <p>{skill.analysis_summary || 'Based on your current skills and target career requirements.'}</p>
          <div className="skill-legend">
            <span className="legend-dot" style={{ background: 'var(--success)' }} /> Strong skills: {strong.length}
            <span className="legend-dot" style={{ background: 'var(--warning)' }} /> Beginner skills: {beginner.length}
            <span className="legend-dot" style={{ background: 'var(--danger)' }} /> Missing skills: {missing.length}
          </div>
        </div>
      </div>

      <div className="skill-grid">
        {/* Strong Skills */}
        <div className="card">
          <h2 className="skill-section-title" style={{ color: 'var(--success)' }}>✅ Strong Skills</h2>
          <div className="skill-items">
            {strong.length === 0 && <p className="text-muted">No strong skills identified yet.</p>}
            {strong.map((s, i) => (
              <div key={i} className="skill-item">
                <div className="skill-item-header">
                  <span className="skill-name">{s.name}</span>
                  <span className="skill-pct strong">{s.proficiency}%</span>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${s.proficiency}%`, background: 'var(--success)' }} />
                </div>
                {s.relevance && <p className="skill-relevance">{s.relevance}</p>}
              </div>
            ))}
          </div>
        </div>

        {/* Beginner Skills */}
        <div className="card">
          <h2 className="skill-section-title" style={{ color: 'var(--warning)' }}>📈 Skills to Improve</h2>
          <div className="skill-items">
            {beginner.length === 0 && <p className="text-muted">No beginner skills identified.</p>}
            {beginner.map((s, i) => (
              <div key={i} className="skill-item">
                <div className="skill-item-header">
                  <span className="skill-name">{s.name}</span>
                  <span className="skill-pct warning">{s.proficiency}%</span>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${s.proficiency}%`, background: 'var(--warning)' }} />
                </div>
                {s.action && <p className="skill-relevance">{s.action}</p>}
              </div>
            ))}
          </div>
        </div>

        {/* Missing Skills */}
        <div className="card skill-missing-card">
          <h2 className="skill-section-title" style={{ color: 'var(--danger)' }}>❌ Missing Skills</h2>
          <div className="missing-skills-list">
            {missing.length === 0 && <p className="text-muted">No critical missing skills!</p>}
            {missing.map((s, i) => (
              <div key={i} className="missing-skill-item">
                <div className="missing-skill-name">{s.name}</div>
                <span className={`badge ${s.importance === 'critical' ? 'badge-red' : s.importance === 'high' ? 'badge-orange' : 'badge-blue'}`}>
                  {s.importance}
                </span>
                <span className="missing-time">{s.learning_time}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Priority Skills */}
        <div className="card">
          <h2 className="skill-section-title" style={{ color: 'var(--primary)' }}>🔥 Priority Skills</h2>
          <p style={{ fontSize: 14, color: 'var(--text-muted)', marginBottom: 16 }}>
            Focus on these skills next to maximize your career readiness.
          </p>
          <div className="priority-skills-list">
            {priority.map((s, i) => (
              <div key={i} className="priority-skill-item">
                <span className="priority-num">{i + 1}</span>
                <span className="priority-name">{s}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
