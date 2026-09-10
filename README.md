# Turism

A smart one-stop Tourism Support App built with **Python Flask** (backend) and **HTML/CSS/JavaScript** (frontend).

## Features

- 🌦️ **Weather** — Current weather & 5-day forecast
- 🚨 **Safety** — Emergency contacts & crowd alerts
- 🍲 **Food** — Temple free food & famous local dishes
- 🌐 **Language** — Translate text & common tourist phrases
- 📅 **Booking** — Hotels, transport & pre-booking

## Project Structure

```
Turism/
├── run.py                  # Entry point
├── frontend/               # HTML, CSS, JavaScript
│   ├── index.html
│   ├── css/style.css
│   ├── js/api.js
│   └── pages/
│       ├── weather.html
│       ├── safety.html
│       ├── food.html
│       ├── language.html
│       └── booking.html
└── backend/
    ├── .env
    ├── requirements.txt
    └── app/
        ├── __init__.py
        └── routes/
            ├── weather.py
            ├── safety.py
            ├── food.py
            ├── language.py
            ├── booking.py
            └── live_data.py
```

## Setup & Run

1. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Add API keys to `backend/.env`:
```
WEATHER_API_KEY=your_openweathermap_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

3. Run the app:
```bash
python run.py
```

4. Open in browser: [http://localhost:5000](http://localhost:5000)

## Tech Stack

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **APIs**: OpenWeatherMap, MyMemory Translation, Google Maps
# Tourism 
