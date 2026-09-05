"""
FinGuard AI
------------
Central application configuration.

This file keeps project paths, model locations, UI settings, risk thresholds,
and runtime options in one place so app.py and other modules can use the same
configuration consistently.
"""

from __future__ import annotations

import os
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "FinGuard AI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-powered financial fraud detection and risk assessment."

HOST = os.getenv("FINGUARD_HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

SECRET_KEY = os.getenv(
    "FINGUARD_SECRET_KEY",
    "finguard-ai-development-key",
)


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

DATASET_DIR = BASE_DIR / "Dataset"
RAW_DATA_DIR = DATASET_DIR / "Raw"
PROCESSED_DATA_DIR = DATASET_DIR / "Processed"
SAMPLE_DATA_DIR = DATASET_DIR / "Sample"

MODELS_DIR = BASE_DIR / "Models"
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
CSS_DIR = STATIC_DIR / "css"
JS_DIR = STATIC_DIR / "js"
ICONS_DIR = STATIC_DIR / "icons"
IMAGES_DIR = STATIC_DIR / "images"
ASSETS_DIR = STATIC_DIR / "assets"


# ============================================================
# MODEL DIRECTORIES
# ============================================================

FRAUD_MODEL_DIR = MODELS_DIR / "fraud_model"
ANOMALY_MODEL_DIR = MODELS_DIR / "anomaly_model"
EXPLAINABILITY_DIR = MODELS_DIR / "explainability"
PREPROCESSING_DIR = MODELS_DIR / "preprocessing"


# ============================================================
# PRIMARY MODEL ARTIFACTS
# ============================================================

# Current project structure contains multiple trained artifacts.
# These are the preferred deployment artifacts.

FRAUD_MODEL_PATH = FRAUD_MODEL_DIR / "xgboost_model.pkl"
ANOMALY_MODEL_PATH = ANOMALY_MODEL_DIR / "isolation_forest.pkl"

SCALER_PATH = PREPROCESSING_DIR / "scaler.pkl"

MODEL_CONFIG_PATH = CONFIG_DIR / "model_config.json"


# ============================================================
# FALLBACK / ALTERNATIVE MODEL ARTIFACTS
# ============================================================

ALTERNATIVE_FRAUD_MODELS = [
    MODELS_DIR / "optimized_fraud_model.joblib",
    MODELS_DIR / "xgboost_model.joblib",
    MODELS_DIR / "best_fraud_model.joblib",
    MODELS_DIR / "random_forest_model.joblib",
    MODELS_DIR / "hist_gradient_boosting_model.joblib",
    MODELS_DIR / "logistic_regression_model.joblib",
]


# ============================================================
# DATASET CANDIDATES
# ============================================================

DATASET_CANDIDATES = [
    PROCESSED_DATA_DIR / "test.csv",
    PROCESSED_DATA_DIR / "validation.csv",
    PROCESSED_DATA_DIR / "train.csv",
    SAMPLE_DATA_DIR / "sample_transactions.csv",
    RAW_DATA_DIR / "creditcard.csv",
]


# ============================================================
# DEFAULT CREDIT-CARD FEATURES
# ============================================================

DEFAULT_FEATURE_NAMES = (
    ["Time"]
    + [f"V{i}" for i in range(1, 29)]
    + ["Amount"]
)


# ============================================================
# RISK ENGINE
# ============================================================

RISK_LOW_MAX = 39.99
RISK_MEDIUM_MAX = 74.99

RISK_THRESHOLDS = {
    "Low": {
        "minimum": 0.0,
        "maximum": RISK_LOW_MAX,
    },
    "Medium": {
        "minimum": 40.0,
        "maximum": RISK_MEDIUM_MAX,
    },
    "High": {
        "minimum": 75.0,
        "maximum": 100.0,
    },
}


# ============================================================
# RISK DECISIONS
# ============================================================

RISK_DECISIONS = {
    "Low": "Transaction Appears Safe",
    "Medium": "Review Required",
    "High": "Potential Fraud",
}


RISK_DESCRIPTIONS = {
    "Low": (
        "The transaction appears legitimate. No significant fraud "
        "or anomaly indicators were detected."
    ),
    "Medium": (
        "Moderate risk detected. Additional verification is recommended "
        "before approving this transaction."
    ),
    "High": (
        "High-risk transaction detected. This transaction requires "
        "immediate attention and further investigation."
    ),
}


# ============================================================
# MODEL SCORING WEIGHTS
# ============================================================

# Used when combining fraud probability and anomaly information.

FRAUD_SCORE_WEIGHT = 0.75
ANOMALY_SCORE_WEIGHT = 0.25

ANOMALY_RISK_SIGNAL = 25.0


# ============================================================
# FALLBACK SCORING
# ============================================================

# These values are only used when a compatible trained fraud model
# cannot produce a probability. They keep the UI functional and
# must not be interpreted as trained-model confidence.

FALLBACK_AMOUNT_LIMIT = 5000.0
FALLBACK_AMOUNT_WEIGHT = 45.0
FALLBACK_FEATURE_WEIGHT = 2.5
FALLBACK_FEATURE_LIMIT = 35.0
FALLBACK_MAX_SCORE = 99.0


# ============================================================
# REQUEST / SECURITY LIMITS
# ============================================================

MAX_CONTENT_LENGTH = 8 * 1024 * 1024

JSON_SORT_KEYS = False


# ============================================================
# UI / BRAND
# ============================================================

BRAND_NAME = "FinGuard AI"
BRAND_TAGLINE = "Intelligent Fraud Detection & Risk Assessment"

BRAND_COLORS = {
    "primary": "#2563eb",
    "primary_dark": "#1d4ed8",
    "navy": "#0f172a",
    "background": "#f8fafc",
    "surface": "#ffffff",
    "border": "#e2e8f0",
    "muted": "#64748b",
    "success": "#16a34a",
    "warning": "#d97706",
    "danger": "#dc2626",
}


# ============================================================
# STATIC ASSETS
# ============================================================

ASSETS = {
    "logo": "images/logo.png",
    "hero": "images/hero.png",
    "hero_background": "images/background/hero_bg.jpg",

    "shield_icon": "icons/shield.svg",
    "secure_icon": "icons/secure.svg",
    "fraud_icon": "icons/fraud.svg",
    "analytics_icon": "icons/analytics.svg",

    "fraud_detection": "assets/illustrations/fraud_detection.svg",
    "analytics_dashboard": "assets/illustrations/analytics_dashboard.svg",
    "secure_finance": "assets/illustrations/secure_finance.svg",
}


# ============================================================
# FONT ASSETS
# ============================================================

FONT_DIR = STATIC_DIR / "assets" / "fonts"

FONTS = {
    "regular": FONT_DIR / "Inter-Regular.otf",
    "medium": FONT_DIR / "Inter-Medium.otf",
    "semibold": FONT_DIR / "Inter-SemiBold.otf",
    "bold": FONT_DIR / "Inter-Bold.otf",
}


# ============================================================
# LOGGING
# ============================================================

LOG_FILE = LOGS_DIR / "finguard.log"

LOG_LEVEL = os.getenv("FINGUARD_LOG_LEVEL", "INFO")


# ============================================================
# API
# ============================================================

API_PREFIX = "/api"

API_ENDPOINTS = {
    "health": f"{API_PREFIX}/health",
    "metrics": f"{API_PREFIX}/metrics",
    "predict": f"{API_PREFIX}/predict",
}


# ============================================================
# APPLICATION META
# ============================================================

DEVELOPER_NAME = "Mohammed Viqar Hyder"

COPYRIGHT_TEXT = "FinGuard AI. All rights reserved."


# ============================================================
# DIRECTORY INITIALIZATION
# ============================================================

REQUIRED_DIRECTORIES = [
    LOGS_DIR,
    DATASET_DIR,
    MODELS_DIR,
    CONFIG_DIR,
    TEMPLATES_DIR,
    STATIC_DIR,
]


def ensure_directories() -> None:
    """Create required runtime directories when they do not exist."""
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def asset_path(relative_path: str) -> Path:
    """Return an absolute path inside the static directory."""
    return STATIC_DIR / relative_path


def model_exists(path: Path) -> bool:
    """Return True when a model artifact exists."""
    return path.is_file()


def get_available_fraud_model() -> Path | None:
    """
    Return the first available fraud model.

    The preferred XGBoost artifact is checked first, followed by the
    alternative trained artifacts already present in the project.
    """
    candidates = [FRAUD_MODEL_PATH, *ALTERNATIVE_FRAUD_MODELS]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    return None


def get_model_status() -> dict[str, bool]:
    """Return deployment readiness for the main model artifacts."""
    fraud_path = get_available_fraud_model()

    return {
        "fraud_model": fraud_path is not None,
        "anomaly_model": ANOMALY_MODEL_PATH.is_file(),
        "scaler": SCALER_PATH.is_file(),
        "model_config": MODEL_CONFIG_PATH.is_file(),
    }


# Initialize safe runtime directories when imported.
ensure_directories()
