import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import './AIChat.css'

const QUICK_PROMPTS = [
  'What should I learn first?',
  'Am I ready for a frontend developer role?',
  'Suggest projects based on my current skills.',
  'What skills am I missing?',
  'I only have 2 hours per day. Adjust my roadmap.',
  'What should I do this week?',
  'Which career suits me better?',
  'I want to switch to data science.',
]

export default function AIChat() {
  const { sendChatMessage, chatHistory, analysisResult, profile } = useApp()
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const bottomRef = useRef(null)
  const navigate = useNavigate()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory, sending])

  async function handleSend(msg = input.trim()) {
    if (!msg || sending) return
    setInput('')
    setSending(true)
    try {
      await sendChatMessage(msg)
    } catch {
      // error handled in context
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="chat-page">
      <div className="chat-sidebar">
        <div className="chat-sidebar-header">
          <div className="chat-agent-avatar">🤖</div>
          <div>
            <div className="chat-agent-name">CareerPilot Agent</div>
            <div className="chat-agent-status">
              <span className="status-dot" />
              Powered by IBM Granite
            </div>
          </div>
        </div>

        {profile && (
          <div className="chat-profile-summary">
            <div className="cps-name">{profile.name}</div>
            <div className="cps-degree">{profile.degree} · {profile.branch}</div>
            <div className="cps-goal">Goal: {analysisResult?.top_career || profile.career_goals?.split('.')[0]}</div>
          </div>
        )}

        <div className="quick-prompts-section">
          <div className="qp-label">Quick Prompts</div>
          {QUICK_PROMPTS.map(p => (
            <button key={p} className="quick-prompt-btn" onClick={() => handleSend(p)}>
              {p}
            </button>
          ))}
        </div>

        {!profile && (
          <div className="chat-no-profile">
            <p>Complete an assessment for personalized responses.</p>
            <button className="btn btn-primary btn-sm" onClick={() => navigate('/assessment')}>
              Start Assessment
            </button>
          </div>
        )}
      </div>

      <div className="chat-main">
        <div className="chat-header">
          <h1>💬 CareerPilot Agent</h1>
          <p>Ask me anything about your career, skills, roadmap, or learning plan.</p>
        </div>

        <div className="chat-messages">
          {chatHistory.length === 0 && (
            <div className="chat-welcome">
              <div className="chat-welcome-icon">🚀</div>
              <h2>How can I help your career today?</h2>
              <p>Ask me about career paths, skill gaps, roadmaps, or specific advice tailored to your profile.</p>
            </div>
          )}

          {chatHistory.map((msg, i) => (
            <div key={i} className={`message ${msg.role === 'user' ? 'message-user' : 'message-agent'}`}>
              {msg.role === 'assistant' && (
                <div className="message-avatar">🤖</div>
              )}
              <div className="message-body">
                <div className="message-text">{msg.content}</div>
                {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                  <div className="message-actions">
                    {msg.suggested_actions.map((action, j) => (
                      <button key={j} className="message-action-btn" onClick={() => handleSend(action)}>
                        {action}
                      </button>
                    ))}
                  </div>
                )}
                <div className="message-time">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))}

          {sending && (
            <div className="message message-agent">
              <div className="message-avatar">🤖</div>
              <div className="message-body">
                <div className="typing-indicator">
                  <span /><span /><span />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        <div className="chat-input-area">
          <div className="chat-input-wrap">
            <input
              className="chat-input"
              placeholder="Ask CareerPilot Agent anything..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend()}
              disabled={sending}
            />
            <button
              className="chat-send-btn"
              onClick={() => handleSend()}
              disabled={!input.trim() || sending}
            >
              {sending ? <span className="spinner" style={{ width: 16, height: 16 }} /> : '→'}
            </button>
          </div>
          <p className="chat-disclaimer">
            Powered by IBM Granite · Responses based on your profile and conversation history
          </p>
        </div>
      </div>
    </div>
  )
}
