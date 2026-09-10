"""
Chat service – context-aware career counseling chat using IBM Granite.
"""

import json
import logging
from services.granite_service import call_granite

logger = logging.getLogger(__name__)


def handle_chat(message: str, profile: dict, history: list, current_goal: str = "") -> dict:
    """
    Handle a career counseling chat message.

    Args:
        message: Student's message.
        profile: Student profile dict.
        history: List of previous messages [{role, content}].
        current_goal: Student's current career goal.

    Returns:
        dict with response and suggested_actions.
    """
    # Build profile context
    profile_ctx = ""
    if profile:
        profile_ctx = f"""
Student Context:
- Name: {profile.get('name', 'Student')}
- Degree: {profile.get('degree', '')} in {profile.get('branch', '')}
- Year: {profile.get('year', '')} | CGPA: {profile.get('cgpa', '')}
- Technical Skills: {profile.get('technical_skills', '')}
- Soft Skills: {profile.get('soft_skills', '')}
- Interests: {profile.get('interests', '')}
- Career Goal: {profile.get('career_goals', '')}
- Learning Hours/Day: {profile.get('learning_hours', '')}
- Projects: {profile.get('projects', '')}
- Certifications: {profile.get('certifications', '')}
"""

    # Build conversation history context (last 4 messages)
    history_ctx = ""
    if history:
        history_ctx = "\nRecent conversation:\n"
        for msg in history[-4:]:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            history_ctx += f"{role}: {content}\n"

    system = (
        "You are CareerPilot Agent, an expert AI career counselor for college students. "
        "You provide personalized, specific, actionable career guidance. "
        "Be encouraging, concise, and helpful. Respond in 3-5 sentences maximum."
    )

    prompt = f"""{profile_ctx}
Current Career Goal: {current_goal}
{history_ctx}
Student question: {message}

Provide a helpful, specific, personalized career counseling response:"""

    try:
        response_text = call_granite(prompt, max_tokens=500, system_prompt=system).strip()
        # Clean up any trailing incomplete sentences
        if response_text and not response_text[-1] in ".!?":
            last_period = max(
                response_text.rfind("."), response_text.rfind("!"), response_text.rfind("?")
            )
            if last_period > 0:
                response_text = response_text[: last_period + 1]

        # Generate suggested follow-up actions
        actions = _get_suggested_actions(message, response_text)

        return {
            "response": response_text,
            "suggested_actions": actions,
            "status": "success",
        }
    except Exception as exc:
        logger.error(f"Chat error: {exc}")
        return {
            "response": "I'm having trouble connecting right now. Please try again in a moment.",
            "suggested_actions": ["View my roadmap", "Check skill gaps", "Compare careers"],
            "status": "error",
        }


def _get_suggested_actions(message: str, response: str) -> list:
    """Generate contextual suggested actions based on the conversation."""
    msg_lower = message.lower()
    if "switch" in msg_lower or "change" in msg_lower:
        return ["Reassess my career", "Compare new career paths", "Update my roadmap"]
    if "skill" in msg_lower or "learn" in msg_lower:
        return ["View skill gap analysis", "Update my roadmap", "Find learning resources"]
    if "project" in msg_lower:
        return ["View recommended projects", "Update my progress", "Get more project ideas"]
    if "ready" in msg_lower or "job" in msg_lower:
        return ["Check career readiness", "View full roadmap", "Update progress tracker"]
    if "roadmap" in msg_lower:
        return ["View my roadmap", "Update progress", "Get a new roadmap"]
    return ["View my roadmap", "Check skill gaps", "Compare career paths"]
