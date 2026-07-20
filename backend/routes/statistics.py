from flask import Blueprint, jsonify

from database.mongo import predictions

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.route("/statistics", methods=["GET"])
def statistics():

    docs = list(predictions.find())

    if len(docs)==0:

        return jsonify({

            "total":0,

            "avg_focus":0,

            "avg_stress":0,

            "avg_energy":0,

            "history":[]

        })

    avg_focus = sum(
        d["input"]["focus"] for d in docs
    ) / len(docs)

    avg_stress = sum(
        d["input"]["stress"] for d in docs
    ) / len(docs)

    avg_energy = sum(
        d["input"]["energy"] for d in docs
    ) / len(docs)

    history=[]

    for d in docs:

        history.append({

            "subject": d.get("subject", ""),

            "date": d.get("date", ""),

            "notes": d.get("notes", ""),

            "sleep_hours": d["input"]["sleep_hours"],

            "study_duration": d["input"]["study_duration"],

            "breaks": d["input"]["breaks"],

            "time_of_day": d["input"]["time_of_day"],

            "focus": d["input"]["focus"],

            "stress": d["input"]["stress"],

            "energy": d["input"]["energy"],

            "result": d["result"],

            "probability": d["probability"]

        })

    return jsonify({

        "total":len(docs),

        "avg_focus":round(avg_focus,2),

        "avg_stress":round(avg_stress,2),

        "avg_energy":round(avg_energy,2),

        "history":history

    })