"""
Comparison service – compares multiple career paths.
"""

import logging
from services.granite_service import call_granite_json

logger = logging.getLogger(__name__)


def compare_careers(careers: list, profile: dict) -> dict:
    """
    Compare multiple career paths for a student.

    Args:
        careers: List of career names to compare.
        profile: Student profile dict.

    Returns:
        Comparison result dict.
    """
    careers_str = ", ".join(careers)
    skills = profile.get("technical_skills", "")

    prompt = f"""You are a career comparison expert for college students.
Compare these career paths for a student.

Careers: {careers_str}
Student Skills: {skills}
Degree: {profile.get('degree', '')} in {profile.get('branch', '')}

Return ONLY a valid JSON object:
{{
  "comparisons": [
    {{
      "career_name": "",
      "match_score": 75,
      "required_skills": [],
      "existing_matching_skills": [],
      "skill_gaps": [],
      "learning_difficulty": "moderate",
      "time_to_job_ready": "6-9 months",
      "avg_salary_range": "$60k - $90k",
      "job_demand": "high",
      "suggested_projects": [],
      "job_roles": [],
      "pros": [],
      "cons": []
    }}
  ],
  "recommended_career": "",
  "recommendation_reason": "",
  "comparison_summary": ""
}}

Include one comparison object for each career. learning_difficulty: easy/moderate/hard. job_demand: high/medium/low."""

    result = call_granite_json(prompt, max_tokens=2500)

    if "error" in result and "comparisons" not in result:
        result = _fallback_comparison(careers, skills)

    return result


def _fallback_comparison(careers: list, skills: str) -> dict:
    """Fallback comparison data."""
    comparisons = []
    difficulties = ["moderate", "easy", "hard"]
    demands = ["high", "high", "medium"]
    scores = [75, 65, 55]

    for i, career in enumerate(careers):
        comparisons.append({
            "career_name": career,
            "match_score": scores[i % len(scores)],
            "required_skills": ["JavaScript", "React", "CSS", "HTML"],
            "existing_matching_skills": skills.split(",")[:2] if skills else [],
            "skill_gaps": ["React", "TypeScript"],
            "learning_difficulty": difficulties[i % len(difficulties)],
            "time_to_job_ready": "6-9 months",
            "avg_salary_range": "$55k - $85k",
            "job_demand": demands[i % len(demands)],
            "suggested_projects": ["Portfolio project", "Practice app"],
            "job_roles": [f"Junior {career}", f"{career} Intern"],
            "pros": ["Growing field", "Good salary", "Remote work possible"],
            "cons": ["Competitive market", "Constant learning required"],
        })

    return {
        "comparisons": comparisons,
        "recommended_career": careers[0] if careers else "",
        "recommendation_reason": "Based on your current skill set, this path requires the least ramp-up time.",
        "comparison_summary": "All paths are viable. Choose based on your strongest interest.",
    }
