import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import toast from 'react-hot-toast'
import './Assessment.css'

const SECTIONS = ['Academic', 'Skills', 'Interests', 'Career Goals', 'Experience', 'Learning']

const INITIAL_FORM = {
  name: '', degree: '', branch: '', year: '', cgpa: '',
  technical_skills: '', soft_skills: '', programming_languages: '', tools: '',
  interests: '', favorite_subjects: '', hobbies: '',
  career_goals: '', preferred_domain: '', preferred_industry: '',
  short_term_goal: '', long_term_goal: '',
  projects: '', internships: '', certifications: '', achievements: '',
  learning_hours: '2', learning_style: 'Visual', learning_priorities: '',
}

export default function Assessment() {
  const [step, setStep] = useState(0)
  const [form, setForm] = useState(INITIAL_FORM)
  const { submitProfile, isAnalyzing } = useApp()
  const navigate = useNavigate()

  function handleChange(e) {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  function handleNext() {
    if (step === 0 && (!form.name || !form.degree || !form.branch || !form.year || !form.cgpa)) {
      toast.error('Please fill in all academic fields.')
      return
    }
    if (step === 1 && !form.technical_skills) {
      toast.error('Please enter at least one technical skill.')
      return
    }
    setStep(s => s + 1)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!form.career_goals) { toast.error('Please describe your career goals.'); return }
    const toastId = toast.loading('🤖 CareerPilot AI is analyzing your profile...')
    try {
      // Merge technical_skills with programming_languages and tools for richer analysis
      const enriched = {
        ...form,
        technical_skills: [form.technical_skills, form.programming_languages, form.tools]
          .filter(Boolean).join(', '),
      }
      await submitProfile(enriched)
      toast.success('Analysis complete! Redirecting to your dashboard...', { id: toastId })
      navigate('/dashboard')
    } catch {
      toast.error('Analysis failed. Please try again.', { id: toastId })
    }
  }

  function fillDemo() {
    setForm({
      name: 'Priya Sharma', degree: 'B.Tech', branch: 'Computer Science',
      year: '2nd Year', cgpa: '7.8',
      technical_skills: 'HTML, CSS, JavaScript (Basic), Python (Beginner), UI/UX Basics',
      soft_skills: 'Communication, Teamwork, Creativity, Problem Solving',
      programming_languages: 'JavaScript, Python', tools: 'VS Code, Figma (Basic)',
      interests: 'Web Design, Data Visualization, User Experience, Technology',
      favorite_subjects: 'Web Technologies, Data Structures, Design Thinking',
      hobbies: 'Sketching, Reading tech blogs',
      career_goals: 'Become a Frontend Developer or Data Analyst within 1 year',
      preferred_domain: 'Frontend Development, Data Analytics, UI/UX',
      preferred_industry: 'Technology, Product Startups',
      short_term_goal: 'Build a strong portfolio with 3 real projects',
      long_term_goal: 'Work at a product company as a senior developer',
      projects: 'Personal blog website (HTML/CSS), Simple Python calculator',
      internships: 'None yet',
      certifications: 'HTML/CSS Basics (freeCodeCamp)',
      achievements: 'Top 10 in department, Participated in college hackathon',
      learning_hours: '2', learning_style: 'Visual',
      learning_priorities: 'Frontend development, JavaScript, React',
    })
    toast.success('Demo profile loaded!')
  }

  return (
    <div className="assessment-page">
      <div className="assessment-header">
        <div className="container">
          <a href="/" className="back-link">← Back to Home</a>
          <div className="assessment-title-wrap">
            <h1 className="assessment-title">Career Assessment</h1>
            <p className="assessment-subtitle">Help us understand you better to deliver personalised career guidance</p>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={fillDemo} type="button">
            ✨ Fill Demo Profile
          </button>
        </div>
      </div>

      {/* Progress tabs */}
      <div className="assessment-tabs-wrap">
        <div className="container assessment-tabs">
          {SECTIONS.map((s, i) => (
            <button
              key={s}
              type="button"
              className={`tab-btn ${step === i ? 'active' : ''} ${i < step ? 'done' : ''}`}
              onClick={() => i < step && setStep(i)}
            >
              <span className="tab-num">{i < step ? '✓' : i + 1}</span>
              <span className="tab-label">{s}</span>
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="assessment-form container">
        {/* Section 0: Academic */}
        {step === 0 && (
          <div className="form-section card">
            <h2 className="form-section-title">📚 Academic Information</h2>
            <div className="grid-2">
              <Field label="Full Name *" name="name" value={form.name} onChange={handleChange} placeholder="e.g. Priya Sharma" />
              <Field label="Degree *" name="degree" value={form.degree} onChange={handleChange} placeholder="e.g. B.Tech, B.Sc, BCA" />
              <Field label="Branch / Specialization *" name="branch" value={form.branch} onChange={handleChange} placeholder="e.g. Computer Science, IT, Electronics" />
              <SelectField label="Current Year *" name="year" value={form.year} onChange={handleChange}
                options={['1st Year','2nd Year','3rd Year','4th Year','Final Year','Postgraduate']} />
              <Field label="CGPA / Percentage *" name="cgpa" value={form.cgpa} onChange={handleChange} placeholder="e.g. 7.8 or 78%" />
            </div>
          </div>
        )}

        {/* Section 1: Skills */}
        {step === 1 && (
          <div className="form-section card">
            <h2 className="form-section-title">💻 Skills & Technologies</h2>
            <div className="grid-2">
              <TextArea label="Technical Skills *" name="technical_skills" value={form.technical_skills} onChange={handleChange}
                placeholder="e.g. HTML, CSS, JavaScript, React, Python, SQL, Machine Learning..." rows={3} />
              <TextArea label="Programming Languages" name="programming_languages" value={form.programming_languages} onChange={handleChange}
                placeholder="e.g. JavaScript, Python, Java, C++..." rows={3} />
              <TextArea label="Tools & Technologies" name="tools" value={form.tools} onChange={handleChange}
                placeholder="e.g. VS Code, Figma, Git, Docker, AWS..." rows={3} />
              <TextArea label="Soft Skills" name="soft_skills" value={form.soft_skills} onChange={handleChange}
                placeholder="e.g. Communication, Leadership, Problem Solving, Teamwork..." rows={3} />
            </div>
          </div>
        )}

        {/* Section 2: Interests */}
        {step === 2 && (
          <div className="form-section card">
            <h2 className="form-section-title">🌟 Interests & Passions</h2>
            <div className="grid-2">
              <TextArea label="Areas of Interest" name="interests" value={form.interests} onChange={handleChange}
                placeholder="e.g. Web Development, AI/ML, Data Science, Design, Cybersecurity..." rows={3} />
              <TextArea label="Favourite Subjects" name="favorite_subjects" value={form.favorite_subjects} onChange={handleChange}
                placeholder="e.g. Data Structures, Web Technologies, Statistics..." rows={3} />
              <TextArea label="Hobbies" name="hobbies" value={form.hobbies} onChange={handleChange}
                placeholder="e.g. Reading, Sketching, Building apps, Gaming..." rows={3} />
            </div>
          </div>
        )}

        {/* Section 3: Career Goals */}
        {step === 3 && (
          <div className="form-section card">
            <h2 className="form-section-title">🎯 Career Goals</h2>
            <div className="grid-2">
              <TextArea label="Career Goals *" name="career_goals" value={form.career_goals} onChange={handleChange}
                placeholder="Describe the career you want to pursue..." rows={3} />
              <TextArea label="Preferred Domain" name="preferred_domain" value={form.preferred_domain} onChange={handleChange}
                placeholder="e.g. Frontend Development, Data Science, DevOps, Product Design..." rows={3} />
              <Field label="Preferred Industry" name="preferred_industry" value={form.preferred_industry} onChange={handleChange}
                placeholder="e.g. Technology, Finance, Healthcare, E-commerce..." />
              <Field label="Short-term Goal (6-12 months)" name="short_term_goal" value={form.short_term_goal} onChange={handleChange}
                placeholder="e.g. Land an internship, build a portfolio..." />
              <Field label="Long-term Goal (3-5 years)" name="long_term_goal" value={form.long_term_goal} onChange={handleChange}
                placeholder="e.g. Senior Developer role at a product company..." />
            </div>
          </div>
        )}

        {/* Section 4: Experience */}
        {step === 4 && (
          <div className="form-section card">
            <h2 className="form-section-title">🏆 Experience & Achievements</h2>
            <div className="grid-2">
              <TextArea label="Projects" name="projects" value={form.projects} onChange={handleChange}
                placeholder="List projects you've built (name + brief description)..." rows={4} />
              <TextArea label="Internships" name="internships" value={form.internships} onChange={handleChange}
                placeholder="List any internships (company, role, duration)..." rows={4} />
              <TextArea label="Certifications" name="certifications" value={form.certifications} onChange={handleChange}
                placeholder="e.g. Python for Everybody (Coursera), AWS Cloud Practitioner..." rows={3} />
              <TextArea label="Achievements" name="achievements" value={form.achievements} onChange={handleChange}
                placeholder="Hackathons, awards, academic achievements..." rows={3} />
            </div>
          </div>
        )}

        {/* Section 5: Learning */}
        {step === 5 && (
          <div className="form-section card">
            <h2 className="form-section-title">📖 Learning Preferences</h2>
            <div className="grid-2">
              <div className="field-group">
                <label>Available Learning Hours per Day *</label>
                <div className="hours-grid">
                  {['0.5','1','2','3','4','5+'].map(h => (
                    <button
                      key={h}
                      type="button"
                      className={`hour-btn ${form.learning_hours === h ? 'selected' : ''}`}
                      onClick={() => setForm(f => ({ ...f, learning_hours: h }))}
                    >
                      {h}h
                    </button>
                  ))}
                </div>
              </div>
              <SelectField label="Preferred Learning Style" name="learning_style" value={form.learning_style} onChange={handleChange}
                options={['Visual (videos, diagrams)','Reading (books, articles)','Hands-on (projects, coding)','Mixed','Mentorship']} />
              <TextArea label="Current Learning Priorities" name="learning_priorities" value={form.learning_priorities} onChange={handleChange}
                placeholder="What are you focusing on learning right now?..." rows={3} />
            </div>
          </div>
        )}

        {/* Nav buttons */}
        <div className="form-nav">
          {step > 0 && (
            <button type="button" className="btn btn-secondary btn-lg" onClick={() => setStep(s => s - 1)}>
              ← Previous
            </button>
          )}
          {step < SECTIONS.length - 1 && (
            <button type="button" className="btn btn-primary btn-lg" onClick={handleNext}>
              Next →
            </button>
          )}
          {step === SECTIONS.length - 1 && (
            <button type="submit" className="btn btn-primary btn-lg" disabled={isAnalyzing}>
              {isAnalyzing ? (
                <><span className="spinner" /> Analyzing with IBM Granite...</>
              ) : (
                '🚀 Analyze My Career Profile'
              )}
            </button>
          )}
        </div>
      </form>
    </div>
  )
}

function Field({ label, name, value, onChange, placeholder }) {
  return (
    <div className="field-group">
      <label>{label}</label>
      <input
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="form-input"
      />
    </div>
  )
}

function TextArea({ label, name, value, onChange, placeholder, rows = 3 }) {
  return (
    <div className="field-group">
      <label>{label}</label>
      <textarea
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        className="form-input form-textarea"
      />
    </div>
  )
}

function SelectField({ label, name, value, onChange, options }) {
  return (
    <div className="field-group">
      <label>{label}</label>
      <select name={name} value={value} onChange={onChange} className="form-input form-select">
        {options.map(o => <option key={o}>{o}</option>)}
      </select>
    </div>
  )
}
