from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.mongo import predictions


statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.route("/statistics", methods=["GET"])
@jwt_required()
def statistics():

    user_id = get_jwt_identity()

    docs = list(
        predictions.find({
            "user_id": user_id
        }).sort("created_at", -1)
    )

    if len(docs) == 0:

        return jsonify({

            "total": 0,

            "avg_focus": 0,

            "avg_stress": 0,

            "avg_energy": 0,

            "history": []

        })

    avg_focus = sum(
        float(d.get("input", {}).get("focus", 0))
        for d in docs
    ) / len(docs)

    avg_stress = sum(
        float(d.get("input", {}).get("stress", 0))
        for d in docs
    ) / len(docs)

    avg_energy = sum(
        float(d.get("input", {}).get("energy", 0))
        for d in docs
    ) / len(docs)

    history = []

    for d in docs:

        input_data = d.get("input", {})

        history.append({

            "subject": d.get("subject") or "Nepoznato",

            "date": d.get("date", ""),

            "notes": d.get("notes", ""),

            "sleep_hours": input_data.get("sleep_hours", 0),

            "study_duration": input_data.get("study_duration", 0),

            "breaks": input_data.get("breaks", 0),

            "time_of_day": input_data.get("time_of_day", 0),

            "focus": input_data.get("focus", 0),

            "stress": input_data.get("stress", 0),

            "energy": input_data.get("energy", 0),

            "result": d.get("result", ""),

            "probability": d.get("probability", 0),

            "created_at": str(d.get("created_at", ""))

        })

    return jsonify({

        "total": len(docs),

        "avg_focus": round(avg_focus, 2),

        "avg_stress": round(avg_stress, 2),

        "avg_energy": round(avg_energy, 2),

        "history": history

    })