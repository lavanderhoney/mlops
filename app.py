import os
import pickle
import requests
import numpy as np
from flask import Flask, jsonify, request, redirect, render_template
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'C:\\Users\\milap\\OneDrive\\Desktop\\CLG\\FINAL LAP\\7th Time\\MLOps\\monitoring\\flask_apps\\webapp\\iris_model.pkl'
DB_SERVICE_URL = "http://localhost:8001/add_record"
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# --MEtrics --
REQUEST_COUNT = Counter('webapp_request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('webapp_request_latency_seconds', 'Request latency', ['endpoint'])

@app.before_request
def before_request():
    REQUEST_COUNT.labels(request.method, request.path).inc() 
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
@REQUEST_LATENCY.labels('/predict').time()
def predict():
    if request.method == 'GET':
        return redirect('/')
    # Extract features from form
    try:
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
    except (KeyError, ValueError):
        return "Invalid input", 400

    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(features)[0]
    print("Prediction made", prediction)

    db_response = requests.post(DB_SERVICE_URL, json={
        'sl': sepal_length,
        'sw': sepal_width,
        'pl': petal_length,
        'pw': petal_width,
        'preds' : int(prediction)
    })
    print("DB response:", db_response.text)
    return jsonify({'prediction': str(prediction)})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
# @app.route('/showpreds', methods=['GET'])
# def show_predictions():
#     db_response = requests.get('http://dbapp:5000/showpreds')
#     print("DB response:", db_response.text)
#     return render_template('predictions.html', data=db_response.json())

if __name__ == '__main__':
    # Run development server
    print("Web app is running...")
    app.run(host='0.0.0.0', port=8000)
