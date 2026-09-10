from bson.objectid import ObjectId

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.mongo import analyses, predictions

from datetime import datetime


data_bp = Blueprint("data", __name__)


# PREDMETI

@data_bp.route("/subjects", methods=["GET"])
@jwt_required()
def subjects():

    user_id = get_jwt_identity()

    pipeline = [

        {
            "$match": {
                "user_id": user_id,
                "subject": {
                    "$ne": ""
                }
            }
        },

        {
            "$group": {

                "_id": "$subject",

                "sessions": {
                    "$sum": 1
                },

                "avg_focus": {
                    "$avg": "$input.focus"
                },

                "avg_stress": {
                    "$avg": "$input.stress"
                },

                "avg_duration": {
                    "$avg": "$input.study_duration"
                },

                "productivity": {
                    "$avg": "$probability"
                },

                "last_created_at": {
                    "$max": "$created_at"
                }
            }
        },

        {
            "$project": {

                "name": "$_id",

                "sessions": 1,

                "avg_focus": {
                    "$round": [
                        "$avg_focus",
                        1
                    ]
                },

                "avg_stress": {
                    "$round": [
                        "$avg_stress",
                        1
                    ]
                },

                "avg_duration": {
                    "$round": [
                        "$avg_duration",
                        0
                    ]
                },

                "productivity": {
                    "$round": [
                        {
                            "$multiply": [
                                "$productivity",
                                100
                            ]
                        },
                        0
                    ]
                },

                "last_session": {
                    "$dateToString": {
                        "format": "%d.%m.%Y",
                        "date": "$last_created_at"
                    }
                }
            }
        }
    ]

    subject_docs = list(
        predictions.aggregate(pipeline)
    )

    return jsonify(subject_docs)


# DOHVAĆANJE AI ANALIZA

@data_bp.route("/analyses", methods=["GET"])
@jwt_required()
def get_analyses():

    user_id = get_jwt_identity()

    docs = list(
        analyses.find({
            "user_id": user_id
        }).sort(
            "created_at",
            -1
        )
    )

    result = []

    for doc in docs:

        result.append({

            "_id": str(doc.get("_id")),

            "subject": doc.get(
                "subject",
                ""
            ),

            "text": doc.get(
                "text",
                ""
            ),

            "date": doc.get(
                "date",
                ""
            ),

            "type": doc.get(
                "type",
                ""
            ),

            "created_at": str(
                doc.get("created_at")
            )

        })

    return jsonify(result)

# SPREMANJE AI ANALIZE

@data_bp.route("/analyses", methods=["POST"])
@jwt_required()
def add_analysis():

    user_id = get_jwt_identity()

    data = request.get_json() or {}

    subject = data.get(
        "subject",
        ""
    )

    text = data.get(
        "text",
        ""
    )

    date = data.get(
        "date",
        ""
    )

    note_type = data.get(
        "type",
        "AI analiza"
    )

    if not subject or not text:

        return jsonify({
            "error": "Predmet i tekst su obavezni."
        }), 400

    inserted = analyses.insert_one({

        "user_id": user_id,

        "subject": subject,

        "text": text,

        "date": date,

        "type": note_type,

        "created_at": datetime.utcnow()

    })

    return jsonify({

        "_id": str(
            inserted.inserted_id
        ),

        "subject": subject,

        "text": text,

        "date": date,

        "type": note_type

    }), 201

# BRISANJE AI ANALIZE

@data_bp.route(
    "/analyses/<analysis_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_analysis(analysis_id):

    user_id = get_jwt_identity()

    try:

        object_id = ObjectId(
            analysis_id
        )

    except Exception:

        return jsonify({
            "error": "Nevažeći ID analize."
        }), 400

    deleted = analyses.delete_one({

        "_id": object_id,

        "user_id": user_id

    })

    if deleted.deleted_count == 0:

        return jsonify({
            "error": "Analiza nije pronađena."
        }), 404

    return jsonify({
        "success": True
    })