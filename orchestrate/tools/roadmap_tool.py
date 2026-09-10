"""
Career Roadmap Generator Tool – Creates a personalised 12-month learning roadmap.
"""

import json
import os
import requests
from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class RoadmapInput(BaseModel):
    """Input for roadmap generation."""
    student_name: str = Field(description="Student's name")
    target_career: str = Field(description="Target career path")
    current_skills: str = Field(description="Current skills with proficiency")
    missing_skills: str = Field(description="Skills that need to be learned")
    learning_hours: str = Field(description="Available learning hours per day")
    degree_branch: str = Field(description="Degree and branch of study")
    goals: Optional[str] = Field(default="", description="Short and long-term goals")


class RoadmapResult(BaseModel):
    """Result of roadmap generation."""
    raw_roadmap: str = Field(description="JSON string with personalised roadmap")
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
            "max_tokens": 2000,
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


@tool(permission=ToolPermission.READ_ONLY)
def generate_career_roadmap(input: RoadmapInput) -> RoadmapResult:
    """
    Generate a personalised 12-month career learning roadmap using IBM Granite.

    Args:
        input (RoadmapInput): Student profile information for roadmap generation.

    Returns:
        RoadmapResult: Structured roadmap divided into three phases.
    """
    api_key = os.environ.get("WATSONX_API_KEY", "")
    project_id = os.environ.get("WATSONX_PROJECT_ID", "3e8ed057-d249-4d0e-98aa-d0de87976a52")

    prompt = f"""You are an expert career roadmap planner. Create a personalised learning roadmap.

Student: {input.student_name}
Target Career: {input.target_career}
Current Skills: {input.current_skills}
Missing Skills: {input.missing_skills}
Learning Hours/Day: {input.learning_hours}
Degree/Branch: {input.degree_branch}
Goals: {input.goals}

Generate a realistic roadmap based on available learning time ({input.learning_hours} hours/day).
Return ONLY a valid JSON object (no markdown):
{{
  "phase_1": {{
    "duration": "0-3 months",
    "focus": "",
    "skills_to_learn": [],
    "topics": [],
    "practice_activities": [],
    "projects": [],
    "certifications": [],
    "expected_outcome": "",
    "weekly_hours": 0
  }},
  "phase_2": {{
    "duration": "3-6 months",
    "focus": "",
    "skills_to_learn": [],
    "topics": [],
    "practice_activities": [],
    "projects": [],
    "certifications": [],
    "expected_outcome": "",
    "weekly_hours": 0
  }},
  "phase_3": {{
    "duration": "6-12 months",
    "focus": "",
    "skills_to_learn": [],
    "topics": [],
    "practice_activities": [],
    "projects": [],
    "certifications": [],
    "expected_outcome": "",
    "weekly_hours": 0
  }},
  "total_duration": "12 months",
  "immediate_next_action": ""
}}"""

    try:
        raw = _call_granite(prompt, api_key, project_id)
        json.loads(raw)
        return RoadmapResult(raw_roadmap=raw, status="success")
    except Exception as exc:
        return RoadmapResult(raw_roadmap=json.dumps({"error": str(exc)}), status="error")
