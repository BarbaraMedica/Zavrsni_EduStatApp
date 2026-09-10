import os
from datetime import datetime

import joblib
import numpy as np

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.mongo import predictions


predict_bp = Blueprint("predict", __name__)


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "model",
    "model.pkl"
)

model = joblib.load(MODEL_PATH)


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():

    data = request.get_json() or {}

    # ID trenutno prijavljenog korisnika
    user_id = get_jwt_identity()

    required_fields = [
        "sleep_hours",
        "study_duration",
        "breaks",
        "time_of_day",
        "focus",
        "stress",
        "energy"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": f"Nedostaju polja: {', '.join(missing_fields)}"
        }), 400

    try:
        sleep_hours = float(data["sleep_hours"])
        study_duration = float(data["study_duration"])
        breaks = int(data["breaks"])
        time_of_day = int(data["time_of_day"])
        focus = float(data["focus"])
        stress = float(data["stress"])
        energy = float(data["energy"])

    except (ValueError, TypeError):
        return jsonify({
            "error": "Vrijednosti ulaznih podataka nisu ispravne."
        }), 400

    features = np.array([[
        sleep_hours,
        study_duration,
        breaks,
        time_of_day,
        focus,
        stress,
        energy
    ]])

    prediction = int(model.predict(features)[0])

    probability = round(
        float(model.predict_proba(features)[0][1]),
        2
    )

    result = (
        "Dobro vrijeme za učenje"
        if prediction == 1
        else "Nije dobro vrijeme za učenje"
    )

    predictions.insert_one({

        "user_id": user_id,

        "subject": data.get("subject", ""),

        "date": data.get("date", ""),

        "notes": data.get("notes", ""),

        "input": {
            "sleep_hours": sleep_hours,
            "study_duration": study_duration,
            "breaks": breaks,
            "time_of_day": time_of_day,
            "focus": focus,
            "stress": stress,
            "energy": energy
        },

        "prediction": prediction,

        "result": result,

        "probability": probability,

        "created_at": datetime.utcnow()
    })

    return jsonify({

        "rezultat": result,

        "vjerojatnost": probability

    })