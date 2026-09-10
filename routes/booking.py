from flask import Blueprint, request, jsonify
from datetime import datetime

booking_bp = Blueprint("booking", __name__)

# In-memory store — replace with a real DB (SQLite/PostgreSQL) for production
bookings = []
booking_id_counter = 1


def _next_id():
    global booking_id_counter
    bid = booking_id_counter
    booking_id_counter += 1
    return bid


@booking_bp.route("/hotels", methods=["GET"])
def list_hotels():
    """List available hotels. Optional ?city= filter."""
    city = request.args.get("city", "").lower()
    hotels = [
        {"id": 1, "name": "Grand Palace Hotel", "city": "Chennai", "price_per_night": 2500, "rating": 4.5},
        {"id": 2, "name": "Heritage Inn", "city": "Madurai", "price_per_night": 1800, "rating": 4.2},
        {"id": 3, "name": "Backwater Resort", "city": "Alleppey", "price_per_night": 3200, "rating": 4.7},
        {"id": 4, "name": "Desert Camp", "city": "Jaisalmer", "price_per_night": 2000, "rating": 4.3},
    ]
    if city:
        hotels = [h for h in hotels if city in h["city"].lower()]
    return jsonify(hotels)


@booking_bp.route("/transport", methods=["GET"])
def transport_options():
    """Get transport options between two cities."""
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    if not origin or not destination:
        return jsonify({"error": "origin and destination are required"}), 400

    # Static sample — integrate with real transport API as needed
    options = [
        {"type": "Bus", "operator": "TNSTC", "duration": "6h", "price": 350},
        {"type": "Train", "operator": "Indian Railways", "duration": "4h", "price": 500},
        {"type": "Flight", "operator": "IndiGo", "duration": "1h", "price": 3500},
    ]
    return jsonify({"origin": origin, "destination": destination, "options": options})


@booking_bp.route("/pre-book", methods=["POST"])
def pre_book():
    """Pre-book a hotel or transport. Body: {type, name, user_name, date, guests}"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    required = ["type", "name", "user_name", "date"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Validate guests is a positive integer
    try:
        guests = int(data.get("guests", 1))
        if guests < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "guests must be a positive integer"}), 400

    booking = {
        "booking_id": _next_id(),
        "type": data["type"],
        "name": data["name"],
        "user_name": data["user_name"],
        "date": data["date"],
        "guests": guests,
        "booked_at": datetime.utcnow().isoformat(),
        "status": "confirmed",
    }
    bookings.append(booking)
    return jsonify({"message": "Booking confirmed", "booking": booking}), 201


@booking_bp.route("/bookings/<user_name>", methods=["GET"])
def get_bookings(user_name):
    """Get all bookings for a user."""
    user_bookings = [b for b in bookings if b["user_name"] == user_name]
    return jsonify(user_bookings)
