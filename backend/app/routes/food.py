from flask import Blueprint, request, jsonify

food_bp = Blueprint("food", __name__)

# ── Tamil Nadu Free Food Places ─────────────────────────────────────────────
TEMPLE_FOOD = [

    # ── Hindu Temples (HR&CE verified Annadhanam) ──
    {
        "name": "Palani Dhandayudhapani Temple – Devasthanam Annadhanam Hall",
        "district": "Dindigul",
        "location": "Palani, Dindigul, Tamil Nadu",
        "religion": "Hindu",
        "timings": "6 AM – 8 PM",
        "food_timings": [
            {"meal": "Breakfast", "time": "7:00 AM – 9:00 AM", "items": "Pongal, Idli, Sambar"},
            {"meal": "Lunch", "time": "12:00 PM – 2:00 PM", "items": "Rice, Sambar, Rasam, Kootu, Payasam"},
            {"meal": "Dinner", "time": "7:00 PM – 8:00 PM", "items": "Rice, Sambar, Pickle"}
        ],
        "free": True, "verified": True,
        "notes": "HR&CE verified Annadhanam daily"
    },
    {
        "name": "Thiruvannamalai Arunachaleswarar Temple",
        "district": "Tiruvannamalai",
        "location": "Tiruvannamalai, Tamil Nadu",
        "religion": "Hindu",
        "timings": "6 AM – 8 PM",
        "food_timings": [
            {"meal": "Breakfast", "time": "7:30 AM – 9:30 AM", "items": "Idli, Vada, Chutney, Sambar"},
            {"meal": "Lunch", "time": "11:30 AM – 1:30 PM", "items": "Full Meals – Rice, Sambar, Rasam, Curd, Papad"},
            {"meal": "Dinner", "time": "7:00 PM – 8:00 PM", "items": "Chapati, Dal, Rice"}
        ],
        "free": True, "verified": True,
        "notes": "HR&CE verified Annadhanam daily"
    },
    {
        "name": "Sri Puram Golden Temple – Annakshetra Annadhanam",
        "district": "Vellore",
        "location": "Sri Puram, Vellore, Tamil Nadu",
        "religion": "Hindu",
        "timings": "All day",
        "food_timings": [
            {"meal": "Breakfast", "time": "8:00 AM – 10:00 AM", "items": "Idli, Pongal, Sambar"},
            {"meal": "Lunch", "time": "12:00 PM – 3:00 PM", "items": "Full South Indian Meals"},
            {"meal": "Dinner", "time": "6:30 PM – 8:30 PM", "items": "Rice, Sambar, Rasam"}
        ],
        "free": True, "verified": True,
        "notes": "Free meals served all day at Annakshetra"
    },
    {
        "name": "Lakshmi Narayani Golden Temple",
        "district": "Vellore",
        "location": "Sri Puram, Vellore, Tamil Nadu",
        "religion": "Hindu",
        "timings": "All day",
        "food_timings": [
            {"meal": "Breakfast", "time": "8:00 AM – 10:00 AM", "items": "Pongal, Idli, Chutney"},
            {"meal": "Lunch", "time": "12:00 PM – 2:00 PM", "items": "Full Meals with Payasam"},
            {"meal": "Dinner", "time": "7:00 PM – 8:30 PM", "items": "Rice, Dal, Pickle"}
        ],
        "free": True, "verified": True,
        "notes": "Community meals available daily"
    },
    {
        "name": "Tiruchendur Subramaniyaswamy Temple",
        "district": "Thoothukudi",
        "location": "Tiruchendur, Thoothukudi, Tamil Nadu",
        "religion": "Hindu",
        "timings": "6 AM – 8 PM",
        "food_timings": [
            {"meal": "Breakfast", "time": "7:00 AM – 9:00 AM", "items": "Idli, Sambar, Chutney"},
            {"meal": "Lunch", "time": "12:00 PM – 1:30 PM", "items": "Rice, Sambar, Rasam, Kootu"},
            {"meal": "Dinner", "time": "7:00 PM – 8:00 PM", "items": "Rice, Sambar"}
        ],
        "free": True, "verified": True,
        "notes": "HR&CE verified Annadhanam"
    },
    {
        "name": "Srirangam Ranganathaswamy Temple",
        "district": "Tiruchirappalli",
        "location": "Srirangam, Tiruchirappalli, Tamil Nadu",
        "religion": "Hindu",
        "timings": "6 AM – 8 PM",
        "food_timings": [
            {"meal": "Breakfast", "time": "7:00 AM – 9:00 AM", "items": "Pongal, Vada, Sambar"},
            {"meal": "Lunch", "time": "11:00 AM – 1:00 PM", "items": "Grand Annadhanam – Full Meals, Payasam"},
            {"meal": "Dinner", "time": "6:30 PM – 8:00 PM", "items": "Rice, Sambar, Rasam"}
        ],
        "free": True, "verified": True,
        "notes": "One of the largest temple Annadhanams in TN"
    },
    {
        "name": "Rameswaram Ramanathaswamy Temple",
        "district": "Ramanathapuram",
        "location": "Rameswaram, Ramanathapuram, Tamil Nadu",
        "religion": "Hindu",
        "timings": "6 AM – 8 PM",
        "food_timings": [
            {"meal": "Breakfast", "time": "7:30 AM – 9:30 AM", "items": "Idli, Pongal, Sambar"},
            {"meal": "Lunch", "time": "12:00 PM – 2:00 PM", "items": "Full Meals – Rice, Sambar, Rasam, Curd"},
            {"meal": "Dinner", "time": "7:00 PM – 8:00 PM", "items": "Rice, Dal, Pickle"}
        ],
        "free": True, "verified": True,
        "notes": "HR&CE verified Annadhanam daily"
    },
    {
        "name": "Samayapuram Mariamman Temple",
        "district": "Tiruchirappalli",
        "location": "Samayapuram, Tiruchirappalli, Tamil Nadu",
        "religion": "Hindu",
        "timings": "6 AM – 8 PM",
        "food_timings": [
            {"meal": "Breakfast", "time": "7:00 AM – 9:00 AM", "items": "Pongal, Idli, Chutney"},
            {"meal": "Lunch", "time": "12:00 PM – 1:30 PM", "items": "Rice, Sambar, Kootu, Rasam"},
            {"meal": "Dinner", "time": "7:00 PM – 8:00 PM", "items": "Rice, Sambar"}
        ],
        "free": True, "verified": True,
        "notes": "HR&CE verified Annadhanam"
    },
    {
        "name": "Tiruttani Subramaniya Swamy Temple",
        "district": "Tiruvallur",
        "location": "Tiruttani, Tiruvallur, Tamil Nadu",
        "religion": "Hindu",
        "timings": "6 AM – 8 PM",
        "food_timings": [
            {"meal": "Breakfast", "time": "7:00 AM – 9:00 AM", "items": "Idli, Vada, Sambar"},
            {"meal": "Lunch", "time": "12:00 PM – 2:00 PM", "items": "Full Meals – Rice, Sambar, Rasam, Payasam"},
            {"meal": "Dinner", "time": "7:00 PM – 8:00 PM", "items": "Rice, Sambar, Pickle"}
        ],
        "free": True, "verified": True,
        "notes": "HR&CE verified Annadhanam daily"
    },

    # ── Muslim Places (confirm locally for meal timings) ──
    {
        "name": "Walajah Big Mosque",
        "district": "Chennai",
        "location": "Triplicane, Chennai, Tamil Nadu",
        "religion": "Muslim",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community meals available; confirm timings locally"
    },
    {
        "name": "Masjid E Ilaahi",
        "district": "Chennai",
        "location": "Chennai, Tamil Nadu",
        "religion": "Muslim",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community religious centre; confirm meal service locally"
    },
    {
        "name": "The New College Mosque",
        "district": "Chennai",
        "location": "Chennai, Tamil Nadu",
        "religion": "Muslim",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community religious centre; confirm meal service locally"
    },
    {
        "name": "Azad Nagar Masjid",
        "district": "Chennai",
        "location": "Chennai, Tamil Nadu",
        "religion": "Muslim",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community religious centre; confirm meal service locally"
    },
    {
        "name": "Atthankarai Dargha Shareef",
        "district": "Tirunelveli",
        "location": "Tirunelveli, Tamil Nadu",
        "religion": "Muslim",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Dargah community meals; confirm timings locally"
    },
    {
        "name": "Athankarai Pallivasal",
        "district": "Tirunelveli",
        "location": "Tirunelveli, Tamil Nadu",
        "religion": "Muslim",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community religious centre; confirm meal service locally"
    },

    # ── Christian Places (confirm locally for meal timings) ──
    {
        "name": "Vailankanni Church Canteen",
        "district": "Nagapattinam",
        "location": "Vailankanni, Nagapattinam, Tamil Nadu",
        "religion": "Christian",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Pilgrimage canteen; meals available for pilgrims"
    },
    {
        "name": "Poondi Madha Basilica",
        "district": "Thanjavur",
        "location": "Poondi, Thanjavur, Tamil Nadu",
        "religion": "Christian",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Pilgrimage centre; community meals available"
    },
    {
        "name": "Our Lady of Good Health Church, Vadipatti",
        "district": "Madurai",
        "location": "Vadipatti, Madurai, Tamil Nadu",
        "religion": "Christian",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community church; confirm meal service locally"
    },
    {
        "name": "New Life Assembly Of God Church",
        "district": "Chennai",
        "location": "Chennai, Tamil Nadu",
        "religion": "Christian",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community church; confirm meal service locally"
    },
    {
        "name": "CSI All Souls Church",
        "district": "Coimbatore",
        "location": "Coimbatore, Tamil Nadu",
        "religion": "Christian",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community church; confirm meal service locally"
    },
    {
        "name": "C.S.I Christ Church",
        "district": "Coimbatore",
        "location": "Coimbatore, Tamil Nadu",
        "religion": "Christian",
        "timings": "Confirm locally",
        "free": True,
        "verified": False,
        "notes": "Community church; confirm meal service locally"
    },
]

