from flask import Blueprint, jsonify, request

from database.mongo import analyses, predictions

from datetime import datetime


analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()


    # ovdje ćeš kasnije pozvati Random Forest
    prediction = "Dobro"


    probability = 0.85



    # Grok AI odgovor
    ai_response = grok_analysis(
        data,
        prediction
    )



    # spremanje u analyses kolekciju

    analyses.insert_one({

        "subject": data.get("subject",""),

        "text": ai_response,

        "date": data.get("date",""),

        "type": "AI analiza",

        "prediction": prediction,

        "probability": probability,

        "input": data,

        "created_at": datetime.utcnow()

    })



    return jsonify({

        "prediction": prediction,

        "probability": round(probability*100,2),

        "ai_analysis": ai_response

    })





def grok_analysis(data, prediction):

    prompt=f"""

    Analiziraj navike učenja studenta.


    Predmet:
    {data.get('subject')}


    San:
    {data.get('sleep_hours')} sati


    Učenje:
    {data.get('study_duration')} minuta


    Fokus:
    {data.get('focus')}/10


    Stres:
    {data.get('stress')}/10


    Energija:
    {data.get('energy')}/10


    Model predviđa:
    {prediction}


    Daj:
    - kratku analizu
    - probleme
    - preporuke


    """

    # ovdje kasnije ide pravi Grok API poziv

    return "AI analiza će biti generirana pomoću Groka."