from app import create_app

app = create_app()

if __name__ == "__main__":
    # For local development; production uses gunicorn
    app.run(host="0.0.0.0", port=8000)
