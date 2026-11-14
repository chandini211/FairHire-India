"""
Automated Tests — Fairlearn Fairness Metrics & Mitigation Suite
Verifies MetricFrame group calculations, Demographic Parity, Equalized Odds, and in-processing mitigation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import joblib
import pandas as pd
import numpy as np

from config import FAIRNESS_METRICS_PATH
from fairness.metrics import compute_group_fairness_metrics
from fairness.mitigation import run_mitigation_experiment

def test_fairlearn_metric_frame_computation():
    # Synthetic aligned test series
    np.random.seed(42)
    y_true = pd.Series([1, 0, 1, 1, 0, 0, 1, 0, 1, 0] * 10)
    y_pred = np.array([1, 0, 1, 0, 0, 0, 1, 0, 1, 1] * 10)
    sensitive_features = pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1] * 10)

    res = compute_group_fairness_metrics(y_true, y_pred, sensitive_features)

    assert "disparities" in res
    assert "demographic_parity_difference" in res["disparities"]
    assert "demographic_parity_ratio" in res["disparities"]
    assert "equalized_odds_difference" in res["disparities"]
    assert "by_group" in res
    assert len(res["by_group"]) == 2

def test_fairlearn_mitigation_experiment_artifacts():
    if not FAIRNESS_METRICS_PATH.exists():
        run_mitigation_experiment()

    fdata = joblib.load(FAIRNESS_METRICS_PATH)
    comp = fdata["comparison"]

    assert "Baseline" in comp
    assert "Mitigated" in comp

    base = comp["Baseline"]
    mit = comp["Mitigated"]

    # Verify both models evaluated on test set
    assert 0.70 <= base["accuracy"] <= 1.0
    assert 0.70 <= mit["accuracy"] <= 1.0

    # Verify parity metric existence
    assert "demographic_parity_ratio" in base
    assert "demographic_parity_ratio" in mit
    assert "equalized_odds_diff" in base
    assert "equalized_odds_diff" in mit
