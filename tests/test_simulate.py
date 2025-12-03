from src.data.simulate import simulate_health_data


def test_simulate_columns():
    df = simulate_health_data(10)
    assert 'heart_rate' in df.columns
    assert 'blood_oxygen' in df.columns
    assert 'activity_level' in df.columns
