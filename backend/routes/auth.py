from flask import Blueprint, request, jsonify
from database.mongo import users

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from bson import ObjectId
from bson.errors import InvalidId

from datetime import datetime


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# REGISTRACIJA

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json() or {}

    username = data.get(
        "username",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    if not username or not email or not password:

        return jsonify({
            "error": "Korisničko ime, email i lozinka su obavezni."
        }), 400

    if len(password) < 6:

        return jsonify({
            "error": "Lozinka mora imati najmanje 6 znakova."
        }), 400

    existing_user = users.find_one({
        "email": email
    })

    if existing_user:

        return jsonify({
            "error": "Korisnik s tim emailom već postoji."
        }), 409

    user = {

        "username": username,

        "email": email,

        "password": generate_password_hash(
            password
        ),

        "created_at": datetime.utcnow()

    }

    result = users.insert_one(
        user
    )

    return jsonify({

        "message": "Registracija je uspješna.",

        "user": {

            "id": str(
                result.inserted_id
            ),

            "username": username,

            "email": email

        }

    }), 201


# PRIJAVA

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json() or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    if not email or not password:

        return jsonify({
            "error": "Email i lozinka su obavezni."
        }), 400

    user = users.find_one({
        "email": email
    })

    if not user:

        return jsonify({
            "error": "Neispravan email ili lozinka."
        }), 401

    if not check_password_hash(
        user["password"],
        password
    ):

        return jsonify({
            "error": "Neispravan email ili lozinka."
        }), 401

    access_token = create_access_token(
        identity=str(
            user["_id"]
        )
    )

    return jsonify({

        "message": "Prijava uspješna.",

        "token": access_token,

        "user": {

            "id": str(
                user["_id"]
            ),

            "username": user["username"],

            "email": user["email"]

        }

    })


# TRENUTNI KORISNIK


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def current_user():

    user_id = get_jwt_identity()

    try:

        object_id = ObjectId(
            user_id
        )

    except (InvalidId, TypeError):

        return jsonify({
            "error": "Nevažeći korisnički ID."
        }), 400

    user = users.find_one({
        "_id": object_id
    })

    if not user:

        return jsonify({
            "error": "Korisnik nije pronađen."
        }), 404

    return jsonify({

        "id": str(
            user["_id"]
        ),

        "username": user["username"],

        "email": user["email"]

    })