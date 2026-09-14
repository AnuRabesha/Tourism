from flask import Flask, jsonify, send_from_directory, abort
from flask_cors import CORS
from dotenv import load_dotenv
import traceback
import os

from .routes.live_data import live_data_bp
from .routes.weather import weather_bp
from .routes.safety import safety_bp
from .routes.language import language_bp
from .routes.food import food_bp
from .routes.booking import booking_bp
from .routes.auth import auth_bp

load_dotenv()

# Resolve frontend folder (two levels up from this file: backend/app/ -> project root -> frontend)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")


def create_app():
    app = Flask(__name__, static_folder=None)
    CORS(app)

    # ── API Blueprints ──────────────────────────────────────────
    app.register_blueprint(live_data_bp, url_prefix="/api/live-data")
    app.register_blueprint(weather_bp,   url_prefix="/api/weather")
    app.register_blueprint(safety_bp,    url_prefix="/api/safety")
    app.register_blueprint(language_bp,  url_prefix="/api/language")
    app.register_blueprint(food_bp,      url_prefix="/api/food")
    app.register_blueprint(booking_bp,   url_prefix="/api/booking")
    app.register_blueprint(auth_bp,      url_prefix="/api/auth")

    # ── Health check ────────────────────────────────────────────
    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "app": "Tourism Support API"})

    # ── Serve login page ─────────────────────────────────────────
    @app.route("/login")
    def serve_login():
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), "login.html")

    # ── Serve frontend static assets (css, js, images) ─────────
    @app.route("/static/frontend/<path:filename>")
    def frontend_static(filename):
        return send_from_directory(FRONTEND_DIR, filename)

    # ── Serve frontend pages ─────────────────────────────────────
    @app.route("/pages/<page>")
    def serve_page(page):
        return send_from_directory(os.path.join(FRONTEND_DIR, "pages"), page)

    # ── Serve home (index.html) ──────────────────────────────────
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path:
            # Prevent path traversal — resolve and verify within FRONTEND_DIR
            frontend_abs = os.path.realpath(FRONTEND_DIR)
            target = os.path.realpath(os.path.join(FRONTEND_DIR, path))
            if not target.startswith(frontend_abs + os.sep) and target != frontend_abs:
                abort(404)
            if os.path.isfile(target):
                return send_from_directory(os.path.dirname(target), os.path.basename(target))
        return send_from_directory(FRONTEND_DIR, "index.html")

    # ── Global error handlers ────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

    return app
