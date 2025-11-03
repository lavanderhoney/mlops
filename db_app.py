from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --Metrics --
RECORD_ADDED = Counter('dbapp_record_added_total', 'Total number of records added to the database')
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sl = db.Column(db.Float, nullable=False)
    sw = db.Column(db.Float, nullable=False)
    pl = db.Column(db.Float, nullable=False)
    pw = db.Column(db.Float, nullable=False)
    preds = db.Column(db.Integer, nullable=True)

@app.route('/add_record', methods=['POST'])
def store_prediction():
    data = request.get_json()
    new_prediction = Prediction(**data)
    db.session.add(new_prediction)
    db.session.commit()
    RECORD_ADDED.inc()  # Increment the counter
    return jsonify({'message': 'Prediction stored successfully!'}), 201

@app.route('/records', methods=['GET'])
def show_predictions():
    predictions = Prediction.query.all()
    result = [
        {'id': pred.id, 'sl': pred.sl, 'sw': pred.sw, 'pl': pred.pl, 'pw': pred.pw, 'preds': pred.preds}
        for pred in predictions
    ]
    return jsonify(result), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("DB app is running...")
    app.run(host='0.0.0.0', port=8001)
