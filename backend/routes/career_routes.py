"""
Career routes – /api/analyze-career
"""

import logging
from flask import Blueprint, request, jsonify
from services.career_service import analyze_career

logger = logging.getLogger(__name__)
career_bp = Blueprint("career", __name__)

REQUIRED_FIELDS = ["name", "degree", "branch", "year", "cgpa", "technical_skills"]


@career_bp.route("/analyze-career", methods=["POST"])
def analyze_career_endpoint():
    """Analyze a student profile and return career recommendations."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Validate required fields
    missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        result = analyze_career(data)
        return jsonify(result), 200
    except Exception as exc:
        logger.error(f"Career analysis error: {exc}")
        return jsonify({"error": "Career analysis failed. Please try again."}), 500
