"""
FinGuard AI API Schemas
-----------------------
Lightweight request/response validation helpers.

No additional validation package is required. These helpers keep the API
contract explicit while remaining compatible with the existing Flask app.
"""

from __future__ import annotations

import math
from typing import Any


# ============================================================
# FEATURE CONTRACT
# ============================================================

DEFAULT_FEATURE_NAMES = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount"]
)


# ============================================================
# BASIC HELPERS
# ============================================================

def is_finite_number(value: Any) -> bool:
    """Return True when value can be represented as a finite float."""
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def normalize_number(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to a finite float."""
    if not is_finite_number(value):
        return default

    return float(value)


# ============================================================
# TRANSACTION REQUEST
# ============================================================

def validate_transaction_payload(
    payload: Any,
    feature_names: list[str] | tuple[str, ...] | None = None,
) -> tuple[bool, str | None, dict[str, float]]:
    """
    Validate and normalize a transaction JSON payload.

    Missing model features are filled with 0.0 so the API remains compatible
    with the defensive inference layer in app.py.
    """

    if not isinstance(payload, dict):
        return False, "Transaction payload must be a JSON object.", {}

    if not payload:
        return False, "Transaction payload cannot be empty.", {}

    names = list(feature_names or DEFAULT_FEATURE_NAMES)

    normalized: dict[str, float] = {}

    # Accept exact feature names first and case-insensitive names second.
    lowered = {
        str(key).strip().lower(): value
        for key, value in payload.items()
    }

    for feature in names:
        if feature in payload:
            raw_value = payload[feature]
        else:
            raw_value = lowered.get(feature.lower(), 0.0)

        if raw_value in (None, ""):
            normalized[feature] = 0.0
            continue

        if not is_finite_number(raw_value):
            return (
                False,
                f"Feature '{feature}' must contain a valid numeric value.",
                {},
            )

        normalized[feature] = normalize_number(raw_value)

    # Amount should never be negative.
    if "Amount" in normalized and normalized["Amount"] < 0:
        return (
            False,
            "Amount cannot be negative.",
            {},
        )

    return True, None, normalized


# ============================================================
# API REQUEST SCHEMA
# ============================================================

def transaction_request_schema(
    feature_names: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Return a machine-readable description of the prediction request."""

    names = list(feature_names or DEFAULT_FEATURE_NAMES)

    properties = {
        name: {
            "type": "number",
            "description": f"Transaction feature: {name}",
        }
        for name in names
    }

    return {
        "type": "object",
        "properties": properties,
        "additionalProperties": True,
    }


# ============================================================
# PREDICTION RESPONSE SCHEMA
# ============================================================

def prediction_response_schema() -> dict[str, Any]:
    """Return the documented structure of a prediction response."""

    return {
        "success": True,
        "result": {
            "fraud_probability": 0.0,
            "fraud_prediction": 0,
            "anomaly_prediction": 1,
            "risk_score": 0.0,
            "risk_level": "Low",
            "risk_class": "low",
            "decision": "Transaction Appears Safe",
            "amount": 0.0,
            "model_available": True,
            "anomaly_available": True,
        },
    }


# ============================================================
# RESPONSE SANITIZATION
# ============================================================

def sanitize_prediction_result(result: dict[str, Any]) -> dict[str, Any]:
    """
    Convert NumPy/scikit-learn scalar values into JSON-safe Python values.

    This prevents jsonify failures when model outputs contain NumPy types.
    """

    if not isinstance(result, dict):
        return {}

    cleaned: dict[str, Any] = {}

    for key, value in result.items():

        if hasattr(value, "item"):
            try:
                value = value.item()
            except Exception:
                pass

        if isinstance(value, float):
            if not math.isfinite(value):
                value = 0.0

        cleaned[str(key)] = value

    return cleaned


# ============================================================
# HEALTH RESPONSE
# ============================================================

def health_response_schema() -> dict[str, Any]:
    """Return the documented health response structure."""

    return {
        "success": True,
        "status": "healthy",
        "service": "FinGuard AI API",
        "version": "1.0.0",
        "timestamp": "ISO-8601 timestamp",
        "models": {
            "fraud_model": True,
            "anomaly_model": True,
            "scaler": True,
        },
    }


# ============================================================
# METRICS RESPONSE
# ============================================================

def metrics_response_schema() -> dict[str, Any]:
    """Return the documented dashboard metrics structure."""

    return {
        "success": True,
        "data": {
            "total_transactions": 0,
            "fraud_transactions": 0,
            "legitimate_transactions": 0,
            "fraud_rate": 0.0,
            "total_amount": 0.0,
            "average_amount": 0.0,
            "risk_score": 0.0,
            "chart_labels": [],
            "chart_values": [],
            "recent_transactions": [],
            "model_ready": False,
            "anomaly_ready": False,
            "last_updated": "ISO-8601/display timestamp",
        },
    }


# ============================================================
# API ERROR SCHEMA
# ============================================================

def error_response_schema() -> dict[str, Any]:
    """Return the documented API error structure."""

    return {
        "success": False,
        "error": "Human-readable error message",
        "timestamp": "ISO-8601 timestamp",
    }
