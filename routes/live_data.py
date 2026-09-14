from flask import Blueprint, request, jsonify
import requests, os
from urllib.parse import quote

live_data_bp = Blueprint("live_data", __name__)

GOOGLE_MAPS_BASE = "https://maps.googleapis.com/maps/api"


def _safe_coord(val):
    """Validate lat/lng is a float."""
    try:
        return str(float(val))
    except (TypeError, ValueError):
        return None


@live_data_bp.route("/nearby", methods=["GET"])
def nearby_places():
    lat = _safe_coord(request.args.get("lat"))
    lng = _safe_coord(request.args.get("lng"))
    radius = _safe_coord(request.args.get("radius", 5000)) or "5000"

    if not lat or not lng:
        return jsonify({"error": "lat and lng must be valid numbers"}), 400

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    url = f"{GOOGLE_MAPS_BASE}/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=tourist_attraction&key={api_key}"
    resp = requests.get(url, timeout=10)
    return jsonify(resp.json())


@live_data_bp.route("/route", methods=["GET"])
def get_route():
    origin = request.args.get("origin", "").strip()
    destination = request.args.get("destination", "").strip()

    if not origin or not destination:
        return jsonify({"error": "origin and destination are required"}), 400

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    url = f"{GOOGLE_MAPS_BASE}/directions/json?origin={quote(origin)}&destination={quote(destination)}&key={api_key}"
    resp = requests.get(url, timeout=10)
    return jsonify(resp.json())
