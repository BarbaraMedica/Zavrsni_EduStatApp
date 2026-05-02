from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# učitaj model
model = joblib.load("../model/model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

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

        prediction = model.predict(features)
        probability = model.predict_proba(features)[0][1]

        if prediction[0] == 1:
            result = "Dobro vrijeme za učenje"
        else:
            result = "Nije dobro vrijeme za učenje"

        return jsonify({
            "rezultat": result,
            "vjerojatnost": round(float(probability), 2)
        })

    except KeyError as e:
        return jsonify({"error": f"Nedostaje podatak: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True)