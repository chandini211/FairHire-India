"""
Automated Tests — Machine Learning Models & Evaluation
Verifies Logistic Regression, Random Forest, Decision Tree training, persistence, and metric boundaries.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import joblib
import numpy as np

from config import MODEL_METRICS_PATH
from ml.model_training import train_all_models, load_trained_model
from ml.prediction import predict_candidate

@pytest.fixture(scope="module")
def trained_results():
    if MODEL_METRICS_PATH.exists():
        return joblib.load(MODEL_METRICS_PATH)
    return train_all_models()

def test_models_existence_and_loading():
    lr = load_trained_model("Logistic Regression")
    rf = load_trained_model("Random Forest")
    dt = load_trained_model("Decision Tree")

    assert lr is not None
    assert rf is not None
    assert dt is not None

def test_models_evaluation_metrics_boundaries(trained_results):
    models = trained_results["models"]
    assert "Logistic Regression" in models
    assert "Random Forest" in models
    assert "Decision Tree" in models

    for name, data in models.items():
        m = data["metrics"]
        # Verify valid probabilities and bounds
        assert 0.70 <= m["accuracy"] <= 1.0, f"{name} accuracy out of realistic bounds: {m['accuracy']}"
        assert 0.60 <= m["f1_score"] <= 1.0, f"{name} F1-score out of realistic bounds: {m['f1_score']}"
        assert 0.70 <= m["roc_auc"] <= 1.0, f"{name} ROC-AUC out of realistic bounds: {m['roc_auc']}"

        # Confusion matrix checks
        cm = m["confusion_matrix"]
        total_cm = cm["tp"] + cm["fp"] + cm["tn"] + cm["fn"]
        assert total_cm == 200, f"Confusion matrix sum should equal test set size (200), got {total_cm}"

def test_inference_pipeline():
    sample_candidate = {
        "Age": 29,
        "EducationLevel": 2,
        "ExperienceYears": 5,
        "PreviousCompanies": 2,
        "DistanceFromCompany": 12.0,
        "InterviewScore": 88.0,
        "SkillScore": 85.0,
        "PersonalityScore": 82.0,
        "RecruitmentStrategy": 1
    }

    pred = predict_candidate(sample_candidate, model_name="Random Forest")
    assert "prediction_label" in pred
    assert pred["prediction_label"] in [0, 1]
    assert 0.0 <= pred["prediction_probability"] <= 1.0
    assert len(pred["recommendation"]) > 0
