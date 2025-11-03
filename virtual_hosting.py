from flask import Flask, jsonify, request, redirect, render_template
import pickle
import numpy as np
import os
from waitress import serve  # <-- import waitress

app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'iris_model.pkl'
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    host = request.host.split(":")[0]  # strip port if present
    if host == "soothslayer.com" or host=="localhost":
        return render_template("index.html")
    elif host == "api.soothslayer.com":
        return jsonify({"message": "Welcome to the API"})
    else:
        return "Unknown host", 404

@app.route('/predict', methods=['POST', 'GET'])
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
    print("Prediction: ", prediction)
    return jsonify({'prediction': str(prediction)})

if __name__ == '__main__':
    # Run using Waitress instead of Flask’s built-in server
    print("Starting production server 1 on 8080 ...")
    serve(app, host="127.0.0.1", port=8080)
