from flask import Flask
from flask_cors import CORS

from routes.incident import incident_bp
from routes.health import health_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(incident_bp)

app.register_blueprint(health_bp)

@app.route("/")

def home():

    return {
        "project":"AI Disaster Response System",
        "status":"Running"
    }

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
