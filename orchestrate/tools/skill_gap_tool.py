"""
Skill Gap Analyzer Tool – Uses IBM Granite to produce a detailed skill-gap analysis.
"""

import json
import os
import requests
from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class SkillGapInput(BaseModel):
    """Input for skill-gap analysis."""
    current_skills: str = Field(description="Comma-separated list of current skills with optional proficiency")
    target_career: str = Field(description="Target career path the student wants to pursue")
    degree: str = Field(description="Student's degree and branch")
    experience_level: Optional[str] = Field(default="beginner", description="Student's experience level")


class SkillGapResult(BaseModel):
    """Result of skill-gap analysis."""
    raw_analysis: str = Field(description="JSON string with skill gap details")
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
            "max_tokens": 1500,
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
def analyze_skill_gaps(input: SkillGapInput) -> SkillGapResult:
    """
    Analyze skill gaps between a student's current skills and their target career.

    Args:
        input (SkillGapInput): Current skills and target career information.

    Returns:
        SkillGapResult: Detailed skill gap analysis with priorities.
    """
    api_key = os.environ.get("WATSONX_API_KEY", "")
    project_id = os.environ.get("WATSONX_PROJECT_ID", "3e8ed057-d249-4d0e-98aa-d0de87976a52")

    prompt = f"""You are a technical skills analyst. Analyze skill gaps for a student.

Current Skills: {input.current_skills}
Target Career: {input.target_career}
Degree/Branch: {input.degree}
Experience Level: {input.experience_level}

Return ONLY a valid JSON object (no markdown):
{{
  "strong_skills": [{{"name": "", "proficiency": 0, "relevance": ""}}],
  "beginner_skills": [{{"name": "", "proficiency": 0, "action": ""}}],
  "missing_skills": [{{"name": "", "importance": "critical|high|medium", "learning_time": ""}}],
  "priority_skills": [],
  "skill_match_percentage": 0,
  "analysis_summary": ""
}}

Proficiency is a percentage 0-100. skill_match_percentage is overall match for target career."""

    try:
        raw = _call_granite(prompt, api_key, project_id)
        json.loads(raw)
        return SkillGapResult(raw_analysis=raw, status="success")
    except Exception as exc:
        return SkillGapResult(raw_analysis=json.dumps({"error": str(exc)}), status="error")
