"""
FairHire India - Algorithmic Bias Mitigation
Implements Fairlearn ExponentiatedGradient reduction to enforce Equalized Odds / Demographic Parity.
Compares baseline unmitigated model vs mitigated model on identical held-out test data.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from fairlearn.reductions import ExponentiatedGradient, EqualizedOdds, DemographicParity

from config import (
    MITIGATED_MODEL_PATH, FAIRNESS_METRICS_PATH, RANDOM_STATE
)
from ml.data_loader import load_processed_1000_data
from ml.preprocessing import prepare_train_test_data
from fairness.metrics import compute_group_fairness_metrics

def run_mitigation_experiment(constraint_type: str = "EqualizedOdds") -> Dict[str, Any]:
    """
    Run in-processing bias mitigation using Fairlearn ExponentiatedGradient.
    Evaluates both baseline and mitigated models on the exact same test partition.
    """
    df = load_processed_1000_data()
    (
        X_train, X_test, y_train, y_test, A_train, A_test,
        preprocessor, feature_names
    ) = prepare_train_test_data(df, test_size=0.20, random_state=RANDOM_STATE)

    # 1. Baseline Model (Unmitigated Logistic Regression)
    base_model = LogisticRegression(C=1.0, max_iter=1000, random_state=RANDOM_STATE)
    base_model.fit(X_train, y_train)
    base_pred = base_model.predict(X_test)
    base_proba = base_model.predict_proba(X_test)[:, 1]

    # Baseline Fairness Metrics
    base_fairness = compute_group_fairness_metrics(y_test, base_pred, A_test)

    # 2. Mitigation via ExponentiatedGradient
    if constraint_type == "DemographicParity":
        constraint = DemographicParity()
    else:
        constraint = EqualizedOdds()

    mitigator = ExponentiatedGradient(
        estimator=LogisticRegression(C=1.0, max_iter=1000, random_state=RANDOM_STATE),
        constraints=constraint,
        eps=0.01,
        max_iter=50
    )

    mitigator.fit(X_train, y_train, sensitive_features=A_train)
    mit_pred = mitigator.predict(X_test)

    # Mitigated Fairness Metrics
    mit_fairness = compute_group_fairness_metrics(y_test, mit_pred, A_test)

    # Save mitigated model
    joblib.dump(mitigator, MITIGATED_MODEL_PATH)

    # Comparison Table
    comparison = {
        "Baseline": {
            "accuracy": float(accuracy_score(y_test, base_pred)),
            "precision": float(precision_score(y_test, base_pred, zero_division=0)),
            "recall": float(recall_score(y_test, base_pred, zero_division=0)),
            "f1_score": float(f1_score(y_test, base_pred, zero_division=0)),
            "demographic_parity_diff": base_fairness["disparities"]["demographic_parity_difference"],
            "demographic_parity_ratio": base_fairness["disparities"]["demographic_parity_ratio"],
            "equalized_odds_diff": base_fairness["disparities"]["equalized_odds_difference"],
            "group_0_selection_rate": base_fairness["by_group"]["Female / Non-Traditional"]["selection_rate"],
            "group_1_selection_rate": base_fairness["by_group"]["Male / Traditional"]["selection_rate"],
            "group_0_tpr": base_fairness["by_group"]["Female / Non-Traditional"]["tpr"],
            "group_1_tpr": base_fairness["by_group"]["Male / Traditional"]["tpr"],
            "group_0_fpr": base_fairness["by_group"]["Female / Non-Traditional"]["fpr"],
            "group_1_fpr": base_fairness["by_group"]["Male / Traditional"]["fpr"],
        },
        "Mitigated": {
            "accuracy": float(accuracy_score(y_test, mit_pred)),
            "precision": float(precision_score(y_test, mit_pred, zero_division=0)),
            "recall": float(recall_score(y_test, mit_pred, zero_division=0)),
            "f1_score": float(f1_score(y_test, mit_pred, zero_division=0)),
            "demographic_parity_diff": mit_fairness["disparities"]["demographic_parity_difference"],
            "demographic_parity_ratio": mit_fairness["disparities"]["demographic_parity_ratio"],
            "equalized_odds_diff": mit_fairness["disparities"]["equalized_odds_difference"],
            "group_0_selection_rate": mit_fairness["by_group"]["Female / Non-Traditional"]["selection_rate"],
            "group_1_selection_rate": mit_fairness["by_group"]["Male / Traditional"]["selection_rate"],
            "group_0_tpr": mit_fairness["by_group"]["Female / Non-Traditional"]["tpr"],
            "group_1_tpr": mit_fairness["by_group"]["Male / Traditional"]["tpr"],
            "group_0_fpr": mit_fairness["by_group"]["Female / Non-Traditional"]["fpr"],
            "group_1_fpr": mit_fairness["by_group"]["Male / Traditional"]["fpr"],
        }
    }

    results = {
        "constraint_type": constraint_type,
        "baseline_fairness": base_fairness,
        "mitigated_fairness": mit_fairness,
        "comparison": comparison
    }

    joblib.dump(results, FAIRNESS_METRICS_PATH)
    print("Fairlearn mitigation experiment executed and results saved.")
    return results

if __name__ == "__main__":
    run_mitigation_experiment()
