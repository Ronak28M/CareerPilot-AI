import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import toast from 'react-hot-toast'
import './ProgressTracker.css'

export default function ProgressTracker() {
  const { analysisResult, progressData, updateProgress, profile } = useApp()
  const navigate = useNavigate()
  const [localProgress, setLocalProgress] = useState({ ...progressData })
  const [updatedRec, setUpdatedRec] = useState(null)
  const [loading, setLoading] = useState(false)
  const [newGoal, setNewGoal] = useState('')

  if (!analysisResult) {
    return (
      <div className="page-content">
        <div className="empty-state">
          <div style={{ fontSize: 56 }}>📈</div>
          <h3>No roadmap to track yet</h3>
          <p>Complete your career assessment to start tracking your progress.</p>
          <button className="btn btn-primary" style={{ marginTop: 20 }} onClick={() => navigate('/assessment')}>
            Start Assessment
          </button>
        </div>
      </div>
    )
  }

  const roadmap = analysisResult.roadmap || {}
  const allSkills = [
    ...(roadmap.phase_1?.skills_to_learn || []),
    ...(roadmap.phase_2?.skills_to_learn || []),
    ...(roadmap.phase_3?.skills_to_learn || []),
  ]
  const allProjects = [
    ...(roadmap.phase_1?.projects || []),
    ...(roadmap.phase_2?.projects || []),
    ...(roadmap.phase_3?.projects || []),
  ]
  const allCerts = [
    ...(roadmap.phase_1?.certifications || []),
    ...(roadmap.phase_2?.certifications || []),
    ...(roadmap.phase_3?.certifications || []),
  ]

  function toggleItem(type, item) {
    setLocalProgress(prev => {
      const list = prev[type] || []
      const newList = list.includes(item) ? list.filter(x => x !== item) : [...list, item]
      const total = allSkills.length + allProjects.length + allCerts.length
      const completed = (type === 'completedSkills' ? newList.length : (prev.completedSkills || []).length) +
        (type === 'completedProjects' ? newList.length : (prev.completedProjects || []).length) +
        (type === 'completedCertifications' ? newList.length : (prev.completedCertifications || []).length)
      const pct = total > 0 ? Math.round((completed / total) * 100) : 0

      // Determine phase
      const phaseTotals = [allSkills.slice(0, Math.ceil(allSkills.length / 3)), allProjects.slice(0, 1)]
      let currentPhase = 'phase_1'
      if (pct >= 66) currentPhase = 'phase_3'
      else if (pct >= 33) currentPhase = 'phase_2'

      return { ...prev, [type]: newList, overallProgress: pct, currentPhase }
    })
  }

  async function handleSave() {
    setLoading(true)
    try {
      const result = await updateProgress({ ...localProgress, newGoal })
      setUpdatedRec(result)
      setNewGoal('')
      toast.success('Progress saved and recommendations updated!')
    } catch {
      // error handled in context
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h1 className="section-title">📈 Progress Tracker</h1>
          <p className="section-subtitle">Track your learning journey and update the AI with your progress</p>
        </div>
        <button className="btn btn-primary btn-sm" onClick={() => navigate('/roadmap')}>
          View Roadmap
        </button>
      </div>

      {/* Overall progress */}
      <div className="card progress-overview">
        <div className="progress-overview-header">
          <div className="progress-circle-wrap">
            <div className="progress-circle" style={{
              background: `conic-gradient(var(--primary) ${localProgress.overallProgress * 3.6}deg, #e2e8f0 0deg)`
            }}>
              <div className="progress-circle-inner">
                <span className="progress-pct">{localProgress.overallProgress}%</span>
                <span className="progress-pct-label">Complete</span>
              </div>
            </div>
          </div>
          <div className="progress-overview-info">
            <h2>Overall Roadmap Progress</h2>
            <p>Target: {analysisResult.top_career}</p>
            <div className="progress-phase-badge">
              Current Phase: {localProgress.currentPhase?.replace('_', ' ')?.toUpperCase()}
            </div>
            <div className="progress-counts">
              <CountBadge label="Skills" done={localProgress.completedSkills?.length || 0} total={allSkills.length} />
              <CountBadge label="Projects" done={localProgress.completedProjects?.length || 0} total={allProjects.length} />
              <CountBadge label="Certifications" done={localProgress.completedCertifications?.length || 0} total={allCerts.length} />
            </div>
          </div>
        </div>
      </div>

      {/* Goal change */}
      <div className="card goal-change-card">
        <h2>🔄 Update Career Goal (Optional)</h2>
        <p>Changed your mind? Update your goal and the AI will adapt your recommendations.</p>
        <div className="goal-change-row">
          <input
            className="form-input"
            placeholder="e.g. I now want to become a Data Scientist"
            value={newGoal}
            onChange={e => setNewGoal(e.target.value)}
          />
        </div>
      </div>

      {/* Task tracking */}
      <div className="progress-grid">
        <TaskSection
          title="💻 Skills"
          items={allSkills}
          completed={localProgress.completedSkills || []}
          onToggle={item => toggleItem('completedSkills', item)}
          color="var(--primary)"
        />
        <TaskSection
          title="🛠️ Projects"
          items={allProjects}
          completed={localProgress.completedProjects || []}
          onToggle={item => toggleItem('completedProjects', item)}
          color="var(--secondary)"
        />
        <TaskSection
          title="🏅 Certifications"
          items={allCerts}
          completed={localProgress.completedCertifications || []}
          onToggle={item => toggleItem('completedCertifications', item)}
          color="var(--success)"
        />
      </div>

      <div className="progress-save-bar">
        <button className="btn btn-primary btn-lg" onClick={handleSave} disabled={loading}>
          {loading ? <><span className="spinner" /> Updating AI recommendations...</> : '💾 Save Progress & Get New Recommendations'}
        </button>
      </div>

      {/* Updated recommendations */}
      {updatedRec && (
        <div className="card updated-rec-card">
          <h2>🤖 Updated AI Guidance</h2>
          <div className="updated-rec-grid">
            <div className="updated-rec-item">
              <div className="uri-label">Progress Assessment</div>
              <div className="uri-value">{updatedRec.progress_assessment}</div>
            </div>
            <div className="updated-rec-item highlight">
              <div className="uri-label">⚡ Next Immediate Action</div>
              <div className="uri-value">{updatedRec.next_immediate_action}</div>
            </div>
            <div className="updated-rec-item">
              <div className="uri-label">Next Project</div>
              <div className="uri-value">{updatedRec.recommended_next_project}</div>
            </div>
            <div className="updated-rec-item">
              <div className="uri-label">Next Certification</div>
              <div className="uri-value">{updatedRec.recommended_next_certification}</div>
            </div>
            {updatedRec.motivational_message && (
              <div className="updated-rec-item motivational">
                <div className="uri-label">💪 {updatedRec.motivational_message}</div>
              </div>
            )}
            {updatedRec.goal_change_impact && (
              <div className="updated-rec-item goal-change">
                <div className="uri-label">🔄 Goal Change Impact</div>
                <div className="uri-value">{updatedRec.goal_change_impact}</div>
              </div>
            )}
          </div>
          <div style={{ marginTop: 16 }}>
            <span className="badge badge-blue">Career Readiness: {updatedRec.career_readiness_score || localProgress.overallProgress}%</span>
          </div>
        </div>
      )}
    </div>
  )
}

function TaskSection({ title, items, completed, onToggle, color }) {
  if (items.length === 0) return null
  return (
    <div className="card task-section">
      <h2 className="task-section-title">{title}</h2>
      <div className="task-progress-mini">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${(completed.length / items.length) * 100}%`, background: color }} />
        </div>
        <span>{completed.length}/{items.length}</span>
      </div>
      <div className="task-list">
        {items.map((item, i) => {
          const isDone = completed.includes(item)
          return (
            <label key={i} className={`task-item ${isDone ? 'done' : ''}`}>
              <input type="checkbox" checked={isDone} onChange={() => onToggle(item)} />
              <span className="task-name">{item}</span>
              {isDone && <span className="task-done-badge">✓</span>}
            </label>
          )
        })}
      </div>
    </div>
  )
}

function CountBadge({ label, done, total }) {
  return (
    <div className="count-badge">
      <span className="cb-done">{done}</span>/<span className="cb-total">{total}</span>
      <span className="cb-label">{label}</span>
    </div>
  )
}
