"""
Granite service – calls IBM watsonx.ai Granite model via the Chat API.
Credentials are loaded from environment variables only.
"""

import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

WATSONX_CHAT_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"
MODEL_ID = "ibm/granite-4-h-small"

# Cache token in module scope (per process)
_cached_token: dict = {"token": None, "expires_at": 0}


def _get_iam_token() -> str:
    """Retrieve a fresh IAM bearer token using the configured API key."""
    import time
    now = time.time()
    if _cached_token["token"] and now < _cached_token["expires_at"] - 60:
        return _cached_token["token"]

    api_key = os.environ.get("WATSONX_API_KEY", "")
    if not api_key:
        raise ValueError("WATSONX_API_KEY environment variable is not set")

    resp = requests.post(
        IAM_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}",
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    _cached_token["token"] = data["access_token"]
    _cached_token["expires_at"] = now + data.get("expires_in", 3600)
    return _cached_token["token"]


def call_granite(prompt: str, max_tokens: int = 2000, system_prompt: str = "") -> str:
    """
    Call IBM Granite model via the Chat API with the given prompt.

    Args:
        prompt: The user message / prompt string.
        max_tokens: Maximum tokens to generate.
        system_prompt: Optional system message.

    Returns:
        Generated text string.

    Raises:
        Exception on API errors.
    """
    project_id = os.environ.get("WATSONX_PROJECT_ID", "3e8ed057-d249-4d0e-98aa-d0de87976a52")
    token = _get_iam_token()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model_id": MODEL_ID,
        "project_id": project_id,
        "messages": messages,
        "parameters": {
            "max_tokens": min(max_tokens, 4096),
            "temperature": 0.1,
        },
    }

    resp = requests.post(
        WATSONX_CHAT_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    result = resp.json()
    generated = result["choices"][0]["message"]["content"]
    logger.debug(f"Granite response length: {len(generated)}")
    return generated


def call_granite_json(prompt: str, max_tokens: int = 2000, system_prompt: str = "") -> dict:
    """
    Call Granite and parse the JSON response. Falls back gracefully on parse errors.

    Args:
        prompt: The prompt that instructs Granite to return JSON.
        max_tokens: Maximum tokens.
        system_prompt: Optional system message.

    Returns:
        Parsed dict or error dict.
    """
    raw = ""
    try:
        raw = call_granite(prompt, max_tokens, system_prompt)
        raw = raw.strip()

        # Step 1: direct parse if raw is already valid JSON
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # Step 2: strip markdown code fences (```json ... ```)
        if "```" in raw:
            parts = raw.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{") or part.startswith("["):
                    try:
                        return json.loads(part)
                    except json.JSONDecodeError:
                        pass

        # Step 3: extract outermost { ... }
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = raw[start:end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # Step 4: repair truncated JSON
                repaired = _repair_json(json_str)
                if repaired:
                    try:
                        return json.loads(repaired)
                    except json.JSONDecodeError:
                        pass

        # Step 5: try JSON array
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(raw[start:end])
            except json.JSONDecodeError:
                pass

        logger.warning("Granite returned non-JSON response, using raw text")
        return {"raw_text": raw, "parse_error": True}
    except json.JSONDecodeError as exc:
        logger.error(f"JSON parse error from Granite: {exc}")
        return {"error": "Failed to parse AI response", "raw": raw[:500]}
    except Exception as exc:
        logger.error(f"Granite call error: {exc}")
        return {"error": str(exc)}


def _repair_json(json_str: str) -> str:
    """
    Attempt to repair truncated JSON by balancing brackets and quotes.
    Returns repaired string or empty string if not fixable.
    """
    try:
        stack = []
        in_string = False
        escaped = False

        for ch in json_str:
            if escaped:
                escaped = False
                continue
            if ch == '\\' and in_string:
                escaped = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if not in_string:
                if ch in ('{', '['):
                    stack.append(ch)
                elif ch == '}':
                    if stack and stack[-1] == '{':
                        stack.pop()
                elif ch == ']':
                    if stack and stack[-1] == '[':
                        stack.pop()

        # Close any open string first
        if in_string:
            json_str += '"'

        # Close open structures in reverse order
        closers = {'{': '}', '[': ']'}
        for opener in reversed(stack):
            json_str += closers[opener]

        return json_str
    except Exception:
        return ""
