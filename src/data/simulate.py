import pandas as pd
import numpy as np
from pathlib import Path


def simulate_health_data(periods: int = 100, freq: str = 'T') -> pd.DataFrame:
    """Simulate wearable health metrics.

    Returns a DataFrame with timestamp, heart_rate, blood_oxygen, and activity_level.
    """
    timestamps = pd.date_range(start=pd.Timestamp.now().floor('min'), periods=periods, freq=freq)
    heart_rate = np.random.randint(55, 110, size=periods)
    blood_oxygen = np.random.randint(88, 101, size=periods)
    activity_level = np.random.choice(['low', 'moderate', 'high'], size=periods, p=[0.6, 0.3, 0.1])

    df = pd.DataFrame({
        'timestamp': timestamps,
        'heart_rate': heart_rate,
        'blood_oxygen': blood_oxygen,
        'activity_level': activity_level
    })
    return df


def save_simulated_data(df: pd.DataFrame, path: str = 'data_simulated.csv') -> Path:
    p = Path(path)
    df.to_csv(p, index=False)
    return p


if __name__ == '__main__':
    df = simulate_health_data(500)
    save_simulated_data(df)
    print('Saved simulated data to data_simulated.csv')
