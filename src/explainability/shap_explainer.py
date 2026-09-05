"""
FinGuard AI - SHAP Explainability
---------------------------------
Provides global and local explainability for the
final supervised fraud detection model.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "Models"
REPORTS_DIR = PROJECT_ROOT / "Reports" / "SHAP"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# MODEL LOADING
# ============================================================

def load_fraud_model(model_path=None):
    """
    Load the final fraud detection model.
    """

    if model_path is None:
        model_path = MODELS_DIR / "optimized_fraud_model.joblib"

    model_path = Path(model_path)

    if not model_path.exists():
        # Fallback to the best model artifact
        fallback_path = MODELS_DIR / "best_fraud_model.joblib"

        if fallback_path.exists():
            model_path = fallback_path
        else:
            raise FileNotFoundError(
                f"Fraud model not found.\n"
                f"Checked:\n"
                f"- {model_path}\n"
                f"- {fallback_path}"
            )

    model = joblib.load(model_path)

    return model


# ============================================================
# SHAP EXPLAINER
# ============================================================

def create_explainer(model):
    """
    Create the appropriate SHAP TreeExplainer
    for tree-based fraud models.
    """

    try:
        explainer = shap.TreeExplainer(model)
    except Exception as exc:
        raise RuntimeError(
            "Unable to create SHAP TreeExplainer. "
            "Make sure the loaded model is compatible "
            "with SHAP tree explainability."
        ) from exc

    return explainer


# ============================================================
# SHAP VALUE CALCULATION
# ============================================================

def calculate_shap_values(
    model,
    X,
    explainer=None
):
    """
    Calculate SHAP values for input samples.

    Returns
    -------
    np.ndarray
        SHAP values corresponding to the input features.
    """

    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)

    if explainer is None:
        explainer = create_explainer(model)

    shap_values = explainer.shap_values(X)

    # Handle binary classification output formats
    if isinstance(shap_values, list):
        if len(shap_values) == 2:
            shap_values = shap_values[1]
        else:
            shap_values = shap_values[0]

    # Handle newer SHAP Explanation objects
    if hasattr(shap_values, "values"):
        shap_values = shap_values.values

    shap_values = np.asarray(shap_values)

    return shap_values


# ============================================================
# LOCAL EXPLANATION
# ============================================================

def explain_transaction(
    model,
    transaction,
    feature_names=None,
    explainer=None
):
    """
    Explain a single transaction.

    Parameters
    ----------
    model : trained model
        Final fraud detection model.

    transaction : array-like or DataFrame
        Single transaction features.

    feature_names : list, optional
        Feature names.

    Returns
    -------
    DataFrame
        Feature-level SHAP contribution.
    """

    if isinstance(transaction, pd.Series):
        transaction = transaction.to_frame().T

    elif isinstance(transaction, dict):
        transaction = pd.DataFrame([transaction])

    elif not isinstance(transaction, pd.DataFrame):
        transaction = pd.DataFrame(transaction)

    if feature_names is not None:
        transaction.columns = feature_names

    shap_values = calculate_shap_values(
        model=model,
        X=transaction,
        explainer=explainer
    )

    values = shap_values[0]

    feature_names = list(transaction.columns)

    explanation = pd.DataFrame({
        "feature": feature_names,
        "value": transaction.iloc[0].values,
        "shap_value": values
    })

    explanation["absolute_shap"] = (
        explanation["shap_value"].abs()
    )

    explanation["impact"] = np.where(
        explanation["shap_value"] > 0,
        "Increases Fraud Risk",
        "Decreases Fraud Risk"
    )

    explanation = explanation.sort_values(
        "absolute_shap",
        ascending=False
    ).reset_index(drop=True)

    return explanation


# ============================================================
# GLOBAL FEATURE IMPORTANCE
# ============================================================

def calculate_global_importance(
    model,
    X,
    explainer=None
):
    """
    Calculate global SHAP feature importance.
    """

    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)

    shap_values = calculate_shap_values(
        model=model,
        X=X,
        explainer=explainer
    )

    importance = np.abs(shap_values).mean(axis=0)

    feature_importance = pd.DataFrame({
        "feature": X.columns,
        "mean_abs_shap": importance
    })

    feature_importance = feature_importance.sort_values(
        "mean_abs_shap",
        ascending=False
    ).reset_index(drop=True)

    return feature_importance


# ============================================================
# TOP FEATURES
# ============================================================

def get_top_features(
    feature_importance,
    top_n=20
):
    """
    Return the most influential features.
    """

    if not isinstance(
        feature_importance,
        pd.DataFrame
    ):
        raise TypeError(
            "feature_importance must be a DataFrame."
        )

    required_columns = {
        "feature",
        "mean_abs_shap"
    }

    if not required_columns.issubset(
        feature_importance.columns
    ):
        raise ValueError(
            "Feature importance DataFrame must contain "
            "'feature' and 'mean_abs_shap'."
        )

    return feature_importance.head(top_n).copy()


# ============================================================
# SAVE GLOBAL IMPORTANCE
# ============================================================

def save_global_importance(
    feature_importance,
    filename="global_feature_importance.csv"
):
    """
    Save global SHAP importance results.
    """

    output_path = REPORTS_DIR / filename

    feature_importance.to_csv(
        output_path,
        index=False
    )

    return output_path


# ============================================================
# SAVE TRANSACTION EXPLANATION
# ============================================================

def save_transaction_explanation(
    explanation,
    filename="transaction_explanation.csv"
):
    """
    Save local transaction explanation.
    """

    output_path = REPORTS_DIR / filename

    explanation.to_csv(
        output_path,
        index=False
    )

    return output_path


# ============================================================
# MODEL SUMMARY
# ============================================================

def get_model_explanation_summary(
    model,
    X,
    top_n=10
):
    """
    Generate a compact explainability summary.
    """

    explainer = create_explainer(model)

    importance = calculate_global_importance(
        model=model,
        X=X,
        explainer=explainer
    )

    top_features = get_top_features(
        importance,
        top_n=top_n
    )

    return {
        "total_features": X.shape[1],
        "samples_explained": X.shape[0],
        "top_features": top_features
    }


# ============================================================
# COMPLETE SHAP PIPELINE
# ============================================================

def run_shap_analysis(
    X,
    model=None,
    model_path=None,
    top_n=20
):
    """
    Run the complete SHAP analysis pipeline.

    Returns
    -------
    dict
        Model, explainer and feature importance results.
    """

    if model is None:
        model = load_fraud_model(model_path)

    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)

    explainer = create_explainer(model)

    shap_values = calculate_shap_values(
        model=model,
        X=X,
        explainer=explainer
    )

    feature_importance = calculate_global_importance(
        model=model,
        X=X,
        explainer=explainer
    )

    top_features = get_top_features(
        feature_importance,
        top_n=top_n
    )

    importance_path = save_global_importance(
        feature_importance
    )

    return {
        "model": model,
        "explainer": explainer,
        "shap_values": shap_values,
        "feature_importance": feature_importance,
        "top_features": top_features,
        "importance_path": importance_path
    }


# ============================================================
# HEALTH CHECK
# ============================================================

def explainability_status():
    """
    Return basic explainability module status.
    """

    model_path = MODELS_DIR / "optimized_fraud_model.joblib"

    return {
        "module": "SHAP Explainability",
        "status": "Ready",
        "model_available": model_path.exists(),
        "reports_directory": str(REPORTS_DIR)
    }