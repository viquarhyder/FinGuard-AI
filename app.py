# ============================================================
# FinGuard AI
# Intelligent Financial Fraud Detection & Risk Intelligence
# Main Flask Application
# ============================================================

from __future__ import annotations

import os
import json
import logging
from pathlib import Path
from datetime import datetime

import joblib
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)


# ============================================================
# APPLICATION PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

DATASET_DIR = BASE_DIR / "Dataset"
PROCESSED_DIR = DATASET_DIR / "Processed"

MODEL_DIR = BASE_DIR / "Models"
CONFIG_DIR = BASE_DIR / "config"
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
)

app.config.update(
    SECRET_KEY=os.environ.get(
        "FINGUARD_SECRET_KEY",
        "finguard-ai-development-secret",
    ),
    JSON_SORT_KEYS=False,
    SEND_FILE_MAX_AGE_DEFAULT=0,
)


# ============================================================
# LOGGING
# ============================================================

LOG_FILE = LOG_DIR / "finguard.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("FinGuardAI")


# ============================================================
# GLOBAL APPLICATION STATE
# ============================================================

APP_STATE = {
    "fraud_model": None,
    "fraud_model_path": None,

    "anomaly_model": None,
    "anomaly_model_path": None,

    "feature_metadata": None,
    "training_metadata": None,
    "preprocessing_metadata": None,
    "risk_metadata": None,

    "fraud_threshold": 0.50,

    "dataset": None,
    "dataset_path": None,

    "models_loaded": False,

    "last_prediction": None,
}


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_CANDIDATES = {

    "fraud": [
        MODEL_DIR / "optimized_fraud_model.joblib",
        MODEL_DIR / "best_fraud_model.joblib",
        MODEL_DIR / "xgboost_model.joblib",
        MODEL_DIR / "random_forest_model.joblib",
        MODEL_DIR / "hist_gradient_boosting_model.joblib",
        MODEL_DIR / "logistic_regression_model.joblib",
    ],

    "anomaly": [
        MODEL_DIR / "anomaly_model" / "isolation_forest.pkl",
        MODEL_DIR / "anomaly_model" / "isolation_forest.joblib",
    ],

    "feature_metadata": [
        MODEL_DIR / "feature_engineering_metadata.joblib",
        MODEL_DIR / "final_model_metadata.joblib",
    ],

    "training_metadata": [
        MODEL_DIR / "model_training_metadata.joblib",
    ],

    "preprocessing_metadata": [
        MODEL_DIR / "preprocessing_metadata.joblib",
    ],

    "risk_metadata": [
        MODEL_DIR / "risk_engine_metadata.joblib",
    ],

    "threshold": [
        MODEL_DIR / "fraud_threshold_metadata.joblib",
    ],
}


# ============================================================
# DATASET
# ============================================================

PRIMARY_DATASET = (
    PROCESSED_DIR / "feature_engineered_test.csv"
)


# ============================================================
# DATASET DISCOVERY
# ============================================================

def discover_dataset():

    candidates = [

        PROCESSED_DIR / "feature_engineered_test.csv",

        PROCESSED_DIR / "test_processed.csv",

        PROCESSED_DIR / "feature_engineered_train.csv",

        DATASET_DIR / "anomaly_output.csv",

        DATASET_DIR / "fraud_dataset.csv",

        DATASET_DIR / "creditcard.csv",

        DATASET_DIR / "transactions.csv",

        DATASET_DIR / "transaction_data.csv",

    ]

    for path in candidates:

        if path.exists() and path.is_file():
            return path


    if PROCESSED_DIR.exists():

        csv_files = sorted(
            PROCESSED_DIR.glob("*.csv")
        )

        if csv_files:
            return csv_files[0]


    if DATASET_DIR.exists():

        csv_files = sorted(
            DATASET_DIR.glob("*.csv")
        )

        if csv_files:
            return csv_files[0]


    return None


# ============================================================
# MODEL LOADING
# ============================================================

def load_first_model(paths, model_name):

    for path in paths:

        if not path.exists():
            continue

        try:

            logger.info(
                "Loading %s model: %s",
                model_name,
                path,
            )

            model = joblib.load(path)

            logger.info(
                "%s model loaded successfully.",
                model_name.capitalize(),
            )

            return model, path

        except Exception as exc:

            logger.exception(
                "Unable to load %s model from %s: %s",
                model_name,
                path,
                exc,
            )

    logger.warning(
        "No usable %s model found.",
        model_name,
    )

    return None, None


# ============================================================
# METADATA LOADING
# ============================================================

def load_metadata(paths, metadata_name):

    for path in paths:

        if not path.exists():
            continue

        try:

            metadata = joblib.load(path)

            logger.info(
                "%s loaded from %s",
                metadata_name,
                path,
            )

            return metadata

        except Exception as exc:

            logger.warning(
                "Could not load %s: %s",
                metadata_name,
                exc,
            )

    return None


# ============================================================
# JSON CONFIG
# ============================================================

def load_json_config():

    config_path = (
        CONFIG_DIR / "model_config.json"
    )

    if not config_path.exists():
        return {}

    try:

        with open(
            config_path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except Exception as exc:

        logger.warning(
            "Could not load model_config.json: %s",
            exc,
        )

        return {}


# ============================================================
# DATASET LOADING
# ============================================================

def load_dataset():

    dataset_path = discover_dataset()

    if dataset_path is None:

        logger.warning(
            "No CSV dataset found inside Dataset/."
        )

        APP_STATE["dataset"] = pd.DataFrame()
        APP_STATE["dataset_path"] = None

        return pd.DataFrame()

    try:

        logger.info(
            "Loading dashboard dataset: %s",
            dataset_path,
        )

        df = pd.read_csv(dataset_path)

        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        APP_STATE["dataset_path"] = dataset_path
        APP_STATE["dataset"] = df

        logger.info(
            "Dataset loaded successfully | file=%s | rows=%s | columns=%s",
            dataset_path.name,
            len(df),
            len(df.columns),
        )

        logger.info(
            "Dataset columns: %s",
            list(df.columns),
        )

        return df

    except Exception as exc:

        logger.exception(
            "Dataset loading failed: %s",
            exc,
        )

        APP_STATE["dataset"] = pd.DataFrame()
        APP_STATE["dataset_path"] = None

        return pd.DataFrame()


# ============================================================
# APPLICATION INITIALIZATION
# ============================================================

def initialize_system():

    logger.info("=" * 70)
    logger.info("Initializing FinGuard AI")
    logger.info("=" * 70)


    # --------------------------------------------------------
    # FRAUD MODEL
    # --------------------------------------------------------

    fraud_model, fraud_path = load_first_model(
        MODEL_CANDIDATES["fraud"],
        "fraud",
    )

    APP_STATE["fraud_model"] = fraud_model
    APP_STATE["fraud_model_path"] = fraud_path


    # --------------------------------------------------------
    # ANOMALY MODEL
    # --------------------------------------------------------

    anomaly_model, anomaly_path = load_first_model(
        MODEL_CANDIDATES["anomaly"],
        "anomaly",
    )

    APP_STATE["anomaly_model"] = anomaly_model
    APP_STATE["anomaly_model_path"] = anomaly_path


    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    APP_STATE["feature_metadata"] = load_metadata(
        MODEL_CANDIDATES["feature_metadata"],
        "Feature metadata",
    )

    APP_STATE["training_metadata"] = load_metadata(
        MODEL_CANDIDATES["training_metadata"],
        "Training metadata",
    )

    APP_STATE["preprocessing_metadata"] = load_metadata(
        MODEL_CANDIDATES["preprocessing_metadata"],
        "Preprocessing metadata",
    )

    APP_STATE["risk_metadata"] = load_metadata(
        MODEL_CANDIDATES["risk_metadata"],
        "Risk metadata",
    )


    # --------------------------------------------------------
    # THRESHOLD
    # --------------------------------------------------------

    threshold_metadata = load_metadata(
        MODEL_CANDIDATES["threshold"],
        "Fraud threshold metadata",
    )

    if threshold_metadata is not None:

        try:

            if isinstance(
                threshold_metadata,
                dict,
            ):

                for key in [
                    "threshold",
                    "fraud_threshold",
                    "optimal_threshold",
                ]:

                    if key in threshold_metadata:

                        APP_STATE[
                            "fraud_threshold"
                        ] = float(
                            threshold_metadata[key]
                        )

                        break

            elif isinstance(
                threshold_metadata,
                (int, float),
            ):

                APP_STATE[
                    "fraud_threshold"
                ] = float(
                    threshold_metadata
                )

        except Exception as exc:

            logger.warning(
                "Could not determine fraud threshold: %s",
                exc,
            )


    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    load_dataset()


    # --------------------------------------------------------
    # MODEL STATUS
    # --------------------------------------------------------

    APP_STATE["models_loaded"] = (
        APP_STATE["fraud_model"] is not None
        or APP_STATE["anomaly_model"] is not None
    )

    logger.info(
        "FinGuard AI initialized | models_loaded=%s",
        APP_STATE["models_loaded"],
    )


# ============================================================
# DATASET HELPER
# ============================================================

def get_dataset():

    if APP_STATE["dataset"] is None:
        return load_dataset()

    return APP_STATE["dataset"]


# ============================================================
# COLUMN NORMALIZATION
# ============================================================

def normalize_column_name(column):

    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


# ============================================================
# COLUMN FINDER
# ============================================================

def find_column(df, candidates):

    if df.empty:
        return None

    normalized = {
        normalize_column_name(column): column
        for column in df.columns
    }

    for candidate in candidates:

        key = normalize_column_name(
            candidate
        )

        if key in normalized:
            return normalized[key]

    return None


# ============================================================
# IMPORTANT DATASET COLUMNS
# ============================================================

def get_target_column(df):

    column = find_column(
        df,
        ["Class"],
    )

    if column:
        return column

    return find_column(
        df,
        [
            "fraud",
            "is_fraud",
            "fraud_flag",
            "target",
            "label",
        ],
    )


def get_amount_column(df):

    return find_column(
        df,
        ["Amount"],
    )


def get_time_column(df):

    return find_column(
        df,
        ["Time"],
    )


def get_transaction_id_column(df):

    return find_column(
        df,
        [
            "Transaction_ID",
            "TransactionID",
            "transaction_id",
            "id",
            "ID",
        ],
    )


# ============================================================
# FRAUD VALUE DETECTION
# ============================================================

def is_fraud_value(value):

    if pd.isna(value):
        return False

    try:

        numeric_value = float(value)

        if numeric_value == 1:
            return True

        if numeric_value == 0:
            return False

    except (
        ValueError,
        TypeError,
    ):

        pass

    normalized = (
        str(value)
        .strip()
        .lower()
    )

    return normalized in [
        "1",
        "true",
        "fraud",
        "fraudulent",
        "yes",
        "high",
        "high risk",
    ]


# ============================================================
# FRAUD COUNTS
# ============================================================

def get_fraud_counts(df):

    if df.empty:
        return 0, 0

    target_col = get_target_column(df)

    if target_col is None:

        logger.warning(
            "Fraud target column not found."
        )

        return 0, len(df)

    fraud_mask = df[
        target_col
    ].apply(is_fraud_value)

    fraud_count = int(
        fraud_mask.sum()
    )

    legitimate_count = int(
        len(df) - fraud_count
    )

    return fraud_count, legitimate_count


# ============================================================
# NUMERIC HELPER
# ============================================================

def safe_float(value, default=0.0):

    try:

        numeric = float(value)

        if np.isnan(numeric):
            return default

        if np.isinf(numeric):
            return default

        return numeric

    except (
        ValueError,
        TypeError,
    ):

        return default


# ============================================================
# RISK SCORE
# ============================================================

def calculate_risk_score(row):

    explicit_columns = [
        "risk_score",
        "Risk_Score",
        "fraud_score",
    ]

    for column in explicit_columns:

        if column in row.index:

            value = safe_float(
                row[column],
                default=-1,
            )

            if value >= 0:

                if value <= 1:
                    value *= 100

                return round(
                    float(
                        np.clip(
                            value,
                            0,
                            100,
                        )
                    ),
                    2,
                )


    probability_columns = [
        "fraud_probability",
        "Fraud_Probability",
        "probability",
        "Probability",
    ]

    for column in probability_columns:

        if column in row.index:

            probability = safe_float(
                row[column],
                default=-1,
            )

            if probability >= 0:

                if probability <= 1:
                    probability *= 100

                return round(
                    float(
                        np.clip(
                            probability,
                            0,
                            100,
                        )
                    ),
                    2,
                )


    if "Class" in row.index:

        if is_fraud_value(
            row["Class"]
        ):
            return 90.0

        return 10.0


    for column in [
        "Fraud",
        "fraud",
        "is_fraud",
        "fraud_flag",
        "target",
        "label",
    ]:

        if column in row.index:

            if is_fraud_value(
                row[column]
            ):
                return 90.0

            return 10.0


    return 0.0


# ============================================================
# RISK LABEL
# ============================================================

def get_risk_label(score):

    score = safe_float(score)

    if score >= 75:
        return "High Risk"

    if score >= 40:
        return "Medium Risk"

    return "Low Risk"


# ============================================================
# DASHBOARD DATA
# ============================================================

def build_dashboard_data():

    df = get_dataset()

    if df.empty:

        return {
            "total_transactions": 0,
            "fraud_transactions": 0,
            "fraud_detected": 0,
            "legitimate_transactions": 0,
            "fraud_rate": 0,
            "high_risk": 0,
            "medium_risk": 0,
            "low_risk": 0,
            "average_risk": 0,
            "model_status": "Offline",
            "dataset_rows": 0,
            "recent_transactions": [],
            "total": 0,
            "transactions": 0,
            "fraud": 0,
            "fraud_count": 0,
            "legitimate": 0,
            "legitimate_count": 0,
            "fraud_percentage": 0,
            "avg_risk": 0,
            "risk_score": 0,
            "status": "Offline",
        }


    # --------------------------------------------------------
    # FRAUD
    # --------------------------------------------------------

    fraud_count, legitimate_count = (
        get_fraud_counts(df)
    )

    total = len(df)

    fraud_rate = (
        (fraud_count / total) * 100
        if total
        else 0
    )


    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk_scores = []

    for _, row in df.iterrows():

        score = calculate_risk_score(row)

        risk_scores.append(score)


    if risk_scores:

        average_risk = round(
            float(
                np.mean(risk_scores)
            ),
            2,
        )

        high_risk = sum(
            score >= 75
            for score in risk_scores
        )

        medium_risk = sum(
            40 <= score < 75
            for score in risk_scores
        )

        low_risk = sum(
            score < 40
            for score in risk_scores
        )

    else:

        average_risk = 0
        high_risk = 0
        medium_risk = 0
        low_risk = 0


    # --------------------------------------------------------
    # RECENT TRANSACTIONS
    # --------------------------------------------------------

    recent_transactions = []

    amount_column = get_amount_column(df)
    time_column = get_time_column(df)
    id_column = get_transaction_id_column(df)
    target_column = get_target_column(df)

    recent_df = (
        df.tail(8)
        .iloc[::-1]
    )


    for index, row in recent_df.iterrows():

        if id_column:

            transaction_id = str(
                row[id_column]
            )

        else:

            transaction_id = (
                f"TXN-{index + 1:05d}"
            )


        if amount_column:

            amount_value = safe_float(
                row[amount_column]
            )

            amount = round(
                amount_value,
                2,
            )

        else:

            amount = None


        score = calculate_risk_score(row)


        if target_column:

            status = (
                "Fraud"
                if is_fraud_value(
                    row[target_column]
                )
                else "Legitimate"
            )

        else:

            status = (
                "Fraud"
                if score >= 75
                else "Legitimate"
            )


        if time_column:

            time_value = row[time_column]

            if pd.isna(time_value):
                time_value = "—"
            else:
                time_value = str(
                    time_value
                )

        else:

            time_value = "—"


        recent_transactions.append(
            {
                "id": transaction_id,
                "time": time_value,
                "amount": amount,
                "risk_score": score,
                "risk": get_risk_label(score),
                "status": status,
            }
        )


    model_status = (
        "Active"
        if APP_STATE["models_loaded"]
        else "Offline"
    )


    return {

        "total_transactions": total,

        "fraud_transactions": fraud_count,

        # Homepage compatibility alias
        "fraud_detected": fraud_count,

        "legitimate_transactions":
            legitimate_count,

        "fraud_rate":
            round(fraud_rate, 2),

        "high_risk":
            high_risk,

        "medium_risk":
            medium_risk,

        "low_risk":
            low_risk,

        "average_risk":
            average_risk,

        "model_status":
            model_status,

        "dataset_rows":
            total,

        "recent_transactions":
            recent_transactions,

        # Compatibility aliases
        "total":
            total,

        "transactions":
            total,

        "fraud":
            fraud_count,

        "fraud_count":
            fraud_count,

        "legitimate":
            legitimate_count,

        "legitimate_count":
            legitimate_count,

        "fraud_percentage":
            round(fraud_rate, 2),

        "avg_risk":
            average_risk,

        "risk_score":
            average_risk,

        "status":
            model_status,
    }


# ============================================================
# CHART DATA
# ============================================================

def build_chart_data():

    df = get_dataset()

    if df.empty:

        return {

            "fraud_distribution": {
                "labels": [
                    "Legitimate",
                    "Fraud",
                ],
                "values": [
                    0,
                    0,
                ],
            },

            "risk_distribution": {
                "labels": [
                    "Low Risk",
                    "Medium Risk",
                    "High Risk",
                ],
                "values": [
                    0,
                    0,
                    0,
                ],
            },
        }


    fraud_count, legitimate_count = (
        get_fraud_counts(df)
    )


    high = 0
    medium = 0
    low = 0


    for _, row in df.iterrows():

        score = calculate_risk_score(row)

        if score >= 75:
            high += 1

        elif score >= 40:
            medium += 1

        else:
            low += 1


    return {

        "fraud_distribution": {

            "labels": [
                "Legitimate",
                "Fraud",
            ],

            "values": [
                legitimate_count,
                fraud_count,
            ],
        },

        "risk_distribution": {

            "labels": [
                "Low Risk",
                "Medium Risk",
                "High Risk",
            ],

            "values": [
                low,
                medium,
                high,
            ],
        },
    }


# ============================================================
# TRANSACTION TABLE
# ============================================================

def build_transaction_table():

    df = get_dataset()

    if df.empty:
        return []


    records = []

    target_col = get_target_column(df)
    amount_col = get_amount_column(df)
    time_col = get_time_column(df)
    id_col = get_transaction_id_column(df)


    recent_df = (
        df.tail(100)
        .iloc[::-1]
    )


    for index, row in recent_df.iterrows():

        if id_col:

            transaction_id = str(
                row[id_col]
            )

        else:

            transaction_id = (
                f"TXN-{index + 1:05d}"
            )


        if time_col:

            time_value = row[time_col]

            if pd.isna(time_value):
                time_value = "—"
            else:
                time_value = str(
                    time_value
                )

        else:

            time_value = "—"


        if amount_col:

            amount_value = safe_float(
                row[amount_col]
            )

            amount_value = round(
                amount_value,
                2,
            )

        else:

            amount_value = "—"


        score = calculate_risk_score(row)

        risk_label = get_risk_label(score)


        if target_col:

            status = (
                "Fraud"
                if is_fraud_value(
                    row[target_col]
                )
                else "Legitimate"
            )

        else:

            status = (
                "Fraud"
                if score >= 75
                else "Legitimate"
            )


        records.append(
            {
                "id": transaction_id,
                "time": time_value,
                "amount": amount_value,
                "risk_score": score,
                "risk": risk_label,
                "status": status,
            }
        )


    return records


# ============================================================
# MODEL FEATURE NAMES
# ============================================================

def get_model_feature_names():

    metadata = APP_STATE[
        "feature_metadata"
    ]

    feature_names = None


    if isinstance(
        metadata,
        dict,
    ):

        possible_keys = [
            "features",
            "feature_names",
            "columns",
            "input_features",
            "selected_features",
        ]

        for key in possible_keys:

            value = metadata.get(key)

            if isinstance(
                value,
                (list, tuple),
            ):

                feature_names = list(value)

                break


    if feature_names is None:

        model = APP_STATE["fraud_model"]

        if model is not None:

            if hasattr(
                model,
                "feature_names_in_",
            ):

                feature_names = list(
                    model.feature_names_in_
                )


    if feature_names is None:

        model = APP_STATE["fraud_model"]

        if model is not None:

            if hasattr(
                model,
                "steps",
            ):

                for _, estimator in reversed(
                    model.steps
                ):

                    if hasattr(
                        estimator,
                        "feature_names_in_",
                    ):

                        feature_names = list(
                            estimator.feature_names_in_
                        )

                        break


    return feature_names


# ============================================================
# PREDICTION INPUT
# ============================================================

def prepare_prediction_input(form_data):

    feature_names = (
        get_model_feature_names()
    )


    if feature_names is None:

        feature_names = [
            key
            for key in form_data.keys()
            if key not in [
                "csrf_token",
                "submit",
            ]
        ]


    values = []
    final_features = []


    for feature in feature_names:

        raw_value = None

        try:

            raw_value = form_data.get(
                feature
            )

        except Exception:

            raw_value = None


        if raw_value is None:

            normalized_feature = (
                normalize_column_name(feature)
            )

            for key in form_data.keys():

                if (
                    normalize_column_name(key)
                    == normalized_feature
                ):

                    raw_value = form_data.get(key)

                    break


        if raw_value in [
            None,
            "",
        ]:

            value = 0.0

        else:

            try:
                value = float(raw_value)

            except (
                ValueError,
                TypeError,
            ):

                value = 0.0


        values.append(value)
        final_features.append(feature)


    return pd.DataFrame(
        [values],
        columns=final_features,
    )


# ============================================================
# PREDICTION ENGINE
# ============================================================

def run_prediction(form_data):

    model = APP_STATE["fraud_model"]


    if model is None:

        return {
            "success": False,
            "error":
                "Fraud detection model is not available.",
        }


    try:

        X = prepare_prediction_input(
            form_data
        )


        prediction = model.predict(X)

        predicted_value = prediction[0]


        probability = None


        if hasattr(
            model,
            "predict_proba",
        ):

            probabilities = (
                model.predict_proba(X)
            )


            if (
                probabilities is not None
                and probabilities.ndim == 2
            ):

                if probabilities.shape[1] >= 2:

                    probability = float(
                        probabilities[0][1]
                    )

                elif probabilities.shape[1] == 1:

                    probability = float(
                        probabilities[0][0]
                    )


        if isinstance(
            predicted_value,
            str,
        ):

            normalized_prediction = (
                predicted_value
                .strip()
                .lower()
            )

            is_fraud = (
                normalized_prediction
                in [
                    "1",
                    "fraud",
                    "fraudulent",
                    "true",
                    "yes",
                    "high",
                    "high risk",
                ]
            )

        else:

            try:

                is_fraud = (
                    int(predicted_value) == 1
                )

            except Exception:

                is_fraud = False


        if probability is not None:

            risk_score = probability * 100

        else:

            risk_score = (
                90.0
                if is_fraud
                else 10.0
            )


        risk_score = round(
            float(
                np.clip(
                    risk_score,
                    0,
                    100,
                )
            ),
            2,
        )


        confidence = round(
            max(
                risk_score,
                100 - risk_score,
            ),
            2,
        )


        fraud_probability = (
            round(
                probability * 100,
                2,
            )
            if probability is not None
            else risk_score
        )


        anomaly_status = (
            "Anomaly"
            if is_fraud
            else "Normal"
        )


        recommendation = (
            "Review & Investigate"
            if is_fraud
            else "Approve & Monitor"
        )


        amount_raw = (
            form_data.get("amount")
            or form_data.get("transaction_amount")
            or form_data.get("TransactionAmount")
            or form_data.get("Amount")
            or 0
        )


        amount_value = safe_float(
            amount_raw,
            default=0.0,
        )


        time_value = (
            form_data.get("transaction_time")
            or form_data.get("time")
            or form_data.get("timestamp")
            or form_data.get("TransactionTime")
            or "—"
        )


        result = {

            "success":
                True,

            "prediction":
                (
                    "Fraudulent"
                    if is_fraud
                    else "Legitimate"
                ),

            "is_fraud":
                is_fraud,

            "risk_score":
                risk_score,

            "confidence":
                confidence,

            "risk_level":
                get_risk_label(
                    risk_score
                ),

            "amount":
                amount_value,

            "transaction_amount":
                amount_value,

            "time":
                str(time_value),

            "transaction_time":
                str(time_value),

            "fraud_probability":
                fraud_probability,

            "anomaly_status":
                anomaly_status,

            "recommended_decision":
                recommendation,

            "recommendation":
                recommendation,

            "fraud_score":
                risk_score,

            "model":
                type(model).__name__,

            "model_path":
                (
                    str(
                        APP_STATE[
                            "fraud_model_path"
                        ]
                    )
                    if APP_STATE[
                        "fraud_model_path"
                    ]
                    else None
                ),

            "timestamp":
                datetime.now().strftime(
                    "%d %b %Y, %H:%M:%S"
                ),
        }


        APP_STATE[
            "last_prediction"
        ] = result


        logger.info(
            "Prediction completed | prediction=%s | risk=%s | confidence=%s",
            result["prediction"],
            result["risk_score"],
            result["confidence"],
        )


        return result


    except Exception as exc:

        logger.exception(
            "Prediction failed: %s",
            exc,
        )

        return {
            "success": False,
            "error": str(exc),
        }


# ============================================================
# TEMPLATE METRICS SAFETY LAYER
# ============================================================

def get_template_metrics():
    """Return a template-safe metrics dictionary for every page."""

    try:
        data = build_dashboard_data()
    except Exception as exc:
        logger.exception("Metrics generation failed: %s", exc)
        data = {}

    if not isinstance(data, dict):
        data = {}

    defaults = {
        "total_transactions": 0,
        "fraud_transactions": 0,
        "fraud_detected": 0,
        "legitimate_transactions": 0,
        "secure_transactions": 0,
        "fraud_rate": 0,
        "high_risk": 0,
        "medium_risk": 0,
        "low_risk": 0,
        "average_risk": 0,
        "avg_risk": 0,
        "risk_score": 0,
        "model_status": "Offline",
        "status": "Offline",
        "dataset_rows": 0,
        "recent_transactions": [],
        "total": 0,
        "transactions": 0,
        "fraud": 0,
        "fraud_count": 0,
        "legitimate": 0,
        "legitimate_count": 0,
        "fraud_percentage": 0,
    }

    merged = dict(defaults)
    merged.update(data)

    # Compatibility aliases used by different page versions.
    merged["total"] = merged.get("total_transactions", 0)
    merged["transactions"] = merged.get("total_transactions", 0)
    merged["fraud"] = merged.get("fraud_transactions", 0)
    merged["fraud_count"] = merged.get("fraud_transactions", 0)
    merged["fraud_detected"] = merged.get("fraud_transactions", merged.get("fraud_detected", 0))
    merged["legitimate"] = merged.get("legitimate_transactions", 0)
    merged["legitimate_count"] = merged.get("legitimate_transactions", 0)
    merged["secure_transactions"] = merged.get("legitimate_transactions", 0)
    merged["fraud_percentage"] = merged.get("fraud_rate", 0)
    merged["avg_risk"] = merged.get("average_risk", 0)
    merged["risk_score"] = merged.get("average_risk", 0)
    merged["status"] = merged.get("model_status", "Offline")

    return merged


# ============================================================
# GLOBAL TEMPLATE CONTEXT
# ============================================================

@app.context_processor
def inject_global_context():

    metrics = get_template_metrics()

    return {
        "app_name": "FinGuard AI",
        "app_version": "1.0",
        "current_year": datetime.now().year,
        "system_active": bool(APP_STATE.get("models_loaded")),
        "model_loaded": APP_STATE.get("fraud_model") is not None,
        "anomaly_loaded": APP_STATE.get("anomaly_model") is not None,
        "metrics": metrics,
        "dashboard_metrics": metrics,
    }


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    metrics = get_template_metrics()

    return render_template(
        "index.html",
        dashboard=metrics,
        metrics=metrics,
        dashboard_metrics=metrics,
        page_title="Home",
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    dashboard_data = (
        build_dashboard_data()
    )

    chart_data = (
        build_chart_data()
    )

    transactions = (
        build_transaction_table()
    )


    return render_template(

        "dashboard.html",

        dashboard=dashboard_data,

        metrics=dashboard_data,

        chart_data=chart_data,

        transactions=transactions,

        page_title="Dashboard",

    )


# ============================================================
# PREDICTION
# ============================================================

@app.route(
    "/prediction",
    methods=["GET", "POST"],
)
def prediction():

    result = None


    if request.method == "POST":

        result = run_prediction(
            request.form
        )


    feature_names = (
        get_model_feature_names()
    )


    if feature_names is None:

        feature_names = []


    return render_template(

        "prediction.html",

        result=result,

        feature_names=feature_names,

        metrics=build_dashboard_data(),

        page_title="Prediction",

    )


# ============================================================
# TRANSACTION ANALYSIS
# ============================================================

@app.route("/transaction")
def transaction():

    metrics = (
        build_dashboard_data()
    )

    transactions = (
        build_transaction_table()
    )


    return render_template(

        "transaction.html",

        metrics=metrics,

        dashboard=metrics,

        transactions=transactions,

        page_title="Transaction Analysis",

    )


# ============================================================
# ANALYTICS DATA
# ============================================================

def build_analytics_data():

    df = get_dataset()

    dashboard_data = (
        build_dashboard_data()
    )

    chart_data = (
        build_chart_data()
    )


    if df is None or df.empty:

        rows = 0
        columns = []
        numeric_columns = []
        missing_values = 0
        target_column = None

    else:

        rows = int(len(df))

        columns = [
            str(column)
            for column in df.columns
        ]

        numeric_columns = [
            str(column)
            for column in df.select_dtypes(
                include=np.number
            ).columns
        ]

        missing_values = int(
            df.isna().sum().sum()
        )

        target_column = get_target_column(df)

        if target_column is not None:
            target_column = str(
                target_column
            )


    fraud_count = int(
        dashboard_data.get(
            "fraud_transactions",
            0,
        ) or 0
    )


    legitimate_count = int(
        dashboard_data.get(
            "legitimate_transactions",
            0,
        ) or 0
    )


    average_risk = safe_float(
        dashboard_data.get(
            "average_risk",
            0,
        ),
        0.0,
    )


    fraud_rate = safe_float(
        dashboard_data.get(
            "fraud_rate",
            0,
        ),
        0.0,
    )


    model_status = dashboard_data.get(
        "model_status",
        "Offline",
    )


    return {

        "rows":
            rows,

        "fraud_count":
            fraud_count,

        "columns":
            columns,

        "missing_values":
            missing_values,

        "target_column":
            target_column,

        "numeric_columns":
            numeric_columns,

        "high_risk":
            int(
                dashboard_data.get(
                    "high_risk",
                    0,
                ) or 0
            ),

        "medium_risk":
            int(
                dashboard_data.get(
                    "medium_risk",
                    0,
                ) or 0
            ),

        "low_risk":
            int(
                dashboard_data.get(
                    "low_risk",
                    0,
                ) or 0
            ),

        "average_risk":
            average_risk,

        "avg_risk":
            average_risk,

        "risk_score":
            average_risk,

        "total":
            rows,

        "transactions":
            rows,

        "total_transactions":
            rows,

        "dataset_rows":
            rows,

        "fraud":
            fraud_count,

        "fraud_transactions":
            fraud_count,

        "legitimate":
            legitimate_count,

        "legitimate_count":
            legitimate_count,

        "legitimate_transactions":
            legitimate_count,

        "fraud_rate":
            fraud_rate,

        "fraud_percentage":
            fraud_rate,

        "model_status":
            model_status,

        "status":
            model_status,

        "recent_transactions":
            dashboard_data.get(
                "recent_transactions",
                [],
            ),

        "fraud_distribution":
            chart_data.get(
                "fraud_distribution",
                {
                    "labels": [
                        "Legitimate",
                        "Fraud",
                    ],
                    "values": [0, 0],
                },
            ),

        "risk_distribution":
            chart_data.get(
                "risk_distribution",
                {
                    "labels": [
                        "Low Risk",
                        "Medium Risk",
                        "High Risk",
                    ],
                    "values": [0, 0, 0],
                },
            ),
    }


# ============================================================
# ANALYTICS
# ============================================================

@app.route("/analytics")
def analytics():

    analytics_data = (
        build_analytics_data()
    )


    chart_data = {

        "fraud_distribution":
            analytics_data.get(
                "fraud_distribution",
                {
                    "labels": [
                        "Legitimate",
                        "Fraud",
                    ],
                    "values": [0, 0],
                },
            ),

        "risk_distribution":
            analytics_data.get(
                "risk_distribution",
                {
                    "labels": [
                        "Low Risk",
                        "Medium Risk",
                        "High Risk",
                    ],
                    "values": [0, 0, 0],
                },
            ),
    }


    return render_template(

        "analytics.html",

        analytics=analytics_data,

        dashboard=analytics_data,

        metrics=analytics_data,

        chart_data=chart_data,

        fraud_distribution=
            chart_data[
                "fraud_distribution"
            ],

        risk_distribution=
            chart_data[
                "risk_distribution"
            ],

        page_title="Analytics",

    )


# ============================================================
# USER ANALYSIS DATA
# ============================================================

def build_user_analysis_data():

    df = get_dataset()


    if df.empty:

        return {

            "total_users": 0,

            "high_risk": 0,

            "medium_risk": 0,

            "low_risk": 0,

            "avg_risk": 0,

            "users": [],

        }


    user_col = find_column(
        df,
        [
            "user_id",
            "userid",
            "user",
            "username",
            "customer_id",
            "customerid",
            "account_id",
            "accountid",
        ],
    )


    if user_col is None:

        user_values = [
            f"USER-{index + 1:04d}"
            for index in range(len(df))
        ]

    else:

        user_values = (
            df[user_col]
            .fillna("Unknown User")
            .astype(str)
            .tolist()
        )


    user_records = {}


    for position, (_, row) in enumerate(
        df.iterrows()
    ):

        user_id = user_values[position]

        score = calculate_risk_score(row)


        if user_id not in user_records:

            user_records[user_id] = {

                "user_id":
                    user_id,

                "risk_score":
                    score,

                "activity":
                    "Normal",

            }

        else:

            if (
                score
                >
                user_records[
                    user_id
                ]["risk_score"]
            ):

                user_records[
                    user_id
                ]["risk_score"] = score


    users = []


    for user in user_records.values():

        score = float(
            user.get(
                "risk_score",
                0,
            )
        )


        if score >= 75:
            risk_level = "High"

        elif score >= 40:
            risk_level = "Medium"

        else:
            risk_level = "Low"


        users.append(
            {

                "user_id":
                    user["user_id"],

                "risk_score":
                    round(score, 2),

                "risk_level":
                    risk_level,

                "activity":
                    user.get(
                        "activity",
                        "Normal",
                    ),
            }
        )


    users.sort(
        key=lambda item:
            item["risk_score"],
        reverse=True,
    )


    high_risk = sum(
        user["risk_level"] == "High"
        for user in users
    )


    medium_risk = sum(
        user["risk_level"] == "Medium"
        for user in users
    )


    low_risk = sum(
        user["risk_level"] == "Low"
        for user in users
    )


    if users:

        avg_risk = round(
            float(
                np.mean(
                    [
                        user["risk_score"]
                        for user in users
                    ]
                )
            ),
            2,
        )

    else:

        avg_risk = 0


    return {

        "total_users":
            len(users),

        "high_risk":
            high_risk,

        "medium_risk":
            medium_risk,

        "low_risk":
            low_risk,

        "avg_risk":
            avg_risk,

        "users":
            users[:100],
    }


# ============================================================
# USER ANALYSIS
# ============================================================

@app.route("/user-analysis")
def user_analysis():

    analysis_data = (
        build_user_analysis_data()
    )


    return render_template(

        "user_analysis.html",

        metrics=analysis_data,

        total_users=
            analysis_data[
                "total_users"
            ],

        high_risk=
            analysis_data[
                "high_risk"
            ],

        medium_risk=
            analysis_data[
                "medium_risk"
            ],

        low_risk=
            analysis_data[
                "low_risk"
            ],

        avg_risk=
            analysis_data[
                "avg_risk"
            ],

        users=
            analysis_data[
                "users"
            ],

        page_title="User Analysis",

    )


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():

    return render_template(

        "about.html",

        metrics=build_dashboard_data(),

        page_title="About FinGuard AI",

    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status":
            "healthy",

        "application":
            "FinGuard AI",

        "models": {

            "fraud":
                APP_STATE[
                    "fraud_model"
                ] is not None,

            "anomaly":
                APP_STATE[
                    "anomaly_model"
                ] is not None,
        },

        "fraud_model": (

            str(
                APP_STATE[
                    "fraud_model_path"
                ]
            )

            if APP_STATE[
                "fraud_model_path"
            ]

            else None
        ),

        "anomaly_model": (

            str(
                APP_STATE[
                    "anomaly_model_path"
                ]
            )

            if APP_STATE[
                "anomaly_model_path"
            ]

            else None
        ),

        "dataset": (

            str(
                APP_STATE[
                    "dataset_path"
                ]
            )

            if APP_STATE[
                "dataset_path"
            ]

            else None
        ),

        "dataset_rows":
            len(get_dataset()),

        "fraud_threshold":
            APP_STATE[
                "fraud_threshold"
            ],

        "timestamp":
            datetime.now().isoformat(),

    })


# ============================================================
# API — DASHBOARD
# ============================================================

@app.route("/api/dashboard")
def api_dashboard():

    try:

        return jsonify({

            "success":
                True,

            "dashboard":
                build_dashboard_data(),

            "charts":
                build_chart_data(),

        })

    except Exception as exc:

        logger.exception(
            "Dashboard API error: %s",
            exc,
        )

        return jsonify({

            "success":
                False,

            "error":
                str(exc),

        }), 500


# ============================================================
# API — TRANSACTIONS
# ============================================================

@app.route("/api/transactions")
def api_transactions():

    try:

        transactions = (
            build_transaction_table()
        )


        return jsonify({

            "success":
                True,

            "count":
                len(transactions),

            "transactions":
                transactions,

        })

    except Exception as exc:

        logger.exception(
            "Transaction API error: %s",
            exc,
        )

        return jsonify({

            "success":
                False,

            "error":
                str(exc),

        }), 500


# ============================================================
# API — PREDICTION
# ============================================================

@app.route(
    "/api/predict",
    methods=["POST"],
)
def api_predict():

    try:

        payload = request.get_json(
            silent=True
        )


        if not payload:

            return jsonify({

                "success":
                    False,

                "error":
                    "No JSON input provided.",

            }), 400


        result = run_prediction(
            payload
        )


        status_code = (
            200
            if result.get("success")
            else 500
        )


        return jsonify(
            result
        ), status_code


    except Exception as exc:

        logger.exception(
            "API prediction error: %s",
            exc,
        )

        return jsonify({

            "success":
                False,

            "error":
                str(exc),

        }), 500


# ============================================================
# API — ANALYTICS
# ============================================================

@app.route("/api/metrics")
def api_metrics():

    try:

        analytics_data = (
            build_analytics_data()
        )


        return jsonify({

            "success":
                True,

            "metrics":
                analytics_data,

            "charts": {

                "fraud_distribution":
                    analytics_data.get(
                        "fraud_distribution",
                        {},
                    ),

                "risk_distribution":
                    analytics_data.get(
                        "risk_distribution",
                        {},
                    ),
            },

        })


    except Exception as exc:

        logger.exception(
            "Analytics metrics API error: %s",
            exc,
        )

        return jsonify({

            "success":
                False,

            "error":
                str(exc),

        }), 500


# ============================================================
# API — USER ANALYSIS
# ============================================================

@app.route("/api/users")
def api_users():

    try:

        data = (
            build_user_analysis_data()
        )


        return jsonify({

            "success":
                True,

            "data":
                data,

        })


    except Exception as exc:

        logger.exception(
            "User analysis API error: %s",
            exc,
        )

        return jsonify({

            "success":
                False,

            "error":
                str(exc),

        }), 500


# ============================================================
# API — SYSTEM STATUS
# ============================================================

@app.route("/api/status")
def api_status():

    dataset = get_dataset()


    return jsonify({

        "success":
            True,

        "application":
            "FinGuard AI",

        "status": (

            "Operational"

            if APP_STATE[
                "models_loaded"
            ]

            else "Monitoring"
        ),

        "fraud_model_loaded":
            APP_STATE[
                "fraud_model"
            ] is not None,

        "anomaly_model_loaded":
            APP_STATE[
                "anomaly_model"
            ] is not None,

        "dataset_loaded":
            not dataset.empty,

        "dataset_rows":
            len(dataset),

        "timestamp":
            datetime.now().isoformat(),

    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html",

        page_title="Page Not Found",

    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    logger.error(
        "Internal server error: %s",
        error,
    )


    return render_template(

        "404.html",

        page_title="Server Error",

    ), 500


# ============================================================
# SECURITY / CACHE HEADERS
# ============================================================

@app.after_request
def add_security_headers(response):

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"


    response.headers[
        "X-Frame-Options"
    ] = "SAMEORIGIN"


    response.headers[
        "Referrer-Policy"
    ] = (
        "strict-origin-when-cross-origin"
    )


    response.headers[
        "Cache-Control"
    ] = (
        "no-cache, "
        "no-store, "
        "must-revalidate"
    )


    return response


# ============================================================
# STARTUP
# ============================================================

initialize_system()


# ============================================================
# DEVELOPMENT SERVER
# ============================================================

if __name__ == "__main__":

    logger.info(
        "Starting FinGuard AI server..."
    )

    logger.info(
        "Open: http://127.0.0.1:5000"
    )

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True,

        threaded=True,

    )