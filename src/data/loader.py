"""
FinGuard AI - Data Loader
-------------------------
Centralized utilities for loading datasets and saved artifacts.
"""

from pathlib import Path
import pandas as pd


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# Main directories
DATASET_DIR = PROJECT_ROOT / "Dataset"
RAW_DIR = DATASET_DIR / "Raw"
PROCESSED_DIR = DATASET_DIR / "Processed"
SAMPLE_DIR = DATASET_DIR / "Sample"


def load_raw_data(filename="creditcard.csv"):
    """
    Load the original raw credit-card transaction dataset.
    """
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def load_processed_data(filename):
    """
    Load a processed CSV dataset.
    """
    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def load_sample_data(filename="sample_transactions.csv"):
    """
    Load sample transaction data for application testing.
    """
    file_path = SAMPLE_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Sample dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def get_project_root():
    """
    Return the FinGuard AI project root directory.
    """
    return PROJECT_ROOT