"""
FairHire India - Demographic Group Analysis
Breaks down candidate shortlisting and historical trends across education, experience, and gender.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from typing import Dict, Any

from ml.data_loader import load_processed_1000_data

def get_demographic_breakdown() -> Dict[str, Any]:
    """Analyze group distributions, hiring rates, and disparities across demographic features."""
    df = load_processed_1000_data()

    # Education mapping
    edu_map = {1: "Bachelor's", 2: "Master's", 3: "PhD", 4: "Other / Diploma"}
    gender_map = {0: "Female / Non-Traditional", 1: "Male / Traditional"}
    strategy_map = {1: "Aggressive Sourcing", 2: "Moderate Sourcing", 3: "Campus / Passive"}

    df_named = df.copy()
    df_named["Education"] = df_named["EducationLevel"].map(edu_map)
    df_named["Gender_Label"] = df_named["Gender"].map(gender_map)
    df_named["Strategy"] = df_named["RecruitmentStrategy"].map(strategy_map)

    # 1. Gender hiring rates
    gender_stats = df_named.groupby("Gender_Label")["HiringDecision"].agg(["count", "mean", "sum"]).reset_index()
    gender_stats.columns = ["Gender", "Total Applicants", "Hiring Rate", "Hired Count"]
    gender_stats["Hiring Rate %"] = (gender_stats["Hiring Rate"] * 100).round(1)

    # 2. Education hiring rates
    edu_stats = df_named.groupby("Education")["HiringDecision"].agg(["count", "mean", "sum"]).reset_index()
    edu_stats.columns = ["Education", "Total Applicants", "Hiring Rate", "Hired Count"]
    edu_stats["Hiring Rate %"] = (edu_stats["Hiring Rate"] * 100).round(1)

    # 3. Strategy hiring rates
    strat_stats = df_named.groupby("Strategy")["HiringDecision"].agg(["count", "mean", "sum"]).reset_index()
    strat_stats.columns = ["Strategy", "Total Applicants", "Hiring Rate", "Hired Count"]
    strat_stats["Hiring Rate %"] = (strat_stats["Hiring Rate"] * 100).round(1)

    # 4. Cross-tabulation: Gender vs Education
    cross_gender_edu = pd.crosstab(df_named["Gender_Label"], df_named["Education"], values=df_named["HiringDecision"], aggfunc="mean").round(3)

    return {
        "gender_stats": gender_stats.to_dict(orient="records"),
        "education_stats": edu_stats.to_dict(orient="records"),
        "strategy_stats": strat_stats.to_dict(orient="records"),
        "cross_gender_edu": cross_gender_edu.to_dict()
    }
