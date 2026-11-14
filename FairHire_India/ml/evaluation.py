"""
FairHire India - Model Evaluation Framework
Calculates standard performance metrics, confusion matrices, ROC and PR curves.
"""
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)

def evaluate_classifier(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> Dict[str, Any]:
    """Calculate comprehensive evaluation metrics on held-out test data."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    # ROC-AUC calculation
    try:
        roc_auc = float(roc_auc_score(y_true, y_proba))
    except Exception:
        roc_auc = 0.5

    # ROC curve points
    fpr, tpr, roc_thresh = roc_curve(y_true, y_proba)

    # Precision-Recall curve points
    precision_vals, recall_vals, pr_thresh = precision_recall_curve(y_true, y_proba)

    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": roc_auc,
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
            "matrix": cm.tolist()
        },
        "classification_report": classification_report(y_true, y_pred, output_dict=True, zero_division=0),
        "roc_curve": {
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist()
        },
        "pr_curve": {
            "precision": precision_vals.tolist(),
            "recall": recall_vals.tolist()
        }
    }
    return metrics
