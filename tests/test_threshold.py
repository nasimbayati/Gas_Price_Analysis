import pandas as pd
from gas_price_insights.threshold_classifier import classify_by_threshold

def test_classify_by_threshold():
    idx = pd.to_datetime(["2024-01-01","2024-01-02","2024-01-03"])
    s = pd.Series([2.5, 3.0, 3.5], index=idx)
    labels = classify_by_threshold(s, threshold=3.0)
    assert list(labels.values) == [-1, 0, 1]
