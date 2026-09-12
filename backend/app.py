import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()  # Učitavanje varijabli iz .env datoteke

from routes.predict import predict_bp
from routes.statistics import statistics_bp
from routes.data import data_bp
from routes.analysis import analysis_bp
from routes.auth import auth_bp


app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

CORS(
    app,
    resources={
        r"/*": {
            "origins": "https://zavrsni-edustatapp.onrender.com"
        }
    },
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

JWTManager(app)

app.register_blueprint(predict_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(data_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)