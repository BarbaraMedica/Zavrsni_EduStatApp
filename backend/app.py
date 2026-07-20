from flask import Flask
from flask_cors import CORS

from routes.predict import predict_bp
from routes.statistics import statistics_bp
from routes.data import data_bp
from routes.analysis import analysis_bp


app = Flask(__name__)

CORS(app)

app.register_blueprint(predict_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(data_bp)
app.register_blueprint(analysis_bp)
if __name__ == "__main__":
    app.run(debug=True)