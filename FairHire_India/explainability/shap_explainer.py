"""
FairHire India - SHAP Explainability Framework
Computes local and global Shapley feature contributions using TreeExplainer and LinearExplainer.
Note: Feature contribution is not proof of causation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import shap
import pandas as pd
import numpy as np
from typing import Dict, Any, List

from ml.preprocessing import load_preprocessor, get_transformed_feature_names
from ml.model_training import load_trained_model
from ml.data_loader import load_processed_1000_data

CAUSATION_DISCLAIMER = "Feature contribution reflects model association and is not proof of causation."

def explain_candidate_shap(candidate_data: Dict[str, Any], model_name: str = "Random Forest") -> Dict[str, Any]:
    """Compute local SHAP explanation for a single applicant."""
    preprocessor = load_preprocessor()
    model = load_trained_model(model_name)
    feature_names = get_transformed_feature_names(preprocessor)

    # Prepare single candidate input
    input_row = {
        "Age": int(candidate_data.get("Age", 28)),
        "EducationLevel": int(candidate_data.get("EducationLevel", 2)),
        "ExperienceYears": int(candidate_data.get("ExperienceYears", 3)),
        "PreviousCompanies": int(candidate_data.get("PreviousCompanies", 1)),
        "DistanceFromCompany": float(candidate_data.get("DistanceFromCompany", 10.0)),
        "InterviewScore": float(candidate_data.get("InterviewScore", 75.0)),
        "SkillScore": float(candidate_data.get("SkillScore", 75.0)),
        "PersonalityScore": float(candidate_data.get("PersonalityScore", 75.0)),
        "RecruitmentStrategy": int(candidate_data.get("RecruitmentStrategy", 2))
    }

    df_single = pd.DataFrame([input_row])
    X_tr = preprocessor.transform(df_single)

    if model_name in ["Random Forest", "Decision Tree"]:
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X_tr)
        # Handle binary classification shapes (list of arrays or 3D array)
        if isinstance(shap_vals, list):
            sv = shap_vals[1][0] if len(shap_vals) > 1 else shap_vals[0][0]
        elif len(shap_vals.shape) == 3:
            sv = shap_vals[0, :, 1]
        else:
            sv = shap_vals[0]
        base_val = float(explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value)
    else:
        # Logistic Regression
        df_all = load_processed_1000_data()
        feature_cols = [c for c in input_row.keys()]
        background = preprocessor.transform(df_all[feature_cols][:100])
        explainer = shap.LinearExplainer(model, background)
        shap_vals = explainer.shap_values(X_tr)
        sv = shap_vals[0]
        base_val = float(explainer.expected_value)

    # Sort contributions
    contributions = []
    for name, val in zip(feature_names, sv):
        contributions.append({
            "feature": name,
            "shap_value": float(val),
            "abs_impact": abs(float(val)),
            "direction": "Positive (+)" if val > 0 else "Negative (-)"
        })

    contributions.sort(key=lambda x: x["abs_impact"], reverse=True)
    positives = [c for c in contributions if c["shap_value"] > 0]
    negatives = [c for c in contributions if c["shap_value"] < 0]

    return {
        "model_name": model_name,
        "base_value": base_val,
        "contributions": contributions,
        "top_positive": positives[:4],
        "top_negative": negatives[:4],
        "disclaimer": CAUSATION_DISCLAIMER
    }

def get_global_shap_importance(model_name: str = "Random Forest", sample_size: int = 150) -> List[Dict[str, Any]]:
    """Compute mean absolute SHAP values across background test population."""
    preprocessor = load_preprocessor()
    model = load_trained_model(model_name)
    feature_names = get_transformed_feature_names(preprocessor)

    df = load_processed_1000_data()
    feature_cols = [
        "Age", "EducationLevel", "ExperienceYears", "PreviousCompanies",
        "DistanceFromCompany", "InterviewScore", "SkillScore", "PersonalityScore",
        "RecruitmentStrategy"
    ]
    sample_df = df[feature_cols].sample(n=min(sample_size, len(df)), random_state=42)
    X_tr = preprocessor.transform(sample_df)

    if model_name in ["Random Forest", "Decision Tree"]:
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X_tr)
        if isinstance(shap_vals, list):
            sv = shap_vals[1] if len(shap_vals) > 1 else shap_vals[0]
        elif len(shap_vals.shape) == 3:
            sv = shap_vals[:, :, 1]
        else:
            sv = shap_vals
    else:
        explainer = shap.LinearExplainer(model, X_tr[:50])
        sv = explainer.shap_values(X_tr)

    mean_abs_impact = np.mean(np.abs(sv), axis=0)
    records = []
    for name, imp in zip(feature_names, mean_abs_impact):
        records.append({"feature": name, "mean_abs_shap": float(imp)})

    records.sort(key=lambda x: x["mean_abs_shap"], reverse=True)
    return records
