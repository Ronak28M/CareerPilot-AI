"""
Career Analyzer Tool – Calls IBM Granite via watsonx.ai to analyze a student profile
and return structured career recommendations.
"""

import json
import os
import requests
from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


# ---------------------------------------------------------------------------
# Input / Output schemas
# ---------------------------------------------------------------------------

class StudentProfile(BaseModel):
    """Complete student profile for career analysis."""
    name: str = Field(description="Student's full name")
    degree: str = Field(description="Degree program (e.g. B.Tech, B.Sc)")
    branch: str = Field(description="Branch / specialization")
    year: str = Field(description="Current year of study")
    cgpa: str = Field(description="CGPA or academic performance")
    technical_skills: str = Field(description="Comma-separated technical skills")
    soft_skills: str = Field(description="Comma-separated soft skills")
    interests: str = Field(description="Areas of interest")
    career_goals: str = Field(description="Short and long-term career goals")
    projects: str = Field(description="Projects completed")
    certifications: str = Field(description="Certifications obtained")
    learning_hours: str = Field(description="Available learning hours per day")
    preferred_domain: Optional[str] = Field(default="", description="Preferred career domain")


class CareerAnalysisResult(BaseModel):
    """Structured result from career analysis."""
    raw_analysis: str = Field(description="JSON string with full career analysis")
    status: str = Field(description="success or error")


# ---------------------------------------------------------------------------
# Helper: get IBM Granite auth token
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------

@tool(permission=ToolPermission.READ_ONLY)
def analyze_student_career(profile: StudentProfile) -> CareerAnalysisResult:
    """
    Analyze a student's profile using IBM Granite and generate career recommendations.

    Args:
        profile (StudentProfile): The complete student profile data.

    Returns:
        CareerAnalysisResult: Structured career analysis with recommendations.
    """
    api_key = os.environ.get("WATSONX_API_KEY", "")
    project_id = os.environ.get("WATSONX_PROJECT_ID", "3e8ed057-d249-4d0e-98aa-d0de87976a52")

    prompt = f"""You are CareerPilot AI, an expert career counselor for college students.

Analyze the following student profile and respond ONLY with a valid JSON object (no markdown, no explanation):

Student Profile:
- Name: {profile.name}
- Degree: {profile.degree}
- Branch: {profile.branch}
- Year: {profile.year}
- CGPA: {profile.cgpa}
- Technical Skills: {profile.technical_skills}
- Soft Skills: {profile.soft_skills}
- Interests: {profile.interests}
- Career Goals: {profile.career_goals}
- Projects: {profile.projects}
- Certifications: {profile.certifications}
- Learning Hours/Day: {profile.learning_hours}
- Preferred Domain: {profile.preferred_domain}

Return JSON with this exact structure:
{{
  "career_recommendations": [
    {{
      "career_name": "",
      "match_percentage": 0,
      "why_it_matches": "",
      "existing_skills": [],
      "missing_skills": [],
      "skills_to_learn": [],
      "job_roles": [],
      "recommended_projects": [],
      "recommended_certifications": [],
      "next_steps": []
    }}
  ],
  "current_skills": [],
  "skill_gaps": [],
  "priority_skills": [],
  "next_action": ""
}}

Provide exactly 3 career recommendations ranked by match percentage."""

    try:
        raw = _call_granite(prompt, api_key, project_id)
        # Validate JSON parse
        json.loads(raw)
        return CareerAnalysisResult(raw_analysis=raw, status="success")
    except Exception as exc:
        return CareerAnalysisResult(raw_analysis=json.dumps({"error": str(exc)}), status="error")
