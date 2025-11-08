"""
data_processing.py
==================
Implements the ``DataProcessing`` class for the Weather Prediction workflow.

Overview
--------
This module provides a minimal, reproducible data-preparation stage used in the
project setup. It:
1) Loads a CSV dataset from disk
2) Performs basic datetime expansion and numeric imputation
3) Applies label encoding to selected categorical columns
4) Splits the data into train/test sets
5) Persists splits to ``artifacts/processed/`` using Joblib

Notes
-----
- Datetime handling expands a ``Date`` column into ``Year``, ``Month``, and ``Day``.
- Numeric columns are imputed with the mean; residual missing values are dropped.
- Saved artefacts:
  * ``X_train.pkl``, ``X_test.pkl`` — feature matrices
  * ``y_train.pkl``, ``y_test.pkl`` — target vectors

Examples
--------
>>> dp = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
>>> dp.run()
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard & third-party imports
# -------------------------------------------------------------------
import os
from typing import List, Optional, Tuple

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# -------------------------------------------------------------------
# Internal imports
# -------------------------------------------------------------------
from src.logger import get_logger
from src.custom_exception import CustomException

# -------------------------------------------------------------------
# Logger setup
# -------------------------------------------------------------------
logger = get_logger(__name__)


# -------------------------------------------------------------------
# Class: DataProcessing
# -------------------------------------------------------------------
class DataProcessing:
    """
    Simple, reproducible data-processing pipeline for Weather Prediction.

    Parameters
    ----------
    input_path : str
        Path to the input CSV file (e.g., ``artifacts/raw/data.csv``).
    output_path : str
        Directory where processed artefacts are persisted
        (e.g., ``artifacts/processed``).

    Attributes
    ----------
    input_path : str
        Source CSV path.
    output_path : str
        Target directory for persisted artefacts.
    df : pd.DataFrame | None
        In-memory dataframe after loading.
    """

    def __init__(self, input_path: str, output_path: str) -> None:
        # Store incoming CSV path and target output directory
        self.input_path: str = input_path
        self.output_path: str = output_path

        # Placeholder for the loaded dataframe
        self.df: Optional[pd.DataFrame] = None

        # Ensure the output directory exists
        os.makedirs(self.output_path, exist_ok=True)

        # Log initialisation
        logger.info("Data Processing initialised.")

    # -------------------------------------------------------------------
    # Method: load_data
    # -------------------------------------------------------------------
    def load_data(self) -> None:
        """
        Load the dataset from ``self.input_path`` into ``self.df``.

        Raises
        ------
        CustomException
            If the CSV cannot be read.
        """
        try:
            # Read CSV into a dataframe
            self.df = pd.read_csv(self.input_path)

            # Log success with basic shape info
            logger.info("Data loaded successfully. Shape: %s", None if self.df is None else self.df.shape)
        except Exception as e:
            # Log the error for debugging
            logger.error("Error while loading data: %s", e)

            # Re-raise using the project's custom exception (call pattern preserved)
            raise CustomException("Failed to load data", e)

    # -------------------------------------------------------------------
    # Method: preprocess
    # -------------------------------------------------------------------
    def preprocess(self) -> None:
        """
        Perform basic preprocessing:
        - Identify categorical/numerical columns (for reference)
        - Expand ``Date`` ➜ ``Year``, ``Month``, ``Day``
        - Mean-impute numeric columns
        - Drop remaining missing values

        Raises
        ------
        CustomException
            If preprocessing fails.
        """
        try:
            # Guard against missing dataframe
            if self.df is None:
                raise ValueError("Dataframe is not loaded. Call `load_data()` first.")

            # Determine categorical and numerical columns (kept for parity with original logic)
            categorical: List[str] = []
            numerical: List[str] = []
            # Iterate over columns and separate by dtype
            for col in self.df.columns:
                if self.df[col].dtype == "object":
                    categorical.append(col)
                else:
                    numerical.append(col)

            # Convert Date column to datetime
            self.df["Date"] = pd.to_datetime(self.df["Date"])

            # Expand into Year / Month / Day features
            self.df["Year"] = self.df["Date"].dt.year
            self.df["Month"] = self.df["Date"].dt.month
            self.df["Day"] = self.df["Date"].dt.day

            # Drop the original Date column
            self.df.drop("Date", axis=1, inplace=True)

            # Mean-impute numeric columns, in place
            for col in numerical:
                self.df[col].fillna(self.df[col].mean(), inplace=True)

            # Drop any residual missing values
            self.df.dropna(inplace=True)

            # Log completion
            logger.info("Basic data preprocessing completed.")
        except Exception as e:
            # Log the error for debugging
            logger.error("Error while preprocessing data: %s", e)

            # Re-raise using the project's custom exception (call pattern preserved)
            raise CustomException("Failed to preprocess data", e)

    # -------------------------------------------------------------------
    # Method: label_encode
    # -------------------------------------------------------------------
    def label_encode(self) -> None:
        """
        Apply label encoding to specific categorical columns.

        Notes
        -----
        Columns encoded (kept as per original logic):
        - ``Location``, ``WindGustDir``, ``WindDir9am``, ``WindDir3pm``,
          ``RainToday``, ``RainTomorrow``

        Raises
        ------
        CustomException
            If label encoding fails.
        """
        try:
            # Guard against missing dataframe
            if self.df is None:
                raise ValueError("Dataframe is not loaded. Call `load_data()` first.")

            # Columns to encode (preserved)
            categorical: List[str] = [
                "Location",
                "WindGustDir",
                "WindDir9am",
                "WindDir3pm",
                "RainToday",
                "RainTomorrow",
            ]

            # Iterate over categorical columns and apply LabelEncoder
            for col in categorical:
                label_encoder = LabelEncoder()
                self.df[col] = label_encoder.fit_transform(self.df[col])

                # Build and log mapping (class → encoded int)
                label_mapping = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))
                logger.info("Label mapping for %s: %s", col, label_mapping)

            # Log completion
            logger.info("Label encoding completed.")
        except Exception as e:
            # Log the error for debugging
            logger.error("Error while label encoding data: %s", e)

            # Re-raise using the project's custom exception (call pattern preserved)
            raise CustomException("Failed to label encode data", e)

    # -------------------------------------------------------------------
    # Method: split_data
    # -------------------------------------------------------------------
    def split_data(self) -> None:
        """
        Split features/target into train/test sets and persist them to disk.

        Notes
        -----
        - Features: all columns except ``RainTomorrow``
        - Target: ``RainTomorrow``

        Raises
        ------
        CustomException
            If the split or persistence fails.
        """
        try:
            # Guard against missing dataframe
            if self.df is None:
                raise ValueError("Dataframe is not loaded. Call `load_data()` first.")

            # Features (drop target column)
            X: pd.DataFrame = self.df.drop("RainTomorrow", axis=1)

            # Target (binary-encoded by previous step)
            Y: pd.Series = self.df["RainTomorrow"]

            # Log feature columns for traceability
            logger.info("Feature columns: %s", list(X.columns))

            # Perform the train/test split with a fixed seed for reproducibility
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            # Persist splits to the processed artefacts directory
            joblib.dump(X_train, os.path.join(self.output_path, "X_train.pkl"))
            joblib.dump(X_test, os.path.join(self.output_path, "X_test.pkl"))
            joblib.dump(y_train, os.path.join(self.output_path, "y_train.pkl"))
            joblib.dump(y_test, os.path.join(self.output_path, "y_test.pkl"))

            # Log successful file saves
            logger.info("Data split and persistence completed successfully.")
        except Exception as e:
            # Log the error for debugging
            logger.error("Error while splitting data: %s", e)

            # Re-raise using the project's custom exception (call pattern preserved)
            raise CustomException("Failed to split data", e)

    # -------------------------------------------------------------------
    # Method: run
    # -------------------------------------------------------------------
    def run(self) -> None:
        """
        Execute the full pipeline in order:
        1) Load data
        2) Preprocess (datetime expansion, imputation, drop NA)
        3) Label encode selected categorical columns
        4) Split and persist datasets
        """
        # Load the CSV
        self.load_data()

        # Apply preprocessing steps
        self.preprocess()

        # Encode categorical columns
        self.label_encode()

        # Split into train/test and save artefacts
        self.split_data()

        # Log completion
        logger.info("Data processing completed.")


# -------------------------------------------------------------------
# Script entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Default paths for input data and processed artefacts
    processor = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")

    # Run the pipeline end-to-end
    processor.run()
