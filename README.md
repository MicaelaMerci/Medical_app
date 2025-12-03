<!--
Place an image at `assets/screenshot.png` and a demo video at `assets/demo.mp4`.
You can replace or update these files with your own screenshots / recordings.
-->

![Project screenshot](assets/images/Medical_App.png)

# AI-Powered Health Monitoring System

Professional, minimal prototype demonstrating real-time wearable health monitoring, anomaly detection, and a user-facing dashboard.

Overview
--------
- Real-time health monitoring (simulated data)
- Anomaly detection using IsolationForest (unsupervised) with a rule-based fallback
- Live web dashboard showing metrics and time-series charts
- Simple training script and Dockerfile for quick deployment

Preview
-------
- Demo video:

![Demo video:](assets//videos/Medical_App.mp4)

Quickstart (developer)
----------------------
These steps assume you have Python 3.9+ and Docker (optional) installed.

1. Create and activate a virtual environment, install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Optional) Train the example anomaly detector and generate `model.joblib`:

```powershell
python -m src.models.train
```

3. Run the Flask web app locally:

```powershell
python -m src.app.app
```

4. Open the dashboard at: `http://127.0.0.1:5000`

Docker (quick demo)
-------------------
Build and run a container for quick sharing or demoing (development image):

```powershell
docker build -t health-monitor .
docker run -p 5000:5000 health-monitor
```

Project layout
--------------
- `src/data/simulate.py` — data simulation utilities
- `src/models/anomaly.py` — IsolationForest wrapper and save/load helpers
- `src/models/train.py` — trains model on simulated data and saves `model.joblib`
- `src/app/app.py` — Flask app and API endpoints
- `src/app/templates/index.html` — simple dashboard UI
- `src/app/static/js/dashboard.js` — Chart.js dashboard logic
- `Dockerfile`, `requirements.txt`, `.gitignore`, `tests/`

Testing
-------
Run the unit tests with `pytest`:

```powershell
pytest -q
```
