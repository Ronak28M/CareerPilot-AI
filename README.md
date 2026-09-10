# CareerPilot AI
## Agentic Career Counseling Companion
### AICTE 2026 Problem Statement No. 15

> *"Your AI-powered path to a future-ready career"*

---

## Problem Statement

**AICTE 2026 Problem Statement No. 15: Agentic Career Counseling Companion**

College students often struggle to make informed career decisions because they lack:
- Personalised guidance based on their unique skills and interests
- Understanding of current industry demands and skill gaps
- A clear, actionable learning roadmap
- A system that adapts as their goals and skills evolve

CareerPilot AI addresses all of these through an **Agentic AI** approach powered by IBM Granite and watsonx Orchestrate.

---

## Objective

Build an intelligent, adaptive career counseling system that:
1. Analyzes student academic background, skills, interests, and goals
2. Recommends personalized career paths with match percentages
3. Performs detailed skill gap analysis
4. Generates a time-bounded, adaptive learning roadmap
5. Provides ongoing, context-aware career chat
6. Adapts all recommendations when student progress or goals change

---

## Features

| Feature | Description |
|---------|-------------|
| 🎯 Career Assessment | Multi-section form collecting academic, skill, interest, and goal data |
| 🤖 AI Career Analysis | IBM Granite analyzes profile via watsonx Orchestrate agent workflow |
| 📊 Career Recommendations | Top 3 career paths with match %, reasons, skill gaps, and next steps |
| 💻 Skill Gap Analysis | Visual skill proficiency bars, missing skills, priority learning list |
| 🗺️ Career Roadmap | Personalized 12-month plan in 3 phases (0–3, 3–6, 6–12 months) |
| ⚖️ Career Comparison | Side-by-side comparison of 2–3 career paths |
| 💬 AI Career Chat | Conversational agent with profile and history context |
| 📈 Progress Tracker | Mark skills/projects/certs complete; AI adapts recommendations |
| 🏠 Student Dashboard | Complete career overview with quick actions |
| 🧪 Demo Profile | One-click demo with realistic student profile |

---

## Agentic AI Architecture

```
Student Profile Input
        ↓
Career Profile Analyzer (IBM Granite)
        ↓
Skill Gap Analyzer (IBM Granite)
        ↓
Career Recommendation Agent (IBM Granite)
        ↓
Career Roadmap Generator (IBM Granite)
        ↓
Project & Certification Agent (IBM Granite)
        ↓
CareerPilot Agent Response (watsonx Orchestrate)
```

### watsonx Orchestrate Role
- Coordinates the multi-agent workflow via the `careerpilot_agent`
- Manages tool orchestration (career analyzer, skill gap, roadmap, chat, comparison, progress)
- Provides the chat interface via the built-in watsonx Orchestrate chat UI

### IBM Granite Role
- Primary LLM for all reasoning and generation tasks
- Model: `ibm/granite-4-h-small`
- Handles: career analysis, skill gap analysis, roadmap generation, career comparison, chat responses, progress-based recommendations

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite |
| Backend | Python + Flask |
| AI Model | IBM Granite (`ibm/granite-4-h-small`) |
| AI Platform | IBM watsonx.ai |
| Agent Orchestration | IBM watsonx Orchestrate |
| Cloud | IBM Cloud |

---

## Project Structure

```
careerpilot-ai/
├── orchestrate/
│   ├── agents/
│   │   └── careerpilot_agent.yaml     # watsonx Orchestrate agent
│   ├── tools/
│   │   ├── career_analyzer_tool.py    # Career analysis tool
│   │   ├── skill_gap_tool.py          # Skill gap analysis tool
│   │   ├── roadmap_tool.py            # Roadmap generation tool
│   │   ├── chat_tool.py               # Career chat tool
│   │   ├── comparison_tool.py         # Career comparison tool
│   │   └── progress_tool.py           # Progress update tool
│   └── import-all.sh                  # Import script for orchestrate CLI
│
├── backend/
│   ├── app.py                         # Flask application entry point
│   ├── routes/
│   │   ├── career_routes.py           # POST /api/analyze-career
│   │   ├── chat_routes.py             # POST /api/chat
│   │   ├── comparison_routes.py       # POST /api/compare-careers
│   │   └── progress_routes.py         # POST /api/update-progress
│   ├── services/
│   │   ├── granite_service.py         # IBM Granite API client
│   │   ├── career_service.py          # Career analysis orchestration
│   │   ├── chat_service.py            # Chat logic
│   │   ├── comparison_service.py      # Career comparison logic
│   │   └── progress_service.py        # Progress update logic
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Landing.jsx            # Landing page
    │   │   ├── Assessment.jsx         # Multi-section assessment form
    │   │   ├── Dashboard.jsx          # Student dashboard
    │   │   ├── CareerRecommendations.jsx
    │   │   ├── SkillGapAnalysis.jsx
    │   │   ├── CareerRoadmap.jsx
    │   │   ├── CareerComparison.jsx
    │   │   ├── AIChat.jsx             # Career chat interface
    │   │   └── ProgressTracker.jsx
    │   ├── components/
    │   │   └── Navbar.jsx
    │   ├── context/
    │   │   └── AppContext.jsx         # Global state management
    │   ├── services/
    │   │   └── api.js                 # Axios API client
    │   └── styles/
    │       └── index.css
    ├── package.json
    └── vite.config.js
```

---

## Installation & Setup

### Prerequisites
- Node.js 18+
- Python 3.9+
- IBM watsonx.ai credentials (project ID + API key)

### 1. Clone / Setup

```bash
cd careerpilot-ai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# or: venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your IBM credentials
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. watsonx Orchestrate (Optional – for agent UI)

```bash
cd orchestrate
chmod +x import-all.sh
./import-all.sh
```

---

## Configuration

Create `backend/.env` from `.env.example`:

```env
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
PORT=5000
FLASK_DEBUG=false
```

**Security**: Never commit `.env` to version control. Credentials are loaded server-side only.

---

## Running the Application

### Start Backend

```bash
cd backend
source venv/bin/activate
python app.py
# Backend runs at http://localhost:5000
```

### Start Frontend

```bash
cd frontend
npm run dev
# Frontend runs at http://localhost:5173
```

Open **http://localhost:5173** in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze-career` | Full career analysis (recommendations + skill gap + roadmap) |
| POST | `/api/chat` | Career counseling chat message |
| POST | `/api/compare-careers` | Compare 2–3 career paths |
| POST | `/api/update-progress` | Update progress and get new recommendations |
| GET | `/api/health` | Health check |

---

## Demo Instructions

1. Open http://localhost:5173
2. Click **"Try Demo Profile"** on the landing page
3. The AI will automatically analyze a pre-built student profile
4. Explore: Dashboard → Career Recommendations → Skill Gap → Roadmap → Chat
5. Try asking the chat: *"I want to switch to data science"* to see adaptive recommendations

---

## Future Enhancements

- Real-time job market API integration (LinkedIn, Indeed)
- Personalized learning resource recommendations (Coursera, Udemy)
- Peer comparison and benchmarking
- Email/calendar reminders for roadmap tasks
- Voice-enabled chat using IBM Watson Speech
- Alumni network matching
- Resume analysis and ATS scoring

---

*Built with IBM Granite · IBM watsonx Orchestrate · IBM Cloud*
*AICTE 2026 Problem Statement No. 15 – Agentic Career Counseling Companion*
