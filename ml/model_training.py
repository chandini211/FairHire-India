"""
FairHire India - Model Training Pipeline
Trains Logistic Regression, Random Forest, and Decision Tree classifiers on the 1,000-record dataset.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Tuple

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from config import (
    LOGISTIC_REGRESSION_PATH, RANDOM_FOREST_PATH, DECISION_TREE_PATH,
    MODEL_METRICS_PATH, RANDOM_STATE
)
from ml.data_loader import load_processed_1000_data
from ml.preprocessing import prepare_train_test_data, save_preprocessor
from ml.evaluation import evaluate_classifier

def train_all_models() -> Dict[str, Any]:
    """Train, evaluate, and persist all three classification models."""
    df = load_processed_1000_data()

    # Preprocess & split into train/test
    (
        X_train, X_test, y_train, y_test, A_train, A_test,
        preprocessor, feature_names
    ) = prepare_train_test_data(df, test_size=0.20, random_state=RANDOM_STATE)

    # Save fitted preprocessor
    save_preprocessor(preprocessor)

    # Model 1: Logistic Regression
    lr = LogisticRegression(C=1.0, max_iter=1000, random_state=RANDOM_STATE)
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_proba = lr.predict_proba(X_test)[:, 1]
    lr_metrics = evaluate_classifier(y_test, lr_pred, lr_proba)
    lr_importances = dict(zip(feature_names, np.abs(lr.coef_[0])))
    joblib.dump(lr, LOGISTIC_REGRESSION_PATH)

    # Model 2: Random Forest Classifier
    rf = RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=3, random_state=RANDOM_STATE)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_proba = rf.predict_proba(X_test)[:, 1]
    rf_metrics = evaluate_classifier(y_test, rf_pred, rf_proba)
    rf_importances = dict(zip(feature_names, rf.feature_importances_))
    joblib.dump(rf, RANDOM_FOREST_PATH)

    # Model 3: Decision Tree Classifier
    dt = DecisionTreeClassifier(max_depth=6, min_samples_split=10, min_samples_leaf=4, random_state=RANDOM_STATE)
    dt.fit(X_train, y_train)
    dt_pred = dt.predict(X_test)
    dt_proba = dt.predict_proba(X_test)[:, 1]
    dt_metrics = evaluate_classifier(y_test, dt_pred, dt_proba)
    dt_importances = dict(zip(feature_names, dt.feature_importances_))
    joblib.dump(dt, DECISION_TREE_PATH)

    # Bundle all evaluation records
    results = {
        "models": {
            "Logistic Regression": {
                "metrics": lr_metrics,
                "feature_importance": lr_importances,
                "predictions": lr_pred.tolist(),
                "probabilities": lr_proba.tolist()
            },
            "Random Forest": {
                "metrics": rf_metrics,
                "feature_importance": rf_importances,
                "predictions": rf_pred.tolist(),
                "probabilities": rf_proba.tolist()
            },
            "Decision Tree": {
                "metrics": dt_metrics,
                "feature_importance": dt_importances,
                "predictions": dt_pred.tolist(),
                "probabilities": dt_proba.tolist()
            }
        },
        "test_labels": y_test.tolist(),
        "test_protected": A_test.tolist(),
        "feature_names": feature_names,
        "sample_size_train": len(y_train),
        "sample_size_test": len(y_test)
    }

    joblib.dump(results, MODEL_METRICS_PATH)
    print("All models trained, evaluated, and saved successfully.")
    return results

def load_trained_model(model_name: str):
    """Load specified trained model."""
    if model_name == "Logistic Regression":
        return joblib.load(LOGISTIC_REGRESSION_PATH)
    elif model_name == "Random Forest":
        return joblib.load(RANDOM_FOREST_PATH)
    elif model_name == "Decision Tree":
        return joblib.load(DECISION_TREE_PATH)
    else:
        raise ValueError(f"Unknown model name: {model_name}")

if __name__ == "__main__":
    train_all_models()
