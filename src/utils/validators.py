"""
FinGuard AI - Validation Utilities
----------------------------------
Validation helpers for transaction and model inputs.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PROJECT CONSTANTS
# ============================================================

EXPECTED_FEATURE_COUNT = 53

ALLOWED_RISK_LEVELS = {
    "LOW",
    "MEDIUM",
    "HIGH"
}


# ============================================================
# GENERAL VALIDATION
# ============================================================

def validate_dataframe(data):
    """
    Validate that the supplied object is a non-empty DataFrame.
    """

    if data is None:
        raise ValueError("Input data cannot be None.")

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a pandas DataFrame.")

    if data.empty:
        raise ValueError("Input DataFrame is empty.")

    return True


# ============================================================
# FEATURE COUNT VALIDATION
# ============================================================

def validate_feature_count(
    data,
    expected_features=EXPECTED_FEATURE_COUNT
):
    """
    Validate the number of model input features.
    """

    validate_dataframe(data)

    actual_features = data.shape[1]

    if actual_features != expected_features:
        raise ValueError(
            f"Invalid feature count. "
            f"Expected {expected_features}, "
            f"received {actual_features}."
        )

    return True


# ============================================================
# NUMERIC VALIDATION
# ============================================================

def validate_numeric_data(data):
    """
    Validate that all DataFrame values are numeric.
    """

    validate_dataframe(data)

    non_numeric_columns = data.select_dtypes(
        exclude=[np.number]
    ).columns.tolist()

    if non_numeric_columns:
        raise ValueError(
            "Non-numeric columns detected: "
            f"{non_numeric_columns}"
        )

    return True


# ============================================================
# MISSING VALUE VALIDATION
# ============================================================

def validate_missing_values(data):
    """
    Check whether missing values are present.
    """

    validate_dataframe(data)

    missing_count = int(data.isnull().sum().sum())

    if missing_count > 0:
        raise ValueError(
            f"Input contains {missing_count} missing values."
        )

    return True


# ============================================================
# INFINITE VALUE VALIDATION
# ============================================================

def validate_infinite_values(data):
    """
    Check whether infinite values are present.
    """

    validate_dataframe(data)

    numeric_data = data.select_dtypes(
        include=[np.number]
    )

    infinite_count = int(
        np.isinf(numeric_data.to_numpy()).sum()
    )

    if infinite_count > 0:
        raise ValueError(
            f"Input contains {infinite_count} "
            "infinite values."
        )

    return True


# ============================================================
# MODEL INPUT VALIDATION
# ============================================================

def validate_model_input(
    data,
    expected_features=EXPECTED_FEATURE_COUNT
):
    """
    Perform complete model input validation.
    """

    validate_dataframe(data)

    validate_feature_count(
        data,
        expected_features
    )

    validate_numeric_data(data)

    validate_missing_values(data)

    validate_infinite_values(data)

    return True


# ============================================================
# PROBABILITY VALIDATION
# ============================================================

def validate_probability(probability):
    """
    Validate a probability/fraud score.
    """

    if probability is None:
        raise ValueError(
            "Probability cannot be None."
        )

    try:
        probability = float(probability)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Probability must be numeric."
        ) from exc

    if not 0 <= probability <= 1:
        raise ValueError(
            "Probability must be between 0 and 1."
        )

    return probability


# ============================================================
# THRESHOLD VALIDATION
# ============================================================

def validate_threshold(threshold):
    """
    Validate fraud classification threshold.
    """

    threshold = validate_probability(threshold)

    if threshold <= 0 or threshold >= 1:
        raise ValueError(
            "Threshold must be greater than 0 "
            "and less than 1."
        )

    return threshold


# ============================================================
# RISK LEVEL VALIDATION
# ============================================================

def validate_risk_level(risk_level):
    """
    Validate a generated risk level.
    """

    if risk_level is None:
        raise ValueError(
            "Risk level cannot be None."
        )

    normalized = str(
        risk_level
    ).strip().upper()

    if normalized not in ALLOWED_RISK_LEVELS:
        raise ValueError(
            f"Invalid risk level: {risk_level}. "
            f"Allowed values: "
            f"{sorted(ALLOWED_RISK_LEVELS)}"
        )

    return normalized


# ============================================================
# FILE VALIDATION
# ============================================================

def validate_file_exists(file_path):
    """
    Validate that a file exists.
    """

    if file_path is None:
        raise ValueError(
            "File path cannot be None."
        )

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Path is not a file: {path}"
        )

    return True


# ============================================================
# PREDICTION RESULT VALIDATION
# ============================================================

def validate_prediction(
    prediction,
    probability=None
):
    """
    Validate prediction output.
    """

    if prediction not in [0, 1]:
        raise ValueError(
            "Prediction must be either 0 or 1."
        )

    if probability is not None:
        probability = validate_probability(
            probability
        )

    return True


# ============================================================
# TRANSACTION VALIDATION
# ============================================================

def validate_transaction(
    transaction,
    expected_features=EXPECTED_FEATURE_COUNT
):
    """
    Validate a single transaction.
    """

    if isinstance(transaction, dict):
        transaction = pd.DataFrame(
            [transaction]
        )

    elif isinstance(transaction, pd.Series):
        transaction = transaction.to_frame().T

    elif not isinstance(transaction, pd.DataFrame):
        raise TypeError(
            "Transaction must be a dictionary, "
            "Series, or DataFrame."
        )

    if transaction.shape[0] != 1:
        raise ValueError(
            "Transaction validator expects "
            "exactly one transaction."
        )

    validate_model_input(
        transaction,
        expected_features
    )

    return True


# ============================================================
# VALIDATION STATUS
# ============================================================

def validation_status():
    """
    Return validator configuration.
    """

    return {
        "status": "Ready",
        "expected_features": EXPECTED_FEATURE_COUNT,
        "allowed_risk_levels": sorted(
            ALLOWED_RISK_LEVELS
        )
    }