import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow React frontend to call this API

# ── Load model once on startup ──────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.pkl')

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")
else:
    print(f"⚠️  model.pkl not found at {MODEL_PATH}.")
    print("   Run project.py first (with the dataset CSV) to train and save the model.")

# ── Feature columns expected by the model ───────────────────────────────────
FEATURE_COLS = [
    'CPU Usage (%)',
    'Memory Usage (%)',
    'Clock Speed (GHz)',
    'Ambient Temperature (°C)',
    'Voltage (V)',
    'Current Load (A)',
    'Cache Miss Rate (%)',
    'Power Consumption (W)',
]

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict CPU temperature from system metrics.

    Expected JSON body:
    {
        "CPU Usage (%)": 68,
        "Memory Usage (%)": 67,
        "Clock Speed (GHz)": 3.5,
        "Ambient Temperature (°C)": 30,
        "Voltage (V)": 1.2,
        "Current Load (A)": 10,
        "Cache Miss Rate (%)": 5,
        "Power Consumption (W)": 80
    }
    """
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Run project.py with the dataset to generate model.pkl.'
        }), 503

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON body provided.'}), 400

    # Validate all required fields are present
    missing = [col for col in FEATURE_COLS if col not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    try:
        # Build a DataFrame that matches the model's training input
        user_input = pd.DataFrame(
            [[float(data[col]) for col in FEATURE_COLS]],
            columns=FEATURE_COLS
        )
        predicted_temp = model.predict(user_input)[0]
        return jsonify({
            'predicted_temp': round(float(predicted_temp), 2)
        })
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