FAMOUS_DISHES = {
    "Tamil Nadu": ["Idli Sambar", "Chettinad Chicken", "Pongal", "Dosa", "Filter Coffee", "Biryani", "Parotta Salna"],
    "Kerala":     ["Appam with Stew", "Kerala Fish Curry", "Puttu & Kadala", "Sadya"],
    "Punjab":     ["Butter Chicken", "Dal Makhani", "Sarson da Saag", "Lassi"],
    "Rajasthan":  ["Dal Baati Churma", "Laal Maas", "Ghevar"],
    "West Bengal":["Rosogolla", "Macher Jhol", "Mishti Doi"],
    "Maharashtra":["Vada Pav", "Puran Poli", "Misal Pav"],
}


INSTANT_FOODS = {
    "Chennai": ["Idli", "Dosa", "Pongal", "Vada", "Filter Coffee", "Bajji", "Sundal"],
    "Madurai": ["Parotta", "Biryani", "Jigarthanda", "Kari Dosa", "Samosa"],
    "Coimbatore": ["Kothu Parotta", "Salna", "Upma", "Rava Dosa", "Tea"],
    "Tiruvannamalai": ["Pongal", "Idli Sambar", "Vada", "Payasam", "Buttermilk"],
    "Rameswaram": ["Fish Fry", "Prawn Masala", "Idli", "Coconut Water", "Sundal"],
    "Ooty": ["Varkey", "Homemade Chocolate", "Carrot Halwa", "Tea", "Bread Omelette"],
    "Alleppey": ["Appam", "Fish Curry", "Puttu", "Coconut Water", "Kerala Meals"],
    "Jaisalmer": ["Dal Baati", "Churma", "Lassi", "Rajasthani Thali", "Chai"],
}


