"""
Career Comparison Tool – Compares multiple career paths for a student.
"""

import json
import os
import requests
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class CareerComparisonInput(BaseModel):
    """Input for career comparison."""
    careers: str = Field(description="Comma-separated list of careers to compare (2-3 careers)")
    current_skills: str = Field(description="Student's current skills")
    student_profile_json: str = Field(default="", description="Full student profile as JSON string")


class CareerComparisonResult(BaseModel):
    """Result of career comparison."""
    raw_comparison: str = Field(description="JSON string with comparison data")
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
def compare_careers(input: CareerComparisonInput) -> CareerComparisonResult:
    """
    Compare multiple career paths for a student based on their skills and profile.

    Args:
        input (CareerComparisonInput): Careers to compare and student's current skills.

    Returns:
        CareerComparisonResult: Detailed comparison of career paths.
    """
    api_key = os.environ.get("WATSONX_API_KEY", "")
    project_id = os.environ.get("WATSONX_PROJECT_ID", "3e8ed057-d249-4d0e-98aa-d0de87976a52")

    career_list = [c.strip() for c in input.careers.split(",")]

    prompt = f"""You are a career comparison expert. Compare these career paths for a student.

Careers to compare: {", ".join(career_list)}
Student's current skills: {input.current_skills}

Return ONLY a valid JSON object (no markdown):
{{
  "comparisons": [
    {{
      "career_name": "",
      "match_score": 0,
      "required_skills": [],
      "existing_matching_skills": [],
      "skill_gaps": [],
      "learning_difficulty": "easy|moderate|hard",
      "time_to_job_ready": "",
      "avg_salary_range": "",
      "job_demand": "high|medium|low",
      "suggested_projects": [],
      "job_roles": [],
      "pros": [],
      "cons": []
    }}
  ],
  "recommended_career": "",
  "recommendation_reason": "",
  "comparison_summary": ""
}}"""

    try:
        raw = _call_granite(prompt, api_key, project_id)
        json.loads(raw)
        return CareerComparisonResult(raw_comparison=raw, status="success")
    except Exception as exc:
        return CareerComparisonResult(
            raw_comparison=json.dumps({"error": str(exc)}), status="error"
        )
