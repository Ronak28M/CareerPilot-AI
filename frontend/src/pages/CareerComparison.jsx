import React, { useState } from 'react'
import { useApp } from '../context/AppContext'
import toast from 'react-hot-toast'
import './CareerComparison.css'

const PRESET_CAREERS = [
  'Frontend Developer', 'Data Analyst', 'UI/UX Designer',
  'Backend Developer', 'Full Stack Developer', 'Data Scientist',
  'Machine Learning Engineer', 'DevOps Engineer', 'Cybersecurity Analyst',
  'Product Manager', 'Mobile App Developer', 'Cloud Engineer',
]

export default function CareerComparison() {
  const { compareCareerPaths, profile } = useApp()
  const [selected, setSelected] = useState([])
  const [custom, setCustom] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  function toggleCareer(career) {
    setSelected(prev => {
      if (prev.includes(career)) return prev.filter(c => c !== career)
      if (prev.length >= 3) { toast.error('Select up to 3 careers'); return prev }
      return [...prev, career]
    })
  }

  function addCustom() {
    if (!custom.trim()) return
    if (selected.length >= 3) { toast.error('Select up to 3 careers'); return }
    if (!selected.includes(custom.trim())) setSelected(prev => [...prev, custom.trim()])
    setCustom('')
  }

  async function handleCompare() {
    if (selected.length < 2) { toast.error('Select at least 2 careers to compare'); return }
    setLoading(true)
    const toastId = toast.loading('🤖 Comparing career paths...')
    try {
      const data = await compareCareerPaths(selected)
      setResult(data)
      toast.success('Comparison complete!', { id: toastId })
    } catch {
      toast.error('Comparison failed. Please try again.', { id: toastId })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-content">
      <h1 className="section-title">⚖️ Career Comparison</h1>
      <p className="section-subtitle">Compare 2–3 career paths to find your best fit</p>

      {/* Career selector */}
      <div className="card comparison-selector">
        <h2>Select careers to compare (2–3)</h2>
        <div className="career-presets">
          {PRESET_CAREERS.map(c => (
            <button
              key={c}
              className={`preset-career-btn ${selected.includes(c) ? 'selected' : ''}`}
              onClick={() => toggleCareer(c)}
            >
              {selected.includes(c) && <span>✓ </span>}{c}
            </button>
          ))}
        </div>
        <div className="custom-career-row">
          <input
            className="form-input"
            placeholder="Or type a custom career..."
            value={custom}
            onChange={e => setCustom(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && addCustom()}
          />
          <button className="btn btn-secondary btn-sm" onClick={addCustom}>Add</button>
        </div>
        {selected.length > 0 && (
          <div className="selected-careers">
            <strong>Selected:</strong>
            {selected.map(c => (
              <span key={c} className="selected-career-tag">
                {c}
                <button onClick={() => setSelected(prev => prev.filter(x => x !== c))}>×</button>
              </span>
            ))}
          </div>
        )}
        <button
          className="btn btn-primary btn-lg"
          onClick={handleCompare}
          disabled={loading || selected.length < 2}
          style={{ marginTop: 16 }}
        >
          {loading ? <><span className="spinner" /> Analyzing...</> : '🔍 Compare Careers'}
        </button>
      </div>

      {/* Results */}
      {result && (
        <>
          {result.recommended_career && (
            <div className="recommendation-banner">
              <div>
                <strong>🏆 Recommended Career: {result.recommended_career}</strong>
                <p>{result.recommendation_reason}</p>
              </div>
            </div>
          )}

          {result.comparison_summary && (
            <div className="comparison-summary card">
              <p>{result.comparison_summary}</p>
            </div>
          )}

          <div className="comparison-grid">
            {(result.comparisons || []).map((comp, i) => (
              <div key={i} className={`comparison-card card ${comp.career_name === result.recommended_career ? 'recommended' : ''}`}>
                {comp.career_name === result.recommended_career && (
                  <div className="rec-ribbon">Recommended</div>
                )}
                <h2 className="comp-career-name">{comp.career_name}</h2>

                <div className="comp-match">
                  <div className="comp-match-bar-wrap">
                    <div className="comp-match-label">Match Score</div>
                    <div className="progress-bar" style={{ height: 12 }}>
                      <div className="progress-fill" style={{ width: `${comp.match_score}%` }} />
                    </div>
                    <div className="comp-match-pct">{comp.match_score}%</div>
                  </div>
                </div>

                <div className="comp-details">
                  <CompRow label="Learning Difficulty" value={comp.learning_difficulty} type={comp.learning_difficulty} />
                  <CompRow label="Time to Job Ready" value={comp.time_to_job_ready} />
                  <CompRow label="Job Demand" value={comp.job_demand} type={comp.job_demand} />
                  <CompRow label="Avg Salary" value={comp.avg_salary_range} />
                </div>

                <div className="comp-section">
                  <h4>✅ Matching Skills</h4>
                  <div className="tags-wrap">
                    {(comp.existing_matching_skills || []).map((s, j) => <span key={j} className="tag tag-green">{s}</span>)}
                  </div>
                </div>

                <div className="comp-section">
                  <h4>❌ Skill Gaps</h4>
                  <div className="tags-wrap">
                    {(comp.skill_gaps || []).map((s, j) => <span key={j} className="tag tag-red">{s}</span>)}
                  </div>
                </div>

                <div className="comp-section">
                  <h4>💼 Job Roles</h4>
                  <div className="tags-wrap">
                    {(comp.job_roles || []).map((r, j) => <span key={j} className="tag">{r}</span>)}
                  </div>
                </div>

                <div className="comp-pros-cons">
                  <div>
                    <h4>👍 Pros</h4>
                    <ul>{(comp.pros || []).map((p, j) => <li key={j}>{p}</li>)}</ul>
                  </div>
                  <div>
                    <h4>👎 Cons</h4>
                    <ul>{(comp.cons || []).map((c, j) => <li key={j}>{c}</li>)}</ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function CompRow({ label, value, type }) {
  const colorMap = {
    easy: 'var(--success)', moderate: 'var(--warning)', hard: 'var(--danger)',
    high: 'var(--success)', medium: 'var(--warning)', low: 'var(--danger)',
  }
  return (
    <div className="comp-row">
      <span className="comp-row-label">{label}</span>
      <span className="comp-row-value" style={type ? { color: colorMap[type?.toLowerCase()] || 'inherit' } : {}}>
        {value || '—'}
      </span>
    </div>
  )
}
