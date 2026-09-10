from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    print("Starting TourEase server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=False, port=5000)
