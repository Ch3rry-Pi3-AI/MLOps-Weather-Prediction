"""
logger.py
----------
Centralised logging configuration module for the
MLOps Titanic Survival Prediction project.

This script sets up a standardised logging system that writes logs
to a dedicated `logs/` directory and prints messages to the console.
Each log file is automatically named by date (`log_YYYY-MM-DD.log`)
and encoded in UTF-8 to support special characters and emojis.

It provides a simple helper function, `get_logger(name)`, that returns
a configured logger instance for use across all modules.

Usage
-----
Example:
    from src.logger import get_logger

    logger = get_logger(__name__)
    logger.info("🚀 Model training started.")
    logger.error("❌ Failed to connect to database.")

Notes
-----
- Logs are written to `logs/log_YYYY-MM-DD.log` (UTF-8 encoded)
- Each message includes a timestamp and severity level.
- Default level: INFO
- Console and file outputs both support Unicode characters.
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
import logging
import os
import sys
from datetime import datetime

# -------------------------------------------------------------------
# Directory Setup
# -------------------------------------------------------------------
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Log File Configuration
# -------------------------------------------------------------------
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# -------------------------------------------------------------------
# Logger Factory Function
# -------------------------------------------------------------------
def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance with UTF-8 support for both
    console and file output.

    Parameters
    ----------
    name : str
        The name of the logger, typically `__name__`.

    Returns
    -------
    logging.Logger
        A logger object with INFO-level configuration and handlers set.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers if re-imported
    if not logger.handlers:
        # -------------------------------------------------------------------
        # File Handler (UTF-8)
        # -------------------------------------------------------------------
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        # -------------------------------------------------------------------
        # Console Handler (UTF-8)
        # -------------------------------------------------------------------
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Ensure stdout stream is UTF-8 encoded (Python 3.9+)
        if hasattr(console_handler.stream, "reconfigure"):
            console_handler.stream.reconfigure(encoding="utf-8")

        # -------------------------------------------------------------------
        # Formatter
        # -------------------------------------------------------------------
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # -------------------------------------------------------------------
        # Attach Handlers
        # -------------------------------------------------------------------
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger