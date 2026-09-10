from flask import Blueprint, request, jsonify

safety_bp = Blueprint("safety", __name__)

# Static emergency contacts — replace with DB or region-based lookup as needed
EMERGENCY_CONTACTS = {
    "police": {"number": "100", "description": "Police emergency"},
    "firefighter": {"number": "101", "description": "Fire & rescue"},
    "doctor": {"number": "108", "description": "Medical ambulance"},
    "women_alert": {"number": "1091", "description": "Women helpline"},
}

# Simulated crowd data — replace with real IoT/sensor data source
CROWD_DATA = {
    "marina_beach": {"level": "high", "advice": "Avoid peak hours 5–8 PM"},
    "gateway_of_india": {"level": "medium", "advice": "Manageable crowd"},
    "taj_mahal": {"level": "low", "advice": "Good time to visit"},
}


@safety_bp.route("/emergency-contacts", methods=["GET"])
def emergency_contacts():
    """Return all emergency contact numbers."""
    return jsonify(EMERGENCY_CONTACTS)


@safety_bp.route("/emergency-contacts/<service>", methods=["GET"])
def emergency_contact(service):
    """Return contact for a specific service: police, firefighter, doctor, women_alert."""
    contact = EMERGENCY_CONTACTS.get(service.lower())
    if not contact:
        return jsonify({"error": f"Service '{service}' not found"}), 404
    return jsonify(contact)


@safety_bp.route("/crowd-alert", methods=["GET"])
def crowd_alert():
    """Get crowd level for a specific place."""
    place = request.args.get("place", "").lower().replace(" ", "_")
    if not place:
        return jsonify(CROWD_DATA)
    data = CROWD_DATA.get(place)
    if not data:
        return jsonify({"error": "Place not found", "available": list(CROWD_DATA.keys())}), 404
    return jsonify({"place": place, **data})
