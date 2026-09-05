"""
FinGuard AI API Routes
----------------------
JSON API endpoints for health checks, dashboard metrics and transaction
prediction.

The blueprint intentionally uses Flask's application context rather than
importing app.py directly. This avoids circular imports and keeps the API
layer modular.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from flask import Blueprint, current_app, jsonify, request


api_bp = Blueprint("api", __name__, url_prefix="/api")


def _service() -> dict[str, Any]:
    """
    Return services registered by app.py.

    app.py should register:
        current_app.extensions["finguard"] = {
            "predict_transaction": predict_transaction,
            "dashboard_metrics": dashboard_metrics,
            "model_status": ...
        }
    """
    return current_app.extensions.get("finguard", {})


def _error(message: str, status_code: int = 400):
    return jsonify(
        {
            "success": False,
            "error": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    ), status_code


# ============================================================
# HEALTH
# ============================================================

@api_bp.get("/health")
def health():
    """Return API and model-service health information."""

    services = _service()

    model_status = services.get("model_status")

    if callable(model_status):
        try:
            models = model_status()
        except Exception:
            models = {}
    elif isinstance(model_status, dict):
        models = model_status
    else:
        models = {
            "fraud_model": False,
            "anomaly_model": False,
            "scaler": False,
        }

    return jsonify(
        {
            "success": True,
            "status": "healthy",
            "service": "FinGuard AI API",
            "version": current_app.config.get("APP_VERSION", "1.0.0"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "models": models,
        }
    )


# ============================================================
# METRICS
# ============================================================

@api_bp.get("/metrics")
def metrics():
    """Return dashboard metrics as JSON."""

    services = _service()
    metrics_function = services.get("dashboard_metrics")

    if not callable(metrics_function):
        return _error(
            "Dashboard metrics service is not available.",
            503,
        )

    try:
        data = metrics_function()

        if not isinstance(data, dict):
            return _error(
                "Dashboard metrics service returned an invalid response.",
                500,
            )

        return jsonify(
            {
                "success": True,
                "data": data,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except Exception:
        current_app.logger.exception("API metrics request failed.")
        return _error(
            "Unable to load dashboard metrics.",
            500,
        )


# ============================================================
# PREDICTION
# ============================================================

@api_bp.post("/predict")
def predict():
    """
    Analyze a transaction.

    Expected JSON:
        {
            "Time": 12345,
            "V1": 0.1,
            ...
            "V28": -0.2,
            "Amount": 250.50
        }
    """

    if not request.is_json:
        return _error(
            "JSON request body is required.",
            415,
        )

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return _error(
            "Request body must contain a JSON object.",
            400,
        )

    if not payload:
        return _error(
            "Transaction data cannot be empty.",
            400,
        )

    services = _service()
    predict_function = services.get("predict_transaction")

    if not callable(predict_function):
        return _error(
            "Prediction service is not available.",
            503,
        )

    try:
        result = predict_function(payload)

        if not isinstance(result, dict):
            return _error(
                "Prediction service returned an invalid response.",
                500,
            )

        return jsonify(
            {
                "success": True,
                "result": result,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except ValueError as exc:
        current_app.logger.warning(
            "Invalid prediction input: %s",
            exc,
        )
        return _error(
            "Invalid transaction values.",
            422,
        )

    except Exception:
        current_app.logger.exception(
            "API prediction request failed."
        )
        return _error(
            "Prediction service could not process the transaction.",
            500,
        )


# ============================================================
# MODEL STATUS
# ============================================================

@api_bp.get("/models")
def models():
    """Return the current availability of deployed model artifacts."""

    services = _service()
    model_status = services.get("model_status")

    try:
        if callable(model_status):
            status = model_status()
        elif isinstance(model_status, dict):
            status = model_status
        else:
            status = {}

        return jsonify(
            {
                "success": True,
                "models": status,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

    except Exception:
        current_app.logger.exception(
            "API model-status request failed."
        )
        return _error(
            "Unable to determine model status.",
            500,
        )


# ============================================================
# API ROOT
# ============================================================

@api_bp.get("/")
def api_index():
    """Return a small API discovery response."""

    return jsonify(
        {
            "success": True,
            "service": "FinGuard AI API",
            "version": current_app.config.get("APP_VERSION", "1.0.0"),
            "endpoints": {
                "health": "/api/health",
                "metrics": "/api/metrics",
                "predict": "/api/predict",
                "models": "/api/models",
            },
        }
    )
