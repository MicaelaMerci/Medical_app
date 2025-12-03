import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from pathlib import Path


class AnomalyDetector:
    def __init__(self, contamination: float = 0.05, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(contamination=self.contamination, random_state=self.random_state)

    def fit(self, X):
        self.model.fit(X)
        return self

    def predict(self, X) -> np.ndarray:
        # returns 'Anomaly' or 'Normal' labels
        preds = self.model.predict(X)
        return np.where(preds == -1, 'Anomaly', 'Normal')

    def save(self, path: str = 'model.joblib') -> Path:
        p = Path(path)
        joblib.dump(self.model, p)
        return p

    def load(self, path: str = 'model.joblib'):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f'Model file not found: {p}')
        self.model = joblib.load(p)
        return self
