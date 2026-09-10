import React, { createContext, useContext, useState, useCallback } from 'react'
import api from '../services/api'
import toast from 'react-hot-toast'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [profile, setProfile] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [progressData, setProgressData] = useState({
    completedSkills: [],
    completedProjects: [],
    completedCertifications: [],
    overallProgress: 0,
    currentPhase: 'phase_1',
  })

  const submitProfile = useCallback(async (profileData) => {
    setIsAnalyzing(true)
    try {
      const result = await api.analyzeCareer(profileData)
      setProfile(profileData)
      setAnalysisResult(result)
      toast.success('Career analysis complete!')
      return result
    } catch (err) {
      toast.error(err.message || 'Career analysis failed. Please try again.')
      throw err
    } finally {
      setIsAnalyzing(false)
    }
  }, [])

  const sendChatMessage = useCallback(async (message) => {
    const userMsg = { role: 'user', content: message, timestamp: new Date().toISOString() }
    const updatedHistory = [...chatHistory, userMsg]
    setChatHistory(updatedHistory)

    try {
      const result = await api.chat({
        message,
        profile: profile || {},
        history: updatedHistory.slice(-8),
        current_goal: analysisResult?.top_career || '',
      })
      const agentMsg = {
        role: 'assistant',
        content: result.response,
        suggested_actions: result.suggested_actions || [],
        timestamp: new Date().toISOString(),
      }
      setChatHistory(prev => [...prev, agentMsg])
      return agentMsg
    } catch (err) {
      toast.error('Chat unavailable. Please try again.')
      throw err
    }
  }, [chatHistory, profile, analysisResult])

  const updateProgress = useCallback(async (updates) => {
    const newProgress = { ...progressData, ...updates }
    setProgressData(newProgress)

    try {
      const result = await api.updateProgress({
        student_name: profile?.name || 'Student',
        target_career: analysisResult?.top_career || '',
        completed_skills: newProgress.completedSkills,
        completed_projects: newProgress.completedProjects,
        completed_certifications: newProgress.completedCertifications,
        current_phase: newProgress.currentPhase,
        overall_progress_percent: newProgress.overallProgress,
        new_goal: updates.newGoal || '',
      })
      toast.success('Progress updated! Getting new recommendations...')
      return result
    } catch (err) {
      toast.error('Could not update progress. Please try again.')
      throw err
    }
  }, [progressData, profile, analysisResult])

  const compareCareerPaths = useCallback(async (careers) => {
    try {
      return await api.compareCareers({ careers, profile: profile || {} })
    } catch (err) {
      toast.error('Career comparison failed. Please try again.')
      throw err
    }
  }, [profile])

  const loadDemoProfile = useCallback(async () => {
    const demo = {
      name: 'Priya Sharma',
      degree: 'B.Tech',
      branch: 'Computer Science',
      year: '2nd Year',
      cgpa: '7.8',
      technical_skills: 'HTML, CSS, JavaScript (Basic), Python (Beginner), UI/UX Basics',
      soft_skills: 'Communication, Teamwork, Creativity, Problem Solving',
      interests: 'Web Design, Data Visualization, User Experience, Technology',
      favorite_subjects: 'Web Technologies, Data Structures, Design Thinking',
      career_goals: 'Become a Frontend Developer or Data Analyst within 1 year',
      preferred_domain: 'Frontend Development, Data Analytics, UI/UX',
      short_term_goal: 'Build a strong portfolio with 3 real projects',
      long_term_goal: 'Work at a product company as a senior developer',
      projects: 'Personal blog website (HTML/CSS), Simple Python calculator',
      certifications: 'HTML/CSS Basics (freeCodeCamp)',
      internships: 'None yet',
      learning_hours: '2',
      learning_style: 'Visual and hands-on',
    }
    return submitProfile(demo)
  }, [submitProfile])

  return (
    <AppContext.Provider
      value={{
        profile,
        setProfile,
        analysisResult,
        setAnalysisResult,
        isAnalyzing,
        chatHistory,
        progressData,
        submitProfile,
        sendChatMessage,
        updateProgress,
        compareCareerPaths,
        loadDemoProfile,
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used inside AppProvider')
  return ctx
}
