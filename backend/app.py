import os
from flask import Flask, request, jsonify
from flask.cli import load_dotenv
from flask_cors import CORS
import joblib
import numpy as np


load_dotenv()
app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
model = joblib.load(MODEL_PATH)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Provjera jesu li sva polja poslana
    required_fields = [
        "sleep_hours",
        "study_duration",
        "breaks",
        "time_of_day",
        "focus",
        "stress",
        "energy"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Nedostaje polje: {field}"
            }), 400

    try:
        sleep_hours = float(data["sleep_hours"])
        study_duration = float(data["study_duration"])
        breaks = int(data["breaks"])
        time_of_day = int(data["time_of_day"])
        focus = float(data["focus"])
        stress = float(data["stress"])
        energy = float(data["energy"])

        features = np.array([[
            sleep_hours,
            study_duration,
            breaks,
            time_of_day,
            focus,
            stress,
            energy
        ]])

        prediction = model.predict(features)[0]

        if hasattr(model, "predict_proba"):
            probability = round(float(model.predict_proba(features)[0][1]), 2)
        else:
            probability = None

        if prediction == 1:
            result = "Dobro vrijeme za učenje"
        else:
            result = "Nije dobro vrijeme za učenje"

        return jsonify({
            "rezultat": result,
            "vjerojatnost": probability
        })

    except (KeyError, ValueError) as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)