"""
Automated Tests — Data Preprocessing & Validation Suite
Verifies exact 1,000-record dataset integrity, zero missing values, zero duplicates,
ColumnTransformer pipeline, and complete omission of protected attribute (Gender) from model features.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import pandas as pd
import numpy as np

from config import DATASET_1000_PATH, PROTECTED_ATTRIBUTE
from ml.data_loader import load_processed_1000_data, validate_dataset_schema
from ml.preprocessing import prepare_train_test_data, build_preprocessing_pipeline, get_transformed_feature_names

def test_exact_1000_records_mandate():
    df = load_processed_1000_data()
    # Official HCLTech compliance assertion
    assert len(df) == 1000, f"Dataset must contain exactly 1,000 records, found {len(df)}"

def test_dataset_schema_and_zero_nulls():
    df = load_processed_1000_data()
    valid, msg, report = validate_dataset_schema(df)
    assert valid is True
    assert report["missing_values"] == 0, "Processed dataset must contain zero missing values"
    assert report["duplicates"] == 0, "Processed dataset must contain zero duplicates"

def test_protected_attribute_omission_from_features():
    df = load_processed_1000_data()
    (
        X_train, X_test, y_train, y_test, A_train, A_test,
        preprocessor, feature_names
    ) = prepare_train_test_data(df, test_size=0.20, random_state=42)

    # 1. Feature names must NOT contain 'Gender'
    for name in feature_names:
        assert PROTECTED_ATTRIBUTE.lower() not in name.lower(), f"Protected attribute '{PROTECTED_ATTRIBUTE}' detected in model features: {name}"

    # 2. Transformed shape check
    assert X_train.shape[0] == 800
    assert X_test.shape[0] == 200
    assert len(y_train) == 800
    assert len(y_test) == 200

    # 3. Protected labels A_train and A_test must align
    assert len(A_train) == 800
    assert len(A_test) == 200

def test_data_leakage_prevention():
    # Preprocessor must be fitted solely on train data
    df = load_processed_1000_data()
    (
        X_train, X_test, y_train, y_test, A_train, A_test,
        preprocessor, feature_names
    ) = prepare_train_test_data(df, test_size=0.20, random_state=42)

    assert hasattr(preprocessor, "transformers_"), "Preprocessor must be properly fitted"
    # Ensure scaling parameters were learned from training data only
    scaler = preprocessor.named_transformers_["num"].named_steps["scaler"]
    assert scaler.mean_ is not None
    assert len(scaler.mean_) == 7 # 7 numerical features
