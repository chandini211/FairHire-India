"""
FairHire India - Configuration & Constants
HCLTech Career Shaper Project
Official Problem Statement: "Automate candidate shortlisting while minimizing bias using fair classification models."
"""
from pathlib import Path
import os

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent

# Application Meta
APP_NAME = "FairHire India"
APP_TAGLINE = "Recruitment Without Bias. By Design."
PROJECT_PROGRAM = "HCLTech Career Shaper"
OFFICIAL_PROBLEM_STATEMENT = "Automate candidate shortlisting while minimizing bias using fair classification models."

# Data Directories & Files
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RAW_DATA_PATH = DATA_DIR / "recruitment_data.csv"
DATASET_1000_PATH = PROCESSED_DATA_DIR / "recruitment_data_1000.csv"

# Models Directory
MODELS_DIR = BASE_DIR / "models"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
LOGISTIC_REGRESSION_PATH = MODELS_DIR / "logistic_regression.joblib"
RANDOM_FOREST_PATH = MODELS_DIR / "random_forest.joblib"
DECISION_TREE_PATH = MODELS_DIR / "decision_tree.joblib"
MITIGATED_MODEL_PATH = MODELS_DIR / "mitigated_model.joblib"
MODEL_METRICS_PATH = MODELS_DIR / "model_metrics.joblib"
FAIRNESS_METRICS_PATH = MODELS_DIR / "fairness_metrics.joblib"

# Database Directory
DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "fairhire.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"

# Assets Directory
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
FAVICON_PATH = ASSETS_DIR / "favicon.png"
ILLUSTRATIONS_DIR = ASSETS_DIR / "illustrations"

# Reports Directory
REPORTS_DIR = BASE_DIR / "reports"
DATASET_REPORTS_DIR = REPORTS_DIR / "dataset"
MODEL_REPORTS_DIR = REPORTS_DIR / "model_evaluation"
FAIRNESS_REPORTS_DIR = REPORTS_DIR / "fairness"
EXPORTS_DIR = REPORTS_DIR / "exports"

# Design System Color Palette (Strict Dark Enterprise Dashboard)
COLOR_PALETTE = {
    "main_bg": "#080B16",
    "sidebar_bg": "#111827",
    "card_bg": "#10182B",
    "primary_purple": "#6558F5",
    "cyan": "#22C3D6",
    "success_green": "#10B981",
    "warning_amber": "#F59E0B",
    "danger_red": "#EF4444",
    "main_text": "#F5F7FC",
    "secondary_text": "#94A3B8",
    "border": "#252D4A",
}

# Typography Specifications
FONTS = {
    "body": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "heading": "'Space Grotesk', -apple-system, sans-serif",
    "mono": "'IBM Plex Mono', monospace"
}

# Protected Attributes and Features
PROTECTED_ATTRIBUTE = "Gender"
TARGET_COLUMN = "HiringDecision"
FEATURE_COLUMNS = [
    "Age",
    "EducationLevel",
    "ExperienceYears",
    "PreviousCompanies",
    "DistanceFromCompany",
    "InterviewScore",
    "SkillScore",
    "PersonalityScore",
    "RecruitmentStrategy"
]

NUMERICAL_FEATURES = [
    "Age",
    "ExperienceYears",
    "PreviousCompanies",
    "DistanceFromCompany",
    "InterviewScore",
    "SkillScore",
    "PersonalityScore"
]

CATEGORICAL_FEATURES = [
    "EducationLevel",
    "RecruitmentStrategy"
]

# Random State for Reproducibility
RANDOM_STATE = 42

# Ensure core directories exist
for p in [PROCESSED_DATA_DIR, MODELS_DIR, DATABASE_DIR, ASSETS_DIR, ILLUSTRATIONS_DIR,
          DATASET_REPORTS_DIR, MODEL_REPORTS_DIR, FAIRNESS_REPORTS_DIR, EXPORTS_DIR]:
    p.mkdir(parents=True, exist_ok=True)
