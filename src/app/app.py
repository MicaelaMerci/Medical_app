from flask import Flask, render_template, jsonify
from flask import Response
import pandas as pd
from src.data.simulate import simulate_health_data
from src.models.anomaly import AnomalyDetector
from pathlib import Path

app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent / 'templates'))

# Try to load a pre-trained model if present
detector = AnomalyDetector()
try:
    detector.load('model.joblib')
    MODEL_LOADED = True
except Exception:
    MODEL_LOADED = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/metrics')
def metrics():
    df = simulate_health_data(1)
    row = df.iloc[0]
    X = pd.DataFrame([row[['heart_rate', 'blood_oxygen']]])
    label = 'Unknown'
    if MODEL_LOADED:
        label = detector.predict(X)[0]
    else:
        # Simple rule-based fallback
        hr = int(row['heart_rate'])
        spo2 = int(row['blood_oxygen'])
        if hr < 50 or hr > 120 or spo2 < 90:
            label = 'Anomaly'
        else:
            label = 'Normal'

    return jsonify({
        'timestamp': str(row['timestamp']),
        'heart_rate': int(row['heart_rate']),
        'blood_oxygen': int(row['blood_oxygen']),
        'activity_level': row['activity_level'],
        'status': label
    })


@app.route('/api/history')
def history():
    # Return a small series of recent simulated points for charting
    df = simulate_health_data(periods=50, freq='T')
    rows = []
    for _, row in df.iterrows():
        X = pd.DataFrame([row[['heart_rate', 'blood_oxygen']]])
        if MODEL_LOADED:
            label = detector.predict(X)[0]
        else:
            hr = int(row['heart_rate'])
            spo2 = int(row['blood_oxygen'])
            label = 'Anomaly' if (hr < 50 or hr > 120 or spo2 < 90) else 'Normal'

        rows.append({
            'timestamp': str(row['timestamp']),
            'heart_rate': int(row['heart_rate']),
            'blood_oxygen': int(row['blood_oxygen']),
            'activity_level': row['activity_level'],
            'status': label
        })

    return jsonify(rows)


@app.route('/favicon.ico')
def favicon():
    # Return empty 204 to avoid browser 404 noise for missing favicon during development
    return Response(status=204)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
