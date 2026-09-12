from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .predict import model
from database.mongo import analyses, predictions

import numpy as np
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# =========================================================
# GROQ KLIJENT
# ISTI NAČIN DOHVAĆANJA KLJUČA KAO U STAROM KODU
# =========================================================

client = None

if OpenAI is not None and os.getenv("GROQ_API_KEY"):
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )


analysis_bp = Blueprint("analysis", __name__)


# =========================================================
# OPTIONS /analyze
# Preflight za browser CORS zahtjeve
# =========================================================

@analysis_bp.route("/analyze", methods=["OPTIONS"])
def analyze_options():
    return "", 204


# =========================================================
# POST /analyze
# Zapisivanje sesije + Random Forest + AI analiza
# =========================================================

@analysis_bp.route("/analyze", methods=["POST"])
@jwt_required()
def analyze():

    data = request.get_json() or {}
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

    missing = [
        field for field in required_fields
        if field not in data
    ]

    if missing:
        return jsonify({
            "error": f"Nedostaju polja: {', '.join(missing)}"
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


    # =====================================================
    # RANDOM FOREST
    # =====================================================

    features = np.array([[
        sleep_hours,
        study_duration,
        breaks,
        time_of_day,
        focus,
        stress,
        energy
    ]])

    prediction = int(
        model.predict(features)[0]
    )

    probability = round(
        float(model.predict_proba(features)[0][1]),
        2
    )

    result = (
        "Dobro vrijeme za učenje"
        if prediction == 1
        else "Nije dobro vrijeme za učenje"
    )


    # =====================================================
    # AI ANALIZA
    # =====================================================

    ai_response = grok_analysis(
        data,
        result
    )


    # =====================================================
    # SPREMANJE PREDIKCIJE U MONGODB
    # =====================================================

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


    # =====================================================
    # SPREMANJE AI ANALIZE U MONGODB
    # =====================================================

    analyses.insert_one({
        "user_id": user_id,
        "subject": data.get("subject", ""),

        "text": ai_response,

        "date": data.get("date", ""),

        "type": "AI analiza",

        "prediction": result,

        "probability": probability,

        "created_at": datetime.utcnow()
    })


    return jsonify({

        "prediction": result,

        "probability": round(
            probability * 100,
            2
        ),

        "ai_analysis": ai_response
    })


# =========================================================
# OPTIONS /daily-analysis
# Preflight za browser CORS zahtjeve
# =========================================================

@analysis_bp.route("/daily-analysis", methods=["OPTIONS"])
def daily_analysis_options():
    return "", 204


# =========================================================
# GET /daily-analysis
#
# SAŽETA ANALIZA ZA DASHBOARD
# =========================================================

@analysis_bp.route("/daily-analysis", methods=["GET"])
@jwt_required()
def daily_analysis():
    user_id = get_jwt_identity()
    try:

        # Dohvati zadnjih 10 sesija
        recent_sessions = list(
            predictions.find(
                {"user_id": user_id}
            ).sort(
                "created_at",
                -1
            ).limit(10)
        )


        if not recent_sessions:

            return jsonify({
                "analysis": "Još nema dovoljno podataka za AI analizu."
            })


        # Priprema podataka za AI
        session_text = ""

        for i, session in enumerate(
            recent_sessions,
            start=1
        ):

            input_data = session.get(
                "input",
                {}
            )

            session_text += f"""

Sesija {i}:

Predmet:
{session.get("subject", "Nije uneseno")}

Datum:
{session.get("date", "Nije uneseno")}

Sati sna:
{input_data.get("sleep_hours", "Nije uneseno")}

Trajanje učenja:
{input_data.get("study_duration", "Nije uneseno")} minuta

Broj pauza:
{input_data.get("breaks", "Nije uneseno")}

Vrijeme učenja:
{input_data.get("time_of_day", "Nije uneseno")} h

Fokus:
{input_data.get("focus", "Nije uneseno")}/10

Stres:
{input_data.get("stress", "Nije uneseno")}/10

Energija:
{input_data.get("energy", "Nije uneseno")}/10

Predikcija:
{session.get("result", "Nije dostupno")}

Vjerojatnost:
{session.get("probability", 0) * 100}%

"""


        # =================================================
        # PROMPT ZA SAŽETU ANALIZU
        # =================================================

        prompt = f"""
Ti si AI mentor za studente.

Na temelju posljednjih sesija učenja napravi
KRATKU I JASNU analizu za prikaz na Dashboardu.

Analiziraj:

- kvalitetu sna
- trajanje učenja
- broj pauza
- vrijeme učenja
- fokus
- stres
- energiju
- rezultate Random Forest modela
- predmete

Podaci:

{session_text}

Odgovor napiši na hrvatskom jeziku.

Odgovor treba biti sažet i prikladan za Dashboard.

NEMOJ raditi dugačke odjeljke.

Napiši:

1. Kratku procjenu trenutnih navika.
2. Najvažniji uočeni problem.
3. Jednu do dvije konkretne preporuke.

Odgovor neka bude maksimalno 1-2 kratka odlomka.
"""


        # =================================================
        # AKO NEMA xAI KLIJENTA
        # =================================================

        if client is None:

            return jsonify({
                "analysis": (
                    "Na temelju dosadašnjih sesija preporučuje se "
                    "održavati redovite pauze, dovoljno spavati "
                    "i pratiti razinu fokusa i stresa tijekom učenja."
                )
            })


        # =================================================
        # POZIV AI MODELA
        # =================================================

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",
            messages=[

                {
                    "role": "system",
                    "content": (
                        "Ti si stručni AI asistent za analizu "
                        "studentskih navika učenja."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7
        )


        ai_text = response.choices[0].message.content


        return jsonify({
            "analysis": ai_text
        })


    except Exception as e:

        print(
            "Greška kod daily-analysis:",
            str(e)
        )

        return jsonify({
            "error": "Nije moguće generirati dnevnu AI analizu."
        }), 500


# =========================================================
# OPTIONS /full-analysis
# Preflight za browser CORS zahtjeve
# =========================================================

@analysis_bp.route("/full-analysis", methods=["OPTIONS"])
def full_analysis_options():
    return "", 204


# =========================================================
# GET /full-analysis
#
# DETALJNA ANALIZA ZA AI ANALIZA STRANICU
# =========================================================

@analysis_bp.route("/full-analysis", methods=["GET"])
@jwt_required()
def full_analysis():
    user_id = get_jwt_identity()
    try:

        # =================================================
        # DOHVAT ZADNJIH 10 SESIJA
        # =================================================

        recent_sessions = list(
            predictions.find(
                {"user_id": user_id}
            ).sort(
                "created_at",
                -1
            ).limit(10)
        )


        if not recent_sessions:

            return jsonify({

                "analysis": "",

                "sessions": []
            })


        # =================================================
        # PRIPREMA PODATAKA
        # =================================================

        session_text = ""

        formatted_sessions = []


        for session in recent_sessions:

            input_data = session.get(
                "input",
                {}
            )


            session_text += f"""

-----------------------------------

Predmet:
{session.get("subject", "Nije uneseno")}

Datum:
{session.get("date", "Nije uneseno")}

Bilješke:
{session.get("notes", "Nema bilješki")}

Sati sna:
{input_data.get("sleep_hours", "Nije uneseno")}

Trajanje učenja:
{input_data.get("study_duration", "Nije uneseno")} minuta

Broj pauza:
{input_data.get("breaks", "Nije uneseno")}

Vrijeme učenja:
{input_data.get("time_of_day", "Nije uneseno")} h

Fokus:
{input_data.get("focus", "Nije uneseno")}/10

Stres:
{input_data.get("stress", "Nije uneseno")}/10

Energija:
{input_data.get("energy", "Nije uneseno")}/10

Random Forest predikcija:
{session.get("result", "Nije dostupno")}

Vjerojatnost pozitivne predikcije:
{session.get("probability", 0) * 100}%

"""


            # Podaci koje frontend koristi u tablici
            formatted_sessions.append({

                "_id": str(
                    session.get("_id")
                ),

                "subject": session.get(
                    "subject",
                    ""
                ),

                "date": session.get(
                    "date",
                    ""
                ),

                "study_duration": input_data.get(
                    "study_duration"
                ),

                "sleep_hours": input_data.get(
                    "sleep_hours"
                ),

                "focus_level": input_data.get(
                    "focus"
                ),

                "stress_level": input_data.get(
                    "stress"
                ),

                "energy_level": input_data.get(
                    "energy"
                ),

                "prediction": session.get(
                    "result",
                    ""
                )
            })


        # =================================================
        # DETALJNI PROMPT
        # =================================================

        prompt = f"""
Ti si stručni AI mentor za studente.

Napraviti DETALJNU analizu studentskih navika učenja
na temelju posljednjih 10 sesija.

Važno:

Nemoj samo opisivati pojedinačne sesije.

Pronađi obrasce i povezanosti između:

- količine sna
- trajanja učenja
- broja pauza
- vremena učenja
- fokusa
- stresa
- energije
- predmeta
- rezultata Random Forest modela

Podaci o sesijama:

{session_text}


Analizu napiši na hrvatskom jeziku.

Koristi sljedeću strukturu:

1. OPĆA PROCJENA

Procijeni ukupne navike učenja i opće stanje.

2. SAN I OPORAVAK

Analiziraj količinu sna i objasni kako se povezuje
s fokusom, energijom i uspješnošću učenja.

3. TRAJANJE UČENJA I PAUZE

Analiziraj trajanje sesija i broj pauza.
Procijeni postoje li znakovi predugog ili prekratkog
učenja bez odgovarajućih pauza.

4. FOKUS, STRES I ENERGIJA

Analiziraj njihove međusobne odnose i istakni
najvažnije obrasce.

5. VRIJEME UČENJA

Analiziraj u koje vrijeme se najčešće uči i
postoje li razlike u kvaliteti sesija ovisno
o vremenu dana.

6. PREDMETI

Ako postoje podaci o predmetima, usporedi navike
učenja između predmeta.

7. RANDOM FOREST PREDIKCIJE

Objasni što rezultati modela govore o uvjetima
u kojima je studentu učenje povoljnije ili manje
povoljno.

8. GLAVNI PROBLEMI

Navedi najvažnije probleme koje si uočio.

9. KONKRETNE PREPORUKE

Daj konkretne i realne preporuke koje student može
primijeniti.

10. ZAKLJUČAK

Napiši kratak zaključak o trenutnim navikama učenja
i najvažnijem koraku za njihovo poboljšanje.

Nemoj izmišljati podatke koji nisu prisutni.
Ako za neku procjenu nema dovoljno podataka,
jasno to navedi.
"""


        # =================================================
        # AKO NEMA xAI KLIJENTA
        # =================================================

        if client is None:

            ai_text = (
                "Na temelju zabilježenih sesija moguće je "
                "pratiti obrasce sna, fokusa, stresa, energije "
                "i trajanja učenja. Za kvalitetnije zaključke "
                "preporučuje se nastaviti bilježiti sesije."
            )

        else:

            # =============================================
            # POZIV AI MODELA
            # =============================================

            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "Ti si stručni AI mentor koji analizira "
                            "studentske navike učenja."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.7
            )


            ai_text = response.choices[0].message.content


        return jsonify({

            "analysis": ai_text,

            "sessions": formatted_sessions
        })


    except Exception as e:

        print(
            "Greška kod full-analysis:",
            str(e)
        )

        return jsonify({
            "error": "Nije moguće generirati detaljnu AI analizu."
        }), 500


# =========================================================
# POSTOJEĆA GROK ANALIZA ZA /analyze
# =========================================================

def grok_analysis(data, prediction):

    prompt = f"""
Ti si AI mentor za studente.

Analiziraj navike učenja.

Predmet:
{data.get('subject')}

Sati sna:
{data.get('sleep_hours')}

Trajanje učenja:
{data.get('study_duration')} minuta

Broj pauza:
{data.get('breaks')}

Vrijeme učenja:
{data.get('time_of_day')} h

Fokus:
{data.get('focus')}/10

Stres:
{data.get('stress')}/10

Energija:
{data.get('energy')}/10

Random Forest predikcija:
{prediction}

Napiši odgovor na hrvatskom jeziku:

1. Procjena trenutnog stanja
2. Glavni problemi
3. Konkretne preporuke za poboljšanje
"""


    if client is None:

        return (
            f"Za predmet '{data.get('subject', 'nepoznat')}' "
            f"zabilježena je sesija učenja s fokusom "
            f"{data.get('focus')}/10 i stresom "
            f"{data.get('stress')}/10. "
            "Preporuka je održavati redovite pauze "
            "i povećati količinu sna prije učenja."
        )


    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "Ti si stručni AI asistent za analizu studentskih navika."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7
        )


        return response.choices[0].message.content


    except Exception as e:

        print(
            "Greška kod xAI analize:",
            str(e)
        )

        return (
            f"Za predmet '{data.get('subject', 'nepoznat')}' "
            f"zabilježena je sesija učenja s fokusom "
            f"{data.get('focus')}/10 i stresom "
            f"{data.get('stress')}/10. "
            "Preporuka je održavati redovite pauze "
            "i povećati količinu sna prije učenja."
        )