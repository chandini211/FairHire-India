"""
FairHire India - Preprocessing Pipeline
Reproducible feature transformation using Scikit-learn Pipeline and ColumnTransformer.
Gender (protected attribute) is intentionally excluded from prediction features.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Tuple, List, Optional
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from config import (
    NUMERICAL_FEATURES, CATEGORICAL_FEATURES, TARGET_COLUMN,
    PROTECTED_ATTRIBUTE, PREPROCESSOR_PATH, RANDOM_STATE
)

def build_preprocessing_pipeline() -> ColumnTransformer:
    """
    Construct the ColumnTransformer pipeline.
    Applies Median Imputation + Standard Scaling to numerical features.
    Applies Most-Frequent Imputation + One-Hot Encoding to categorical features.
    """
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERICAL_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES)
        ],
        remainder="drop"  # Strictly drops protected attributes (Gender) and extraneous columns
    )
    return preprocessor

def prepare_train_test_data(
    df: pd.DataFrame,
    test_size: float = 0.20,
    random_state: int = RANDOM_STATE
) -> Tuple[np.ndarray, np.ndarray, pd.Series, pd.Series, pd.Series, pd.Series, ColumnTransformer, List[str]]:
    """
    Split dataset into training and testing partitions using stratified sampling.
    Returns:
    - X_train_transformed, X_test_transformed
    - y_train, y_test
    - A_train, A_test (Protected attribute: Gender)
    - fitted_preprocessor
    - feature_names
    """
    # Verify protected attribute exists
    assert PROTECTED_ATTRIBUTE in df.columns, f"Missing protected attribute '{PROTECTED_ATTRIBUTE}'"
    assert TARGET_COLUMN in df.columns, f"Missing target column '{TARGET_COLUMN}'"

    # Separate target, protected attribute, and candidate features
    y = df[TARGET_COLUMN].copy()
    A = df[PROTECTED_ATTRIBUTE].copy()

    # Features strictly exclude Gender and Target
    feature_cols = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
    X = df[feature_cols].copy()

    # Stratify train-test split on joint (Target + Gender) to guarantee demographic parity in splits
    strata = y.astype(str) + "_" + A.astype(str)
    X_train, X_test, y_train, y_test, A_train, A_test = train_test_split(
        X, y, A, test_size=test_size, stratify=strata, random_state=random_state
    )

    # Build and fit preprocessor strictly on training data
    preprocessor = build_preprocessing_pipeline()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # Retrieve transformed feature names
    feature_names = get_transformed_feature_names(preprocessor)

    return (
        X_train_transformed,
        X_test_transformed,
        y_train.reset_index(drop=True),
        y_test.reset_index(drop=True),
        A_train.reset_index(drop=True),
        A_test.reset_index(drop=True),
        preprocessor,
        feature_names
    )

def get_transformed_feature_names(preprocessor: ColumnTransformer) -> List[str]:
    """Extract interpretable feature names from fitted ColumnTransformer."""
    feature_names = []
    # Numerical
    feature_names.extend(NUMERICAL_FEATURES)
    # Categorical OneHot
    cat_encoder = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    cat_features = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES)
    feature_names.extend(list(cat_features))
    return feature_names

def save_preprocessor(preprocessor: ColumnTransformer, save_path: Optional[Path] = None) -> Path:
    target_path = save_path or PREPROCESSOR_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, target_path)
    return target_path

def load_preprocessor(load_path: Optional[Path] = None) -> ColumnTransformer:
    target_path = load_path or PREPROCESSOR_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Fitted preprocessor not found at {target_path}")
    return joblib.load(target_path)
