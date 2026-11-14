"""
FairHire India - LIME Explainability Framework
Local Interpretable Model-agnostic Explanations for individual candidate shortlisting predictions.
Note: Feature contribution is not proof of causation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from lime import lime_tabular

from ml.preprocessing import load_preprocessor, get_transformed_feature_names
from ml.model_training import load_trained_model
from ml.data_loader import load_processed_1000_data

CAUSATION_DISCLAIMER = "Feature contribution reflects local surrogate linear approximation and is not proof of causation."

def explain_candidate_lime(candidate_data: Dict[str, Any], model_name: str = "Random Forest") -> Dict[str, Any]:
    """Generate local LIME explanation for a single applicant."""
    preprocessor = load_preprocessor()
    model = load_trained_model(model_name)
    feature_names = get_transformed_feature_names(preprocessor)

    # Load training distribution for background reference
    df_all = load_processed_1000_data()
    feature_cols = [
        "Age", "EducationLevel", "ExperienceYears", "PreviousCompanies",
        "DistanceFromCompany", "InterviewScore", "SkillScore", "PersonalityScore",
        "RecruitmentStrategy"
    ]
    background_tr = preprocessor.transform(df_all[feature_cols][:150])

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
    X_candidate = preprocessor.transform(df_single)[0]

    # Instantiate LIME Tabular Explainer
    explainer = lime_tabular.LimeTabularExplainer(
        training_data=background_tr,
        feature_names=feature_names,
        class_names=["Not Shortlisted", "Shortlisted"],
        mode="classification",
        random_state=42
    )

    exp = explainer.explain_instance(
        data_row=X_candidate,
        predict_fn=model.predict_proba,
        num_features=8
    )

    exp_list = exp.as_list()
    contributions = []
    for rule, weight in exp_list:
        contributions.append({
            "rule": rule,
            "weight": float(weight),
            "abs_weight": abs(float(weight)),
            "direction": "Supports Shortlisting (+)" if weight > 0 else "Opposes Shortlisting (-)"
        })

    positives = [c for c in contributions if c["weight"] > 0]
    negatives = [c for c in contributions if c["weight"] < 0]

    return {
        "model_name": model_name,
        "rules": contributions,
        "top_positive": positives[:3],
        "top_negative": negatives[:3],
        "prediction_proba": float(model.predict_proba([X_candidate])[0][1]),
        "disclaimer": CAUSATION_DISCLAIMER
    }
