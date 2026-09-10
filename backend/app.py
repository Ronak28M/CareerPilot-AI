"""
CareerPilot AI – Flask Backend
Coordinates between the React frontend and IBM Granite / watsonx Orchestrate.
"""

import os
import json
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# Register blueprints
from routes.career_routes import career_bp
from routes.chat_routes import chat_bp
from routes.comparison_routes import comparison_bp
from routes.progress_routes import progress_bp

app.register_blueprint(career_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")
app.register_blueprint(comparison_bp, url_prefix="/api")
app.register_blueprint(progress_bp, url_prefix="/api")


@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "CareerPilot AI Backend"}, 200


@app.errorhandler(404)
def not_found(e):
    return {"error": "Endpoint not found"}, 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return {"error": "Internal server error. Please try again."}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    logger.info(f"Starting CareerPilot AI backend on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