@food_bp.route("/instant-foods", methods=["GET"])
def instant_foods():
    """Get instant foods available by city."""
    city = request.args.get("city", "").strip()
    if city:
        key = next((k for k in INSTANT_FOODS if k.lower() == city.lower()), None)
        if not key:
            return jsonify({"error": "City not found", "available_cities": list(INSTANT_FOODS.keys())}), 404
        return jsonify({"city": key, "instant_foods": INSTANT_FOODS[key]})
    return jsonify(INSTANT_FOODS)


@food_bp.route("/temple-food", methods=["GET"])
def temple_food():
    """
    List free food places.
    Filters: ?district=  ?religion=Hindu|Muslim|Christian  ?verified=true|false  ?state=
    """
    district = request.args.get("district", "").strip().lower()
    religion = request.args.get("religion", "").strip().lower()
    verified = request.args.get("verified", "").strip().lower()
    state    = request.args.get("state", "").strip().lower()

    result = TEMPLE_FOOD

    if district:
        result = [t for t in result if district in t["district"].lower()]
    if religion:
        result = [t for t in result if t["religion"].lower() == religion]
    if verified == "true":
        result = [t for t in result if t["verified"] is True]
    elif verified == "false":
        result = [t for t in result if t["verified"] is False]
    if state:
        result = [t for t in result if state in t["location"].lower()]

    return jsonify(result)


@food_bp.route("/temple-food/summary", methods=["GET"])
def temple_food_summary():
    """Return count of free food places grouped by religion and verification status."""
    summary = {}
    for t in TEMPLE_FOOD:
        rel = t["religion"]
        if rel not in summary:
            summary[rel] = {"total": 0, "verified": 0, "unverified": 0}
        summary[rel]["total"] += 1
        if t["verified"]:
            summary[rel]["verified"] += 1
        else:
            summary[rel]["unverified"] += 1
    return jsonify({
        "total": len(TEMPLE_FOOD),
        "by_religion": summary
    })


@food_bp.route("/famous-dishes", methods=["GET"])
def famous_dishes():
    """Get famous dishes. Optional ?state= filter."""
    state = request.args.get("state")
    if state:
        dishes = FAMOUS_DISHES.get(state)
        if not dishes:
            return jsonify({"error": "State not found", "available": list(FAMOUS_DISHES.keys())}), 404
        return jsonify({"state": state, "dishes": dishes})
    return jsonify(FAMOUS_DISHES)
