from flask import Blueprint, jsonify, request
from .predict import model
from database.mongo import analyses, predictions
import numpy as np
from datetime import datetime

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)
analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()
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

    probability = round(
        float(model.predict_proba(features)[0][1]),
        2
    )

    result = (
        "Dobro vrijeme za učenje"
        if prediction == 1
        else "Nije dobro vrijeme za učenje"
)

    # Grok AI odgovor
    ai_response = grok_analysis(
        data,
        result
    )

    predictions.insert_one({

        "subject": data.get("subject",""),

        "date": data.get("date",""),

        "notes": data.get("notes",""),

        "input":{

            "sleep_hours":sleep_hours,
            "study_duration":study_duration,
            "breaks":breaks,
            "time_of_day":time_of_day,
            "focus":focus,
            "stress":stress,
            "energy":energy

        },

        "prediction": int(prediction),

        "result": result,

        "probability": probability,

        "created_at": datetime.utcnow()

    })



    # spremanje u analyses kolekciju

    analyses.insert_one({

        "subject": data.get("subject",""),

        "text": ai_response,

        "date": data.get("date",""),

        "type": "AI analiza",

        "prediction": result,

        "probability": probability,

        "created_at": datetime.utcnow()

    })



    return jsonify({

        "prediction": result,

        "probability": round(probability*100,2),

        "ai_analysis": ai_response

    })





def grok_analysis(data, prediction):

    prompt = f"""

Ti si AI mentor za studente.

Analiziraj navike učenja.


Predmet:
{data.get("subject")}


Sati sna:
{data.get("sleep_hours")}


Trajanje učenja:
{data.get("study_duration")} minuta


Broj pauza:
{data.get("breaks")}


Fokus:
{data.get("focus")}/10


Stres:
{data.get("stress")}/10


Energija:
{data.get("energy")}/10


Random Forest predikcija:
{prediction}



Napiši odgovor na hrvatskom jeziku:

1. Procjena trenutnog stanja
2. Glavni problemi
3. Konkretne preporuke za poboljšanje


"""


    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content":
                "Ti si stručni AI asistent za analizu studentskih navika."
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.7
    )


    return response.choices[0].message.content
