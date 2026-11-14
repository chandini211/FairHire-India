"""
FairHire India - Model Prediction & Inference Service
Performs single candidate and batch shortlisting inference using fitted preprocessors.
Predictions serve as decision-support signals, requiring human recruiter review.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from ml.preprocessing import load_preprocessor
from ml.model_training import load_trained_model

DEFAULT_MODEL = "Random Forest"

def predict_candidate(candidate_data: Dict[str, Any], model_name: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Generate shortlisting prediction for an individual candidate.
    Excludes protected attribute (Gender) from model inference.
    """
    preprocessor = load_preprocessor()
    model = load_trained_model(model_name)

    # Required feature fields
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

    df_input = pd.DataFrame([input_row])
    X_transformed = preprocessor.transform(df_input)

    pred_label = int(model.predict(X_transformed)[0])
    try:
        pred_proba = float(model.predict_proba(X_transformed)[0][1])
    except Exception:
        pred_proba = float(pred_label)

    # Human-in-the-loop recommendation text
    if pred_label == 1:
        if pred_proba >= 0.75:
            recommendation = "Strong Match — Recommended for Technical Interview"
        else:
            recommendation = "Moderate Match — Recommended for Recruiter Screening"
    else:
        if pred_proba <= 0.25:
            recommendation = "Does Not Meet Threshold — Secondary Human Review Advised"
        else:
            recommendation = "Borderline Evaluation — Holistic Recruiter Assessment Required"

    return {
        "model_name": model_name,
        "prediction_label": pred_label,
        "prediction_probability": pred_proba,
        "recommendation": recommendation,
        "transformed_features": X_transformed[0],
        "input_features": input_row
    }
