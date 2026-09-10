"""
Progress service – generates updated recommendations based on student progress.
"""

import logging
from services.granite_service import call_granite_json

logger = logging.getLogger(__name__)


def update_progress(progress_data: dict) -> dict:
    """
    Generate updated recommendations based on student's progress.

    Args:
        progress_data: Dict with completed items and current state.

    Returns:
        Updated guidance dict.
    """
    name = progress_data.get("student_name", "Student")
    target = progress_data.get("target_career", "")
    completed_skills = progress_data.get("completed_skills", [])
    completed_projects = progress_data.get("completed_projects", [])
    completed_certs = progress_data.get("completed_certifications", [])
    overall_progress = progress_data.get("overall_progress_percent", 0)
    new_goal = progress_data.get("new_goal", "")
    current_phase = progress_data.get("current_phase", "phase_1")

    goal_note = f"\nIMPORTANT: Student wants to switch career goal to: {new_goal}" if new_goal else ""

    prompt = f"""You are CareerPilot AI. A student has updated their learning progress.
{goal_note}
Student: {name}
Target Career: {target}
Completed Skills: {", ".join(completed_skills) if completed_skills else "None yet"}
Completed Projects: {", ".join(completed_projects) if completed_projects else "None yet"}
Completed Certifications: {", ".join(completed_certs) if completed_certs else "None yet"}
Current Phase: {current_phase}
Overall Progress: {overall_progress}%

Return ONLY a valid JSON object:
{{
  "progress_assessment": "",
  "next_immediate_action": "",
  "updated_priority_skills": [],
  "recommended_next_project": "",
  "recommended_next_certification": "",
  "motivational_message": "",
  "phase_completion_tips": [],
  "career_readiness_score": {overall_progress},
  "goal_change_impact": ""
}}

career_readiness_score is 0-100. goal_change_impact is empty if no goal change."""

    result = call_granite_json(prompt, max_tokens=1200)

    if "error" in result and "next_immediate_action" not in result:
        result = _fallback_progress_update(overall_progress, completed_skills, new_goal)

    return result


def _fallback_progress_update(progress: int, completed_skills: list, new_goal: str) -> dict:
    messages = [
        "Great start! Keep the momentum going.",
        "You're making solid progress. Stay consistent!",
        "Halfway there! You're doing amazing.",
        "Almost job-ready! Polish your portfolio now.",
        "Excellent work! You're ready for your first role.",
    ]
    idx = min(progress // 25, len(messages) - 1)

    return {
        "progress_assessment": f"You've completed {progress}% of your roadmap. " + messages[idx],
        "next_immediate_action": "Complete the next skill in your roadmap and build a small project to practice it.",
        "updated_priority_skills": ["React", "JavaScript ES6+", "Git"] if not completed_skills else [],
        "recommended_next_project": "Build a full CRUD app using your recently learned skills",
        "recommended_next_certification": "Meta Frontend Developer Professional Certificate",
        "motivational_message": messages[idx],
        "phase_completion_tips": [
            "Set a daily learning timer",
            "Document what you build on GitHub",
            "Practice with real project prompts",
        ],
        "career_readiness_score": progress,
        "goal_change_impact": f"Switching to {new_goal} will require learning new skills. Your foundation still applies!" if new_goal else "",
    }
