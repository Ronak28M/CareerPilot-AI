import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import './CareerRecommendations.css'

export default function CareerRecommendations() {
  const { analysisResult, profile } = useApp()
  const navigate = useNavigate()

  if (!analysisResult) {
    return (
      <div className="page-content">
        <div className="empty-state">
          <div style={{ fontSize: 56 }}>🎯</div>
          <h3>No recommendations yet</h3>
          <p>Complete your career assessment first.</p>
          <button className="btn btn-primary" style={{ marginTop: 20 }} onClick={() => navigate('/assessment')}>
            Start Assessment
          </button>
        </div>
      </div>
    )
  }

  const { career_recommendations = [], priority_skills = [], next_action = '' } = analysisResult

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h1 className="section-title">🎯 Career Recommendations</h1>
          <p className="section-subtitle">Top career paths personalized for {profile?.name || 'you'} by IBM Granite</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/comparison')}>Compare Careers</button>
          <button className="btn btn-primary btn-sm" onClick={() => navigate('/roadmap')}>View Roadmap</button>
        </div>
      </div>

      {/* Next action banner */}
      {next_action && (
        <div className="next-action-banner">
          <span>⚡</span>
          <div>
            <strong>Recommended Next Action</strong>
            <p>{next_action}</p>
          </div>
        </div>
      )}

      {/* Career cards */}
      <div className="career-cards">
        {career_recommendations.map((rec, i) => (
          <CareerCard key={i} rec={rec} rank={i + 1} />
        ))}
        {career_recommendations.length === 0 && (
          <div className="empty-state">
            <p>No career recommendations found. Try reassessing your profile.</p>
          </div>
        )}
      </div>

      {/* Priority skills */}
      {priority_skills.length > 0 && (
        <div className="card" style={{ marginTop: 24 }}>
          <h2 className="section-title" style={{ marginBottom: 16 }}>🔥 Priority Skills to Focus On</h2>
          <div className="tags-wrap">
            {priority_skills.map((s, i) => <span key={i} className="tag tag-orange">{s}</span>)}
          </div>
        </div>
      )}
    </div>
  )
}

function CareerCard({ rec, rank }) {
  const rankColors = ['#fbbf24', '#9ca3af', '#cd7c3f']
  const matchColor = rec.match_percentage >= 75 ? 'var(--success)' : rec.match_percentage >= 60 ? 'var(--warning)' : 'var(--danger)'

  return (
    <div className={`career-card ${rank === 1 ? 'career-card-top' : ''}`}>
      {rank === 1 && <div className="top-badge">🏆 Best Match</div>}

      <div className="career-card-header">
        <div className="career-rank-badge" style={{ background: rankColors[rank - 1] || '#6b7280' }}>#{rank}</div>
        <div className="career-title-wrap">
          <h2 className="career-name">{rec.career_name}</h2>
          <p className="career-why">{rec.why_it_matches}</p>
        </div>
        <div className="match-ring-large" style={{ borderColor: matchColor, color: matchColor }}>
          {rec.match_percentage}%
        </div>
      </div>

      <div className="career-card-body">
        <div className="career-section">
          <h3>✅ Existing Relevant Skills</h3>
          <div className="tags-wrap">
            {(rec.existing_skills || []).map((s, i) => <span key={i} className="tag tag-green">{s}</span>)}
          </div>
        </div>

        <div className="career-section">
          <h3>📚 Skills to Learn</h3>
          <div className="tags-wrap">
            {(rec.skills_to_learn || rec.missing_skills || []).map((s, i) => <span key={i} className="tag tag-blue">{s}</span>)}
          </div>
        </div>

        <div className="career-section">
          <h3>💼 Job Roles</h3>
          <div className="tags-wrap">
            {(rec.job_roles || []).map((r, i) => <span key={i} className="tag tag-purple">{r}</span>)}
          </div>
        </div>

        <div className="career-sections-row">
          <div className="career-section">
            <h3>🛠️ Recommended Projects</h3>
            <ul className="career-list">
              {(rec.recommended_projects || []).map((p, i) => <li key={i}>{p}</li>)}
            </ul>
          </div>
          <div className="career-section">
            <h3>🏅 Certifications</h3>
            <ul className="career-list">
              {(rec.recommended_certifications || []).map((c, i) => <li key={i}>{c}</li>)}
            </ul>
          </div>
        </div>

        {(rec.next_steps || []).length > 0 && (
          <div className="career-section">
            <h3>👣 Next Steps</h3>
            <ol className="career-list career-steps">
              {rec.next_steps.map((s, i) => <li key={i}>{s}</li>)}
            </ol>
          </div>
        )}
      </div>
    </div>
  )
}
