"""
FinGuard AI - Feature Engineering
----------------------------------
Reusable feature-engineering utilities for transaction data.

IMPORTANT:
The feature formulas in this module reproduce the feature
engineering logic used during model training.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "Models"
METADATA_PATH = MODELS_DIR / "feature_engineering_metadata.joblib"


# ============================================================
# ORIGINAL DATA COLUMNS
# ============================================================

V_COLUMNS = [
    f"V{i}"
    for i in range(1, 29)
]


# ============================================================
# LOAD / SAVE FEATURE METADATA
# ============================================================

def load_feature_metadata():
    """
    Load feature-engineering metadata generated during training.
    """

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Feature engineering metadata not found: {METADATA_PATH}"
        )

    return joblib.load(METADATA_PATH)


def save_feature_metadata(
    metadata,
    filename="feature_engineering_metadata.joblib"
):
    """
    Save feature-engineering metadata.
    """

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    path = MODELS_DIR / filename

    joblib.dump(
        metadata,
        path
    )

    return path


# ============================================================
# SOURCE COLUMN PREPARATION
# ============================================================

def _prepare_original_columns(df):
    """
    Prepare the temporary original columns used by the
    training feature-engineering functions.

    Training notebook used:
        _Amount_Original
        _Time_Original

    Application input normally contains:
        Amount
        Time
    """

    result = df.copy()

    # --------------------------------------------------------
    # Amount
    # --------------------------------------------------------

    if "_Amount_Original" not in result.columns:

        if "Amount" not in result.columns:
            raise ValueError(
                "Input data must contain either "
                "'Amount' or '_Amount_Original'."
            )

        result["_Amount_Original"] = result["Amount"]

    # --------------------------------------------------------
    # Time
    # --------------------------------------------------------

    if "_Time_Original" not in result.columns:

        if "Time" not in result.columns:
            raise ValueError(
                "Input data must contain either "
                "'Time' or '_Time_Original'."
            )

        result["_Time_Original"] = result["Time"]

    return result


# ============================================================
# TRANSACTION AMOUNT FEATURES
# ============================================================

def add_amount_features(df):
    """
    Reproduce the amount feature engineering used during training.

    Creates:

        Amount_Log1p
        Amount_Sqrt
        Amount_Squared
        Amount_Is_Zero
        Amount_Is_High
    """

    result = df.copy()

    if "_Amount_Original" not in result.columns:

        if "Amount" not in result.columns:
            raise ValueError(
                "Amount column is required."
            )

        result["_Amount_Original"] = result["Amount"]

    amount = result["_Amount_Original"].clip(
        lower=0
    )

    result["Amount_Log1p"] = np.log1p(
        amount
    )

    result["Amount_Sqrt"] = np.sqrt(
        amount
    )

    result["Amount_Squared"] = (
        amount ** 2
    )

    result["Amount_Is_Zero"] = (
        amount == 0
    ).astype("int8")

    # Exact training logic:
    # high threshold = 95th percentile of amount
    high_threshold = amount.quantile(
        0.95
    )

    result["Amount_Is_High"] = (
        amount >= high_threshold
    ).astype("int8")

    return result


# ============================================================
# TEMPORAL FEATURES
# ============================================================

SECONDS_PER_DAY = 24 * 60 * 60
SECONDS_PER_HOUR = 60 * 60
SECONDS_PER_MINUTE = 60


def add_temporal_features(df):
    """
    Reproduce the temporal feature engineering used during training.

    Creates:

        Time_Day_Index
        Time_Hour
        Time_Minute
        Time_Hour_Sin
        Time_Hour_Cos
        Time_Day_Sin
        Time_Day_Cos
    """

    result = df.copy()

    if "_Time_Original" not in result.columns:

        if "Time" not in result.columns:
            raise ValueError(
                "Time column is required."
            )

        result["_Time_Original"] = result["Time"]

    time_value = result["_Time_Original"].clip(
        lower=0
    )

    # --------------------------------------------------------
    # Day index
    # --------------------------------------------------------

    result["Time_Day_Index"] = (
        np.floor(
            time_value / SECONDS_PER_DAY
        )
        .astype("int32")
    )

    # --------------------------------------------------------
    # Time within day
    # --------------------------------------------------------

    seconds_in_day = (
        time_value % SECONDS_PER_DAY
    )

    hour = np.floor(
        seconds_in_day / SECONDS_PER_HOUR
    )

    minute = np.floor(
        (
            seconds_in_day
            % SECONDS_PER_HOUR
        )
        / SECONDS_PER_MINUTE
    )

    result["Time_Hour"] = (
        hour.astype("int8")
    )

    result["Time_Minute"] = (
        minute.astype("int8")
    )

    # --------------------------------------------------------
    # Cyclic hour encoding
    # --------------------------------------------------------

    result["Time_Hour_Sin"] = np.sin(
        2 * np.pi * hour / 24
    )

    result["Time_Hour_Cos"] = np.cos(
        2 * np.pi * hour / 24
    )

    # --------------------------------------------------------
    # Cyclic day encoding
    # --------------------------------------------------------

    result["Time_Day_Sin"] = np.sin(
        2 * np.pi
        * seconds_in_day
        / SECONDS_PER_DAY
    )

    result["Time_Day_Cos"] = np.cos(
        2 * np.pi
        * seconds_in_day
        / SECONDS_PER_DAY
    )

    return result


# ============================================================
# V1-V28 STATISTICAL FEATURES
# ============================================================

def add_v_statistical_features(df):
    """
    Reproduce the V1-V28 statistical feature engineering
    used during training.

    Creates:

        V_Abs_Mean
        V_Abs_Max
        V_Abs_Std
        V_L2_Norm
        V_Positive_Count
        V_Negative_Count
        V_Extreme_Count
    """

    result = df.copy()

    missing_v = [
        column
        for column in V_COLUMNS
        if column not in result.columns
    ]

    if missing_v:
        raise ValueError(
            f"Missing V features: {missing_v}"
        )

    v = result[V_COLUMNS]

    result["V_Abs_Mean"] = (
        v.abs().mean(axis=1)
    )

    result["V_Abs_Max"] = (
        v.abs().max(axis=1)
    )

    result["V_Abs_Std"] = (
        v.abs()
        .std(axis=1)
        .fillna(0)
    )

    result["V_L2_Norm"] = np.sqrt(
        (v ** 2).sum(axis=1)
    )

    result["V_Positive_Count"] = (
        (v > 0)
        .sum(axis=1)
        .astype("int8")
    )

    result["V_Negative_Count"] = (
        (v < 0)
        .sum(axis=1)
        .astype("int8")
    )

    result["V_Extreme_Count"] = (
        (v.abs() > 3)
        .sum(axis=1)
        .astype("int8")
    )

    return result


# ============================================================
# RISK-ORIENTED FEATURES
# ============================================================

def add_risk_features(df):
    """
    Reproduce the risk-oriented behavioral features
    used during training.

    Creates:

        Risk_Deviation_Score
        Risk_Max_Deviation
        Risk_Extreme_Ratio
        Risk_Severe_Ratio
    """

    result = df.copy()

    missing_v = [
        column
        for column in V_COLUMNS
        if column not in result.columns
    ]

    if missing_v:
        raise ValueError(
            f"Missing V features: {missing_v}"
        )

    v = result[V_COLUMNS]

    result["Risk_Deviation_Score"] = (
        v.abs().mean(axis=1)
    )

    result["Risk_Max_Deviation"] = (
        v.abs().max(axis=1)
    )

    result["Risk_Extreme_Ratio"] = (
        (v.abs() > 3)
        .mean(axis=1)
    )

    result["Risk_Severe_Ratio"] = (
        (v.abs() > 5)
        .mean(axis=1)
    )

    return result


# ============================================================
# COMPLETE FEATURE ENGINEERING
# ============================================================

def add_transaction_features(data):
    """
    Apply the complete feature-engineering pipeline.

    Raw input:
        30 original features

    Generated:
        23 engineered features

    Final:
        53 model features
    """

    if not isinstance(
        data,
        pd.DataFrame
    ):
        raise TypeError(
            "data must be a pandas DataFrame."
        )

    result = data.copy()

    # Prepare temporary original columns
    result = _prepare_original_columns(
        result
    )

    # --------------------------------------------------------
    # 1. Amount features
    # --------------------------------------------------------

    result = add_amount_features(
        result
    )

    # --------------------------------------------------------
    # 2. Temporal features
    # --------------------------------------------------------

    result = add_temporal_features(
        result
    )

    # --------------------------------------------------------
    # 3. V statistical features
    # --------------------------------------------------------

    result = add_v_statistical_features(
        result
    )

    # --------------------------------------------------------
    # 4. Risk features
    # --------------------------------------------------------

    result = add_risk_features(
        result
    )

    # Remove temporary training-only columns
    result = result.drop(
        columns=[
            "_Amount_Original",
            "_Time_Original"
        ],
        errors="ignore"
    )

    return result


# ============================================================
# MODEL FEATURE SELECTION
# ============================================================

def select_model_features(
    data,
    feature_names
):
    """
    Select features in the exact order expected by the model.
    """

    if not isinstance(
        data,
        pd.DataFrame
    ):
        raise TypeError(
            "data must be a pandas DataFrame."
        )

    missing_features = [
        feature
        for feature in feature_names
        if feature not in data.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing model features: "
            f"{missing_features}"
        )

    return data[
        feature_names
    ].copy()


# ============================================================
# FEATURE NAME UTILITY
# ============================================================

def get_feature_names(
    data,
    target_column=None
):
    """
    Return feature names used for model input.
    """

    if not isinstance(
        data,
        pd.DataFrame
    ):
        raise TypeError(
            "data must be a pandas DataFrame."
        )

    features = data.copy()

    if (
        target_column is not None
        and target_column in features.columns
    ):
        features = features.drop(
            columns=[target_column]
        )

    return list(
        features.columns
    )