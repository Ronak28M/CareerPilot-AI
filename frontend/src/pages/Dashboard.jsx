import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import './Dashboard.css'

export default function Dashboard() {
  const { profile, analysisResult, progressData } = useApp()
  const navigate = useNavigate()

  if (!profile || !analysisResult) {
    return (
      <div className="page-content">
        <div className="empty-state">
          <div style={{ fontSize: 64, marginBottom: 16 }}>🚀</div>
          <h3>No career analysis yet</h3>
          <p>Complete your career assessment to see your personalized dashboard.</p>
          <div style={{ marginTop: 24, display: 'flex', gap: 12, justifyContent: 'center' }}>
            <button className="btn btn-primary btn-lg" onClick={() => navigate('/assessment')}>
              Start Career Assessment
            </button>
          </div>
        </div>
      </div>
    )
  }

  const topRec = analysisResult.career_recommendations?.[0] || {}
  const skillAnalysis = analysisResult.skill_analysis || {}
  const roadmap = analysisResult.roadmap || {}

  return (
    <div className="page-content">
      {/* Header */}
      <div className="dashboard-header">
        <div className="dash-greeting">
          <div className="dash-avatar">{profile.name?.[0]?.toUpperCase()}</div>
          <div>
            <h1>Welcome back, {profile.name.split(' ')[0]}! 👋</h1>
            <p>{profile.degree} · {profile.branch} · {profile.year} · CGPA: {profile.cgpa}</p>
          </div>
        </div>
        <div className="dash-header-actions">
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/assessment')}>
            🔄 Reassess Career
          </button>
          <button className="btn btn-primary btn-sm" onClick={() => navigate('/chat')}>
            💬 Chat with AI
          </button>
        </div>
      </div>

      {/* Stats row */}
      <div className="dashboard-stats">
        <StatCard
          icon="🎯"
          label="Top Career Match"
          value={topRec.career_name || 'N/A'}
          sub={`${topRec.match_percentage || 0}% match`}
          color="blue"
        />
        <StatCard
          icon="📊"
          label="Skill Match"
          value={`${skillAnalysis.skill_match_percentage || 0}%`}
          sub="Current skill alignment"
          color="purple"
        />
        <StatCard
          icon="📈"
          label="Roadmap Progress"
          value={`${progressData.overallProgress}%`}
          sub={`Phase: ${progressData.currentPhase?.replace('_', ' ')}`}
          color="green"
        />
        <StatCard
          icon="⚡"
          label="Priority Skills"
          value={analysisResult.priority_skills?.length || 0}
          sub="Skills to focus on"
          color="orange"
        />
      </div>

      {/* Main content */}
      <div className="dashboard-grid">
        {/* Career Recommendations */}
        <div className="card dash-card">
          <div className="dash-card-header">
            <h2>🎯 Career Recommendations</h2>
            <button className="btn btn-secondary btn-sm" onClick={() => navigate('/recommendations')}>
              View All
            </button>
          </div>
          <div className="rec-list">
            {(analysisResult.career_recommendations || []).slice(0, 3).map((rec, i) => (
              <div key={i} className="rec-item">
                <div className="rec-rank">{i + 1}</div>
                <div className="rec-info">
                  <div className="rec-name">{rec.career_name}</div>
                  <div className="rec-why">{rec.why_it_matches?.slice(0, 80)}...</div>
                </div>
                <div className={`match-pill ${rec.match_percentage >= 75 ? 'high' : rec.match_percentage >= 60 ? 'mid' : 'low'}`}>
                  {rec.match_percentage}%
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Skill Analysis */}
        <div className="card dash-card">
          <div className="dash-card-header">
            <h2>💻 Skill Analysis</h2>
            <button className="btn btn-secondary btn-sm" onClick={() => navigate('/skill-gap')}>
              Full Analysis
            </button>
          </div>
          <div className="skill-list">
            {(skillAnalysis.strong_skills || []).slice(0, 3).map((skill, i) => (
              <SkillBar key={i} name={skill.name} pct={skill.proficiency} color="var(--primary)" />
            ))}
            {(skillAnalysis.beginner_skills || []).slice(0, 2).map((skill, i) => (
              <SkillBar key={i} name={skill.name} pct={skill.proficiency} color="var(--warning)" />
            ))}
          </div>
        </div>

        {/* Next Action */}
        <div className="card dash-card next-action-card">
          <h2>⚡ Recommended Next Action</h2>
          <p className="next-action-text">
            {roadmap.immediate_next_action || analysisResult.next_action || 'Complete your assessment to get personalized recommendations.'}
          </p>
          <div className="dash-actions">
            <button className="btn btn-primary" onClick={() => navigate('/roadmap')}>View Roadmap</button>
            <button className="btn btn-secondary" onClick={() => navigate('/progress')}>Update Progress</button>
          </div>
        </div>

        {/* Priority Skills */}
        <div className="card dash-card">
          <div className="dash-card-header">
            <h2>🔥 Priority Skills</h2>
          </div>
          <div className="tags-wrap">
            {(analysisResult.priority_skills || []).map((skill, i) => (
              <span key={i} className="tag tag-blue">{skill}</span>
            ))}
            {(analysisResult.skill_gaps || []).slice(0, 5).map((skill, i) => (
              <span key={i} className="tag tag-red">{skill}</span>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card dash-card quick-actions-card">
          <h2>🗺️ Quick Actions</h2>
          <div className="quick-actions-grid">
            <QuickAction icon="🗺️" label="View Roadmap" onClick={() => navigate('/roadmap')} />
            <QuickAction icon="⚖️" label="Compare Careers" onClick={() => navigate('/comparison')} />
            <QuickAction icon="💬" label="Chat with AI" onClick={() => navigate('/chat')} />
            <QuickAction icon="📊" label="Skill Analysis" onClick={() => navigate('/skill-gap')} />
            <QuickAction icon="📈" label="Update Progress" onClick={() => navigate('/progress')} />
            <QuickAction icon="🎯" label="All Careers" onClick={() => navigate('/recommendations')} />
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon, label, value, sub, color }) {
  return (
    <div className={`stat-card stat-${color}`}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-body">
        <div className="stat-label">{label}</div>
        <div className="stat-value">{value}</div>
        <div className="stat-sub">{sub}</div>
      </div>
    </div>
  )
}

function SkillBar({ name, pct, color }) {
  return (
    <div className="skill-bar-row">
      <div className="skill-bar-label">
        <span>{name}</span>
        <span>{pct}%</span>
      </div>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
    </div>
  )
}

function QuickAction({ icon, label, onClick }) {
  return (
    <button className="quick-action-btn" onClick={onClick}>
      <span className="qa-icon">{icon}</span>
      <span>{label}</span>
    </button>
  )
}
