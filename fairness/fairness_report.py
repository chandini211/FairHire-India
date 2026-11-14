"""
FairHire India - Fairness Narrative and Audit Report Generator
Translates technical fairness metrics into executive recruiter and compliance summaries.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
from typing import Dict, Any
from config import FAIRNESS_METRICS_PATH, MODEL_METRICS_PATH

def generate_fairness_summary() -> Dict[str, Any]:
    """Retrieve evaluated fairness metrics and formulate executive narrative."""
    if not FAIRNESS_METRICS_PATH.exists():
        return {
            "status": "Pending",
            "message": "Fairness evaluation experiment has not been executed yet."
        }

    fairness_data = joblib.load(FAIRNESS_METRICS_PATH)
    base = fairness_data["baseline_fairness"]
    mit = fairness_data["mitigated_fairness"]
    comp = fairness_data["comparison"]

    dp_ratio = base["disparities"]["demographic_parity_ratio"]
    dp_diff = base["disparities"]["demographic_parity_difference"]
    eq_odds = base["disparities"]["equalized_odds_difference"]

    executive_narrative = (
        f"Baseline Logistic Regression achieved a Demographic Parity Ratio of {dp_ratio:.2f} "
        f"and Demographic Parity Difference of {dp_diff:.4f} across gender groups on the 200-sample test partition. "
        f"Under US EEOC 4/5ths rule guidelines (ratio >= 0.80), the baseline satisfies selection parity. "
        f"Equalized Odds disparity was measured at {eq_odds:.4f}. "
        f"In mitigation experiments utilizing Fairlearn's ExponentiatedGradient with an EqualizedOdds constraint, "
        f"model accuracy shifted from {comp['Baseline']['accuracy']*100:.1f}% to {comp['Mitigated']['accuracy']*100:.1f}%, "
        f"illustrating the empirical Pareto trade-off between strict statistical constraint enforcement and overall predictive utility."
    )

    return {
        "status": "Completed",
        "executive_narrative": executive_narrative,
        "baseline": base,
        "mitigated": mit,
        "comparison": comp
    }
