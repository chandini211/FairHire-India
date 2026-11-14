"""
FairHire India - Algorithmic Fairness Metrics Framework
Utilizes Fairlearn to compute group disparities, demographic parity, and equalized odds.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from fairlearn.metrics import (
    MetricFrame,
    selection_rate,
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    true_positive_rate,
    false_positive_rate
)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

MIN_SUBGROUP_SIZE_THRESHOLD = 30

def compute_group_fairness_metrics(
    y_true: pd.Series,
    y_pred: np.ndarray,
    sensitive_features: pd.Series,
    group_names: Optional[Dict[Any, str]] = None
) -> Dict[str, Any]:
    """
    Calculate comprehensive Fairlearn metrics comparing protected groups.
    Aligns protected attribute values strictly with held-out test set predictions.
    """
    if group_names is None:
        group_names = {0: "Female / Non-Traditional", 1: "Male / Traditional"}

    # Subgroup sample size check & warnings
    group_counts = sensitive_features.value_counts().to_dict()
    warnings = []
    for grp, cnt in group_counts.items():
        if cnt < MIN_SUBGROUP_SIZE_THRESHOLD:
            warnings.append(f"Subgroup '{group_names.get(grp, grp)}' sample size ({cnt}) is below recommended threshold ({MIN_SUBGROUP_SIZE_THRESHOLD}). Interpret metrics cautiously.")

    # Fairlearn MetricFrame with standard recruitment metrics
    metrics_dict = {
        "selection_rate": selection_rate,
        "true_positive_rate": true_positive_rate,
        "false_positive_rate": false_positive_rate,
        "accuracy": accuracy_score,
        "precision": lambda y, p: precision_score(y, p, zero_division=0),
        "recall": lambda y, p: recall_score(y, p, zero_division=0),
        "f1": lambda y, p: f1_score(y, p, zero_division=0)
    }

    mf = MetricFrame(
        metrics=metrics_dict,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )

    # Disparity calculations
    dp_diff = float(demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_features))
    dp_ratio = float(demographic_parity_ratio(y_true, y_pred, sensitive_features=sensitive_features))
    eq_odds_diff = float(equalized_odds_difference(y_true, y_pred, sensitive_features=sensitive_features))

    # Overall and per-group series
    by_group = {}
    for grp in mf.by_group.index:
        grp_label = group_names.get(grp, str(grp))
        by_group[grp_label] = {
            "count": int(group_counts.get(grp, 0)),
            "selection_rate": float(mf.by_group.loc[grp, "selection_rate"]),
            "tpr": float(mf.by_group.loc[grp, "true_positive_rate"]),
            "fpr": float(mf.by_group.loc[grp, "false_positive_rate"]),
            "accuracy": float(mf.by_group.loc[grp, "accuracy"]),
            "precision": float(mf.by_group.loc[grp, "precision"]),
            "recall": float(mf.by_group.loc[grp, "recall"]),
            "f1": float(mf.by_group.loc[grp, "f1"])
        }

    overall = {
        "selection_rate": float(mf.overall["selection_rate"]),
        "accuracy": float(mf.overall["accuracy"]),
        "precision": float(mf.overall["precision"]),
        "recall": float(mf.overall["recall"]),
        "f1": float(mf.overall["f1"]),
        "demographic_parity_difference": dp_diff,
        "demographic_parity_ratio": dp_ratio,
        "equalized_odds_difference": eq_odds_diff
    }

    # Plain-language compliance assessments
    compliance_status = {
        "four_fifths_rule": dp_ratio >= 0.80,
        "demographic_parity_compliant": abs(dp_diff) <= 0.10,
        "equalized_odds_compliant": abs(eq_odds_diff) <= 0.10
    }

    return {
        "overall": overall,
        "by_group": by_group,
        "disparities": {
            "demographic_parity_difference": dp_diff,
            "demographic_parity_ratio": dp_ratio,
            "equalized_odds_difference": eq_odds_diff
        },
        "compliance": compliance_status,
        "warnings": warnings,
        "subgroup_counts": group_counts
    }
