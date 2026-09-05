"""
FinGuard AI - Preprocessing Module
----------------------------------
Reusable preprocessing utilities for transaction data.
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "Models"
PREPROCESSING_DIR = MODELS_DIR / "preprocessing"

SCALER_PATH = MODELS_DIR / "standard_scaler.joblib"


def load_scaler():
    """
    Load the scaler generated during the preprocessing stage.
    """
    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Scaler not found: {SCALER_PATH}"
        )

    return joblib.load(SCALER_PATH)


def save_scaler(scaler, filename="standard_scaler.joblib"):
    """
    Save a fitted scaler to the Models directory.
    """
    PREPROCESSING_DIR.mkdir(parents=True, exist_ok=True)

    path = PREPROCESSING_DIR / filename
    joblib.dump(scaler, path)

    return path


def scale_features(X, scaler=None):
    """
    Scale numerical features using the saved or supplied scaler.
    """
    if scaler is None:
        scaler = load_scaler()

    X_scaled = scaler.transform(X)

    return X_scaled


def prepare_features(data, target_column=None):
    """
    Separate features and target from a DataFrame.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame.")

    if target_column is not None:
        if target_column not in data.columns:
            raise ValueError(
                f"Target column '{target_column}' not found."
            )

        X = data.drop(columns=[target_column])
        y = data[target_column]

        return X, y

    return data.copy()