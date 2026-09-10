"""
Progress Update Tool – Re-evaluates recommendations when student updates progress.
"""

import json
import os
import requests
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class ProgressUpdateInput(BaseModel):
    """Input for progress-based recommendation update."""
    student_name: str = Field(description="Student's name")
    target_career: str = Field(description="Target career")
    completed_skills: str = Field(description="Comma-separated skills marked as completed")
    completed_projects: str = Field(description="Comma-separated projects completed")
    completed_certifications: str = Field(description="Comma-separated certifications completed")
    current_phase: str = Field(description="Current roadmap phase (phase_1, phase_2, phase_3)")
    overall_progress_percent: int = Field(description="Overall roadmap completion percentage 0-100")
    new_goal: str = Field(default="", description="Updated career goal if changed")


class ProgressUpdateResult(BaseModel):
    """Updated recommendations based on progress."""
    raw_update: str = Field(description="JSON string with updated guidance")
    status: str = Field(description="success or error")


def _get_iam_token(api_key: str) -> str:
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}",
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def _call_granite(prompt: str, api_key: str, project_id: str) -> str:
    token = _get_iam_token(api_key)
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
    payload = {
        "model_id": "ibm/granite-4-h-small",
        "project_id": project_id,
        "messages": [{"role": "user", "content": prompt}],
        "parameters": {
            "max_tokens": 1200,
            "temperature": 0.1,
        },
    }
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


@tool(permission=ToolPermission.READ_WRITE)
def update_progress_recommendations(input: ProgressUpdateInput) -> ProgressUpdateResult:
    """
    Generate updated career recommendations based on student's progress.

    Args:
        input (ProgressUpdateInput): Student's current progress data.

    Returns:
        ProgressUpdateResult: Updated guidance and next actions.
    """
    api_key = os.environ.get("WATSONX_API_KEY", "")
    project_id = os.environ.get("WATSONX_PROJECT_ID", "3e8ed057-d249-4d0e-98aa-d0de87976a52")

    goal_update = f"Note: Student wants to switch to: {input.new_goal}" if input.new_goal else ""

    prompt = f"""You are CareerPilot AI. A student has updated their progress. Provide updated guidance.

Student: {input.student_name}
Target Career: {input.target_career}
{goal_update}
Completed Skills: {input.completed_skills}
Completed Projects: {input.completed_projects}
Completed Certifications: {input.completed_certifications}
Current Phase: {input.current_phase}
Overall Progress: {input.overall_progress_percent}%

Return ONLY a valid JSON object (no markdown):
{{
  "progress_assessment": "",
  "next_immediate_action": "",
  "updated_priority_skills": [],
  "recommended_next_project": "",
  "recommended_next_certification": "",
  "motivational_message": "",
  "phase_completion_tips": [],
  "career_readiness_score": 0,
  "goal_change_impact": ""
}}

career_readiness_score is 0-100. goal_change_impact is empty string if no goal change."""

    try:
        raw = _call_granite(prompt, api_key, project_id)
        json.loads(raw)
        return ProgressUpdateResult(raw_update=raw, status="success")
    except Exception as exc:
        return ProgressUpdateResult(
            raw_update=json.dumps({"error": str(exc)}), status="error"
        )
