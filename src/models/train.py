import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np
from src.data.simulate import simulate_health_data, save_simulated_data
from src.models.anomaly import AnomalyDetector


def inject_anomalies(df: pd.DataFrame, n_anom: int = 10) -> pd.DataFrame:
    df = df.copy()
    idx = np.random.choice(df.index, size=n_anom, replace=False)
    # Create artificial anomalies: very high heart rate and low SpO2
    df.loc[idx, 'heart_rate'] = df.loc[idx, 'heart_rate'] + np.random.randint(30, 60, size=n_anom)
    df.loc[idx, 'blood_oxygen'] = df.loc[idx, 'blood_oxygen'] - np.random.randint(5, 12, size=n_anom)
    df['label'] = 0
    df.loc[idx, 'label'] = 1
    return df


def main():
    df = simulate_health_data(1000)
    df = inject_anomalies(df, n_anom=40)
    save_simulated_data(df, path='data_simulated.csv')

    X = df[['heart_rate', 'blood_oxygen']]
    y = df['label']

    # Use a train/test split to demonstrate evaluation; IsolationForest is unsupervised,
    # so here we just show how it discovers injected anomalies.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    detector = AnomalyDetector(contamination=0.05)
    detector.fit(X_train)

    preds = detector.predict(X_test)
    y_pred = np.where(preds == 'Anomaly', 1, 0)

    print(classification_report(y_test, y_pred, digits=4))
    detector.save('model.joblib')
    print('Trained and saved model to model.joblib')


if __name__ == '__main__':
    main()
