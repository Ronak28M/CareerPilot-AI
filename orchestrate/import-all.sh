#!/usr/bin/env bash
# ============================================================
# CareerPilot AI – Import all tools and agents into watsonx Orchestrate
# ============================================================

set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "===== CareerPilot AI – Importing into watsonx Orchestrate ====="

# Import Python tools
echo "--- Importing Python tools ---"
for tool in career_analyzer_tool.py skill_gap_tool.py roadmap_tool.py chat_tool.py comparison_tool.py progress_tool.py; do
  echo "  Importing tool: ${tool}"
  orchestrate tools import -k python -f "${SCRIPT_DIR}/tools/${tool}"
done

# Import agents
echo "--- Importing agents ---"
for agent in careerpilot_agent.yaml; do
  echo "  Importing agent: ${agent}"
  orchestrate agents import -f "${SCRIPT_DIR}/agents/${agent}"
done

echo "===== Import complete ====="
echo ""
echo "Next steps:"
echo "  1. Set environment variables in your .env file (see backend/.env.example)"
echo "  2. Start the backend:  cd backend && python app.py"
echo "  3. Start the frontend: cd frontend && npm run dev"
echo "  4. Open http://localhost:5173 in your browser"
