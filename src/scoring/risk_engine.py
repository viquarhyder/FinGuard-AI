"""
FinGuard AI - Risk Engine
-------------------------
Combines supervised fraud probability and anomaly
detection into a unified transaction risk score.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# RISK ENGINE CONFIGURATION
# ============================================================

FRAUD_WEIGHT = 0.70
ANOMALY_WEIGHT = 0.30

FRAUD_THRESHOLD = 0.82


# Risk score boundaries
LOW_RISK_MAX = 30.0
MEDIUM_RISK_MAX = 70.0


# ============================================================
# VALIDATION
# ============================================================

def validate_weights():
    """
    Validate fraud and anomaly weights.
    """

    total_weight = FRAUD_WEIGHT + ANOMALY_WEIGHT

    if not np.isclose(total_weight, 1.0):
        raise ValueError(
            f"Risk weights must sum to 1.0. "
            f"Current total: {total_weight}"
        )


def validate_fraud_threshold(threshold):
    """
    Validate fraud decision threshold.
    """

    threshold = float(threshold)

    if not 0 < threshold < 1:
        raise ValueError(
            f"Invalid fraud threshold: {threshold}"
        )

    return threshold


# ============================================================
# RISK SCORE CALCULATION
# ============================================================

def calculate_risk_score(
    fraud_probability,
    anomaly_score,
    fraud_weight=FRAUD_WEIGHT,
    anomaly_weight=ANOMALY_WEIGHT
):
    """
    Calculate combined transaction risk score.

    Parameters
    ----------
    fraud_probability : float
        Fraud probability between 0 and 1.

    anomaly_score : float
        Anomaly indicator between 0 and 1.

    fraud_weight : float
        Weight assigned to fraud probability.

    anomaly_weight : float
        Weight assigned to anomaly score.

    Returns
    -------
    float
        Risk score between 0 and 100.
    """

    fraud_probability = np.clip(
        float(fraud_probability), 0.0, 1.0
    )

    anomaly_score = np.clip(
        float(anomaly_score), 0.0, 1.0
    )

    total_weight = fraud_weight + anomaly_weight

    if not np.isclose(total_weight, 1.0):
        raise ValueError(
            "Fraud and anomaly weights must sum to 1.0."
        )

    combined_score = (
        fraud_probability * fraud_weight
        + anomaly_score * anomaly_weight
    )

    return float(combined_score * 100)


# ============================================================
# RISK LEVEL
# ============================================================

def classify_risk(risk_score):
    """
    Convert numerical risk score into risk category.
    """

    risk_score = float(risk_score)

    if risk_score < 0 or risk_score > 100:
        raise ValueError(
            f"Risk score must be between 0 and 100. "
            f"Received: {risk_score}"
        )

    if risk_score <= LOW_RISK_MAX:
        return "Low"

    if risk_score <= MEDIUM_RISK_MAX:
        return "Medium"

    return "High"


# ============================================================
# TRANSACTION RISK ASSESSMENT
# ============================================================

def assess_transaction_risk(
    fraud_probability,
    anomaly_score,
    fraud_threshold=FRAUD_THRESHOLD
):
    """
    Generate complete risk assessment for one transaction.
    """

    validate_weights()

    fraud_threshold = validate_fraud_threshold(
        fraud_threshold
    )

    risk_score = calculate_risk_score(
        fraud_probability=fraud_probability,
        anomaly_score=anomaly_score
    )

    risk_level = classify_risk(risk_score)

    fraud_probability = float(fraud_probability)

    fraud_prediction = int(
        fraud_probability >= fraud_threshold
    )

    anomaly_flag = int(
        float(anomaly_score) >= 0.50
    )

    return {
        "fraud_probability": fraud_probability,
        "fraud_prediction": fraud_prediction,
        "anomaly_score": float(anomaly_score),
        "anomaly_flag": anomaly_flag,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "fraud_weight": FRAUD_WEIGHT,
        "anomaly_weight": ANOMALY_WEIGHT,
        "fraud_threshold": fraud_threshold
    }


# ============================================================
# BATCH RISK ASSESSMENT
# ============================================================

def generate_risk_report(
    fraud_probabilities,
    anomaly_scores,
    fraud_threshold=FRAUD_THRESHOLD
):
    """
    Generate risk assessment for multiple transactions.
    """

    fraud_probabilities = np.asarray(
        fraud_probabilities,
        dtype=float
    )

    anomaly_scores = np.asarray(
        anomaly_scores,
        dtype=float
    )

    if len(fraud_probabilities) != len(anomaly_scores):
        raise ValueError(
            "Fraud probabilities and anomaly scores "
            "must have the same length."
        )

    risk_scores = (
        fraud_probabilities * FRAUD_WEIGHT
        + anomaly_scores * ANOMALY_WEIGHT
    ) * 100

    fraud_predictions = (
        fraud_probabilities >= fraud_threshold
    ).astype(int)

    anomaly_flags = (
        anomaly_scores >= 0.50
    ).astype(int)

    risk_levels = [
        classify_risk(score)
        for score in risk_scores
    ]

    report = pd.DataFrame({
        "fraud_probability": fraud_probabilities,
        "fraud_prediction": fraud_predictions,
        "anomaly_score": anomaly_scores,
        "anomaly_flag": anomaly_flags,
        "risk_score": risk_scores,
        "risk_level": risk_levels
    })

    return report


# ============================================================
# RISK SUMMARY
# ============================================================

def get_risk_summary(risk_report):
    """
    Generate summary statistics from a risk report.
    """

    if not isinstance(risk_report, pd.DataFrame):
        raise TypeError(
            "risk_report must be a pandas DataFrame."
        )

    if "risk_level" not in risk_report.columns:
        raise ValueError(
            "risk_report must contain 'risk_level'."
        )

    high_risk = int(
        (risk_report["risk_level"] == "High").sum()
    )

    medium_risk = int(
        (risk_report["risk_level"] == "Medium").sum()
    )

    low_risk = int(
        (risk_report["risk_level"] == "Low").sum()
    )

    return {
        "total_transactions": len(risk_report),
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "mean_risk_score": float(
            risk_report["risk_score"].mean()
        )
    }


# ============================================================
# SINGLE TRANSACTION HELPER
# ============================================================

def get_risk_label(risk_score):
    """
    Return only the risk category for a score.
    """

    return classify_risk(risk_score)