"""
Comparison routes – /api/compare-careers
"""

import logging
from flask import Blueprint, request, jsonify
from services.comparison_service import compare_careers

logger = logging.getLogger(__name__)
comparison_bp = Blueprint("comparison", __name__)


@comparison_bp.route("/compare-careers", methods=["POST"])
def compare_careers_endpoint():
    """Compare multiple career paths for a student."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    careers = data.get("careers", [])
    if not careers or not isinstance(careers, list) or len(careers) < 2:
        return jsonify({"error": "Provide at least 2 careers to compare"}), 400

    if len(careers) > 3:
        careers = careers[:3]

    profile = data.get("profile", {})

    try:
        result = compare_careers(careers, profile)
        return jsonify(result), 200
    except Exception as exc:
        logger.error(f"Comparison error: {exc}")
        return jsonify({"error": "Career comparison failed. Please try again."}), 500
