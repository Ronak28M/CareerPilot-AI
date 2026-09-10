"""
Career Chat Tool – Handles contextual conversation with IBM Granite.
"""

import json
import os
import requests
from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class ChatInput(BaseModel):
    """Input for the career chat tool."""
    message: str = Field(description="The student's message or question")
    student_profile_json: Optional[str] = Field(
        default="", description="JSON string of student profile for context"
    )
    conversation_history: Optional[str] = Field(
        default="", description="Previous conversation history as JSON array"
    )
    current_career_goal: Optional[str] = Field(
        default="", description="Student's current career goal"
    )


class ChatResult(BaseModel):
    """Result from career chat."""
    response: str = Field(description="CareerPilot Agent's response")
    status: str = Field(description="success or error")
    suggested_actions: str = Field(description="JSON array of suggested next actions")


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
            "max_tokens": 800,
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
def career_chat(input: ChatInput) -> ChatResult:
    """
    Handle a conversational career counseling message using IBM Granite.

    Args:
        input (ChatInput): The student's message and contextual information.

    Returns:
        ChatResult: Personalized career advice response.
    """
    api_key = os.environ.get("WATSONX_API_KEY", "")
    project_id = os.environ.get("WATSONX_PROJECT_ID", "3e8ed057-d249-4d0e-98aa-d0de87976a52")

    # Build context
    profile_ctx = ""
    if input.student_profile_json:
        try:
            profile = json.loads(input.student_profile_json)
            profile_ctx = f"""
Student Context:
- Name: {profile.get('name', 'Student')}
- Degree: {profile.get('degree', '')} in {profile.get('branch', '')}
- Skills: {profile.get('technical_skills', '')}
- Career Goal: {profile.get('career_goals', '')}
- Learning Hours/Day: {profile.get('learning_hours', '')}
"""
        except Exception:
            profile_ctx = ""

    history_ctx = ""
    if input.conversation_history:
        try:
            history = json.loads(input.conversation_history)
            if history:
                history_ctx = "\nPrevious conversation:\n"
                for msg in history[-4:]:  # last 4 exchanges
                    role = msg.get("role", "")
                    content = msg.get("content", "")
                    history_ctx += f"{role.capitalize()}: {content}\n"
        except Exception:
            history_ctx = ""

    prompt = f"""You are CareerPilot Agent, an expert AI career counselor for college students.
You provide personalized, actionable career advice.
{profile_ctx}
{history_ctx}
Current Career Goal: {input.current_career_goal}

Student: {input.message}

CareerPilot Agent (provide a helpful, specific, personalized response in 3-5 sentences. Be direct and actionable):"""

    try:
        response_text = _call_granite(prompt, api_key, project_id).strip()

        # Generate suggested actions
        actions_prompt = f"""Based on this career counseling conversation, suggest 3 next actions as a JSON array.
Student question: {input.message}
Response given: {response_text[:200]}

Return ONLY a JSON array of strings like: ["Action 1", "Action 2", "Action 3"]"""

        try:
            actions_raw = _call_granite(actions_prompt, api_key, project_id)
            # Try to extract JSON array
            start = actions_raw.find("[")
            end = actions_raw.rfind("]") + 1
            if start >= 0 and end > start:
                actions_json = actions_raw[start:end]
                json.loads(actions_json)
            else:
                actions_json = '["Review your roadmap", "Practice a new skill", "Work on a project"]'
        except Exception:
            actions_json = '["Review your roadmap", "Practice a new skill", "Work on a project"]'

        return ChatResult(response=response_text, status="success", suggested_actions=actions_json)
    except Exception as exc:
        return ChatResult(
            response="I apologize, I encountered an issue. Please try again.",
            status="error",
            suggested_actions='[]',
        )
