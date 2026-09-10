import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import toast from 'react-hot-toast'
import './Landing.css'

const FEATURES = [
  {
    icon: '🤖',
    title: 'Agentic AI Workflow',
    desc: 'IBM watsonx Orchestrate coordinates multiple AI agents to analyze your profile holistically.',
  },
  {
    icon: '🎯',
    title: 'Personalized Career Paths',
    desc: 'IBM Granite analyzes your skills, interests, and goals to recommend the best-matched careers.',
  },
  {
    icon: '📊',
    title: 'Skill Gap Analysis',
    desc: 'See exactly which skills you have, which need improvement, and which to learn next.',
  },
  {
    icon: '🗺️',
    title: 'Dynamic Roadmaps',
    desc: 'Get a personalized 12-month learning roadmap that adapts as you progress.',
  },
  {
    icon: '💬',
    title: 'AI Career Chat',
    desc: 'Chat with CareerPilot Agent anytime for personalized guidance and instant answers.',
  },
  {
    icon: '📈',
    title: 'Progress Tracking',
    desc: 'Track your learning journey and receive updated recommendations as you complete tasks.',
  },
]

const HOW_IT_WORKS = [
  { step: '01', title: 'Fill Your Profile', desc: 'Share your academic background, skills, interests, and career goals.' },
  { step: '02', title: 'AI Analyzes', desc: 'IBM Granite and watsonx Orchestrate analyze your profile through multiple specialized agents.' },
  { step: '03', title: 'Get Recommendations', desc: 'Receive top 3 career paths with match scores, skill gaps, and personalized roadmaps.' },
  { step: '04', title: 'Track & Adapt', desc: 'Update your progress and the AI adapts your roadmap and recommendations automatically.' },
]

export default function Landing() {
  const navigate = useNavigate()
  const { loadDemoProfile, isAnalyzing } = useApp()

  async function handleDemo() {
    const toastId = toast.loading('Loading demo profile and running AI analysis...')
    try {
      await loadDemoProfile()
      toast.success('Demo profile analyzed!', { id: toastId })
      navigate('/dashboard')
    } catch {
      toast.error('Demo failed. Please try again.', { id: toastId })
    }
  }

  return (
    <div className="landing">
      {/* Hero */}
      <header className="hero">
        <nav className="hero-nav container">
          <div className="hero-brand">
            <span className="hero-icon">🚀</span>
            <span className="hero-name">CareerPilot <span>AI</span></span>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/assessment')}>
            Start Free Assessment
          </button>
        </nav>

        <div className="hero-content container">
          <div className="hero-badge">
            <span>🏆 AICTE 2026 Problem Statement No. 15</span>
          </div>
          <h1 className="hero-title">
            Your AI-powered path to a<br />
            <span className="gradient-text">future-ready career</span>
          </h1>
          <p className="hero-desc">
            CareerPilot AI is an agentic career counseling companion that analyzes your academic
            background, skills, and goals using <strong>IBM Granite</strong> and{' '}
            <strong>watsonx Orchestrate</strong> to deliver personalized career recommendations,
            skill-gap analysis, and adaptive learning roadmaps.
          </p>
          <div className="hero-actions">
            <button
              className="btn btn-primary btn-lg"
              onClick={() => navigate('/assessment')}
            >
              🎯 Start Career Assessment
            </button>
            <button
              className="btn btn-secondary btn-lg"
              onClick={handleDemo}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? (
                <><span className="spinner" /> Analyzing...</>
              ) : (
                '▶ Try Demo Profile'
              )}
            </button>
          </div>
          <div className="hero-stats">
            <div className="stat"><span>IBM Granite</span><small>Primary AI Model</small></div>
            <div className="stat"><span>watsonx Orchestrate</span><small>Agent Workflow</small></div>
            <div className="stat"><span>6 AI Agents</span><small>Working Together</small></div>
            <div className="stat"><span>12-Month</span><small>Personalized Roadmap</small></div>
          </div>
        </div>
      </header>

      {/* Features */}
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Everything you need for career clarity</h2>
            <p>CareerPilot AI brings together multiple AI capabilities into one intelligent companion</p>
          </div>
          <div className="features-grid">
            {FEATURES.map(f => (
              <div key={f.title} className="feature-card">
                <span className="feature-icon">{f.icon}</span>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-section">
        <div className="container">
          <div className="section-header">
            <h2>How CareerPilot AI works</h2>
            <p>An agentic multi-step workflow powered by IBM AI</p>
          </div>
          <div className="steps-grid">
            {HOW_IT_WORKS.map((s, i) => (
              <div key={s.step} className="step-card">
                <div className="step-number">{s.step}</div>
                <h3>{s.title}</h3>
                <p>{s.desc}</p>
                {i < HOW_IT_WORKS.length - 1 && <div className="step-arrow">→</div>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Agent workflow diagram */}
      <section className="workflow-section">
        <div className="container">
          <div className="section-header">
            <h2>Agentic AI Architecture</h2>
            <p>watsonx Orchestrate coordinates a pipeline of specialized AI agents</p>
          </div>
          <div className="workflow-diagram">
            {[
              'Student Profile Input',
              'Career Profile Analyzer',
              'Skill Gap Analyzer',
              'Career Recommendation Agent',
              'Roadmap Generator Agent',
              'Project & Certification Agent',
              'CareerPilot Agent Response',
            ].map((node, i) => (
              <React.Fragment key={node}>
                <div className={`workflow-node ${i === 0 ? 'node-input' : i === 6 ? 'node-output' : 'node-agent'}`}>
                  <span>{node}</span>
                </div>
                {i < 6 && <div className="workflow-arrow">↓</div>}
              </React.Fragment>
            ))}
          </div>
          <p className="workflow-note">
            Powered by <strong>IBM watsonx Orchestrate</strong> · LLM: <strong>IBM Granite</strong>
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-card">
            <h2>Ready to discover your ideal career path?</h2>
            <p>Complete a 5-minute assessment and let AI map your future.</p>
            <div className="cta-actions">
              <button className="btn btn-primary btn-lg" onClick={() => navigate('/assessment')}>
                🚀 Start Career Assessment
              </button>
              <button className="btn btn-lg" style={{background:'rgba(255,255,255,0.15)', color:'#fff', border:'1.5px solid rgba(255,255,255,0.3)'}} onClick={handleDemo} disabled={isAnalyzing}>
                ▶ Try Demo Profile
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-brand">
            <span>🚀</span>
            <strong>CareerPilot AI</strong>
          </div>
          <p className="footer-desc">
            Agentic Career Counseling Companion · AICTE 2026 Problem Statement No. 15
          </p>
          <p className="footer-tech">
            Powered by IBM Granite · IBM watsonx Orchestrate · IBM Cloud
          </p>
        </div>
      </footer>
    </div>
  )
}
