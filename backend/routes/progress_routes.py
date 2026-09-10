"""
Progress routes – /api/update-progress
"""

import logging
from flask import Blueprint, request, jsonify
from services.progress_service import update_progress

logger = logging.getLogger(__name__)
progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/update-progress", methods=["POST"])
def update_progress_endpoint():
    """Update progress and get new recommendations."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    if not data.get("student_name") and not data.get("target_career"):
        return jsonify({"error": "student_name and target_career are required"}), 400

    overall = data.get("overall_progress_percent", 0)
    if not isinstance(overall, int) or not (0 <= overall <= 100):
        data["overall_progress_percent"] = max(0, min(100, int(overall or 0)))

    try:
        result = update_progress(data)
        return jsonify(result), 200
    except Exception as exc:
        logger.error(f"Progress update error: {exc}")
        return jsonify({"error": "Progress update failed. Please try again."}), 500
