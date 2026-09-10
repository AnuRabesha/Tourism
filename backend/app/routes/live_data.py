from flask import Blueprint, request, jsonify
import requests, os

live_data_bp = Blueprint("live_data", __name__)

@live_data_bp.route("/nearby", methods=["GET"])
def nearby_places():
    """Get nearby tourist places based on lat/lng."""
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    radius = request.args.get("radius", 5000)

    if not lat or not lng:
        return jsonify({"error": "lat and lng are required"}), 400

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}&radius={radius}&type=tourist_attraction&key={api_key}"
    )
    resp = requests.get(url)
    return jsonify(resp.json())


@live_data_bp.route("/route", methods=["GET"])
def get_route():
    """Get route between origin and destination."""
    origin = request.args.get("origin")
    destination = request.args.get("destination")

    if not origin or not destination:
        return jsonify({"error": "origin and destination are required"}), 400

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin}&destination={destination}&key={api_key}"
    )
    resp = requests.get(url)
    return jsonify(resp.json())
