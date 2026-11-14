"""
FairHire India - Data Loading and Validation Module
Loads raw and 1,000-record processed dataset with schema checks, validation rules, and caching.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
from config import RAW_DATA_PATH, DATASET_1000_PATH, TARGET_COLUMN, PROTECTED_ATTRIBUTE, RANDOM_STATE

REQUIRED_COLUMNS = [
    "Age", "Gender", "EducationLevel", "ExperienceYears", "PreviousCompanies",
    "DistanceFromCompany", "InterviewScore", "SkillScore", "PersonalityScore",
    "RecruitmentStrategy", "HiringDecision"
]

def load_processed_1000_data(data_path: Optional[Path] = None) -> pd.DataFrame:
    """Load the final 1,000-record modeling dataset."""
    target_path = data_path or DATASET_1000_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Processed 1,000-record dataset not found at {target_path}. Run sampling first.")
    df = pd.read_csv(target_path)
    assert len(df) == 1000, f"Expected exactly 1,000 records, found {len(df)}"
    return df

def load_raw_data(data_path: Optional[Path] = None) -> pd.DataFrame:
    """Load the full source dataset."""
    target_path = data_path or RAW_DATA_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Source recruitment dataset not found at {target_path}")
    df = pd.read_csv(target_path)
    return df

def validate_dataset_schema(df: pd.DataFrame) -> Tuple[bool, str, Dict[str, Any]]:
    """Validate schema, nulls, duplicates, and column types."""
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {missing_cols}", {}

    report = {
        "record_count": len(df),
        "column_count": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "columns": list(df.columns),
        "dtypes": {c: str(df[c].dtype) for c in df.columns},
        "target_distribution": df[TARGET_COLUMN].value_counts().to_dict() if TARGET_COLUMN in df else {},
        "protected_distribution": df[PROTECTED_ATTRIBUTE].value_counts().to_dict() if PROTECTED_ATTRIBUTE in df else {}
    }
    return True, "Dataset schema is valid.", report

def get_eda_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute comprehensive descriptive statistics for EDA."""
    num_cols = ["Age", "ExperienceYears", "PreviousCompanies", "DistanceFromCompany",
                "InterviewScore", "SkillScore", "PersonalityScore"]
    cat_cols = ["Gender", "EducationLevel", "RecruitmentStrategy", "HiringDecision"]

    summary = {
        "shape": df.shape,
        "describe_numerical": df[num_cols].describe().round(2).to_dict(),
        "categorical_counts": {c: df[c].value_counts().to_dict() for c in cat_cols if c in df.columns},
        "correlations": df.corr().round(4).to_dict(),
        "missing_by_column": df.isnull().sum().to_dict()
    }
    return summary
