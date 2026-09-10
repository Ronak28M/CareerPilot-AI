import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AppProvider } from './context/AppContext'
import Landing from './pages/Landing'
import Assessment from './pages/Assessment'
import Dashboard from './pages/Dashboard'
import CareerRecommendations from './pages/CareerRecommendations'
import SkillGapAnalysis from './pages/SkillGapAnalysis'
import CareerRoadmap from './pages/CareerRoadmap'
import CareerComparison from './pages/CareerComparison'
import AIChat from './pages/AIChat'
import ProgressTracker from './pages/ProgressTracker'
import Navbar from './components/Navbar'

export default function App() {
  return (
    <AppProvider>
      <Router>
        <Toaster position="top-right" toastOptions={{ duration: 4000 }} />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/assessment" element={<Assessment />} />
          <Route
            path="/dashboard"
            element={<><Navbar /><Dashboard /></>}
          />
          <Route
            path="/recommendations"
            element={<><Navbar /><CareerRecommendations /></>}
          />
          <Route
            path="/skill-gap"
            element={<><Navbar /><SkillGapAnalysis /></>}
          />
          <Route
            path="/roadmap"
            element={<><Navbar /><CareerRoadmap /></>}
          />
          <Route
            path="/comparison"
            element={<><Navbar /><CareerComparison /></>}
          />
          <Route
            path="/chat"
            element={<><Navbar /><AIChat /></>}
          />
          <Route
            path="/progress"
            element={<><Navbar /><ProgressTracker /></>}
          />
        </Routes>
      </Router>
    </AppProvider>
  )
}
