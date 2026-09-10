"""
Chat routes – /api/chat
"""

import logging
from flask import Blueprint, request, jsonify
from services.chat_service import handle_chat

logger = logging.getLogger(__name__)
chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat_endpoint():
    """Handle a career counseling chat message."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    profile = data.get("profile", {})
    history = data.get("history", [])
    current_goal = data.get("current_goal", "")

    # Sanitize history
    if not isinstance(history, list):
        history = []
    history = history[-10:]  # keep last 10 messages only

    try:
        result = handle_chat(message, profile, history, current_goal)
        return jsonify(result), 200
    except Exception as exc:
        logger.error(f"Chat error: {exc}")
        return jsonify({"error": "Chat service unavailable. Please try again."}), 500
