"""
FinGuard AI - Application Logger
--------------------------------
Centralized logging utility for the application.
"""

import logging
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "finguard_ai.log"


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

def get_logger(
    name="FinGuardAI",
    level=logging.INFO
):
    """
    Create and return a configured application logger.
    """

    logger = logging.getLogger(name)

    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------------------------
    # File Handler
    # --------------------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # --------------------------------------------------------
    # Console Handler
    # --------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # --------------------------------------------------------
    # Attach Handlers
    # --------------------------------------------------------

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ============================================================
# DEFAULT APPLICATION LOGGER
# ============================================================

logger = get_logger()


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def log_info(message):
    """Log an informational message."""
    logger.info(message)


def log_warning(message):
    """Log a warning message."""
    logger.warning(message)


def log_error(message):
    """Log an error message."""
    logger.error(message)


def log_exception(message):
    """Log an exception with traceback information."""
    logger.exception(message)


# ============================================================
# LOGGER STATUS
# ============================================================

def logger_status():
    """
    Return logger configuration information.
    """

    return {
        "logger_name": logger.name,
        "log_level": logging.getLevelName(logger.level),
        "log_file": str(LOG_FILE),
        "log_directory": str(LOG_DIR),
        "status": "Ready"
    }