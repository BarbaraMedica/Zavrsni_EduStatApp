from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from database.mongo import analyses, predictions

from datetime import datetime

data_bp = Blueprint("data", __name__)


@data_bp.route("/subjects", methods=["GET"])
def subjects():
    pipeline = [
        {
            "$match": {
                "subject": {"$ne": ""}
            }
        },
        {
            "$group": {
                "_id": "$subject",
                "sessions": {"$sum": 1},
                "avg_focus": {"$avg": "$input.focus"},
                "avg_stress": {"$avg": "$input.stress"},
                "avg_duration": {"$avg": "$input.study_duration"},
                "productivity": {"$avg": "$probability"},
                "last_created_at": {"$max": "$created_at"}
            }
        },
        {
            "$project": {
                "name": "$_id",
                "sessions": 1,
                "avg_focus": {"$round": ["$avg_focus", 1]},
                "avg_stress": {"$round": ["$avg_stress", 1]},
                "avg_duration": {"$round": ["$avg_duration", 0]},
                "productivity": {"$round": [{"$multiply": ["$productivity", 100]}, 0]},
                "last_session": {
                    "$dateToString": {
                        "format": "%d.%m.%Y",
                        "date": "$last_created_at"
                    }
                }
            }
        }
    ]

    subject_docs = list(predictions.aggregate(pipeline))

    return jsonify(subject_docs)


@data_bp.route("/analyses", methods=["GET"])
def get_analyses():
    docs = list(analyses.find().sort("created_at", -1))
    result = []

    for doc in docs:
        result.append({
            "_id": str(doc.get("_id")),
            "subject": doc.get("subject", ""),
            "text": doc.get("text", ""),
            "date": doc.get("date", ""),
            "type": doc.get("type", ""),
            "created_at": str(doc.get("created_at"))
        })

    return jsonify(result)


@data_bp.route("/analyses", methods=["POST"])
def add_analysis():
    data = request.get_json() or {}
    subject = data.get("subject", "")
    text = data.get("text", "")
    date = data.get("date", "")
    note_type = data.get("type", "AI analiza")

    if not subject or not text:
        return jsonify({"error": "Predmet i tekst su obavezni."}), 400

    inserted = analyses.insert_one({
        "subject": subject,
        "text": text,
        "date": date,
        "type": note_type,
        "created_at": datetime.utcnow()
    })

    return jsonify({
        "_id": str(inserted.inserted_id),
        "subject": subject,
        "text": text,
        "date": date,
        "type": note_type
    })


@data_bp.route("/analyses/<analysis_id>", methods=["DELETE"])
def delete_analysis(analysis_id):
    try:
        deleted = analyses.delete_one({"_id": ObjectId(analysis_id)})
    except Exception:
        return jsonify({"error": "Nevažeći ID analize."}), 400

    if deleted.deleted_count == 0:
        return jsonify({"error": "Analiza nije pronađena."}), 404

    return jsonify({"success": True})
