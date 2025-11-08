"""
training_pipeline.py
====================
Implements the end-to-end training workflow for the Weather Prediction MLOps pipeline.

Overview
--------
This module acts as the orchestration script that chains together all core workflow stages:
1) Data preprocessing (via ``DataProcessing``)
2) Model training and evaluation (via ``ModelTraining``)

It ensures that raw weather data is cleaned, encoded, split, and then used to train
and evaluate an XGBoost model — producing reproducible artefacts ready for deployment.

Examples
--------
>>> python pipeline/training_pipeline.py
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Internal imports
# -------------------------------------------------------------------
from src.data_processing import DataProcessing
from src.model_training import ModelTraining


# -------------------------------------------------------------------
# Script Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    """
    Main entrypoint for executing the full Weather Prediction training pipeline.

    Steps
    -----
    1) Run data preprocessing to generate clean train/test artefacts.
    2) Run model training and evaluation using those processed artefacts.
    """

    # -------------------------------------------------------------------
    # Stage 1: Data Preprocessing
    # -------------------------------------------------------------------
    processor = DataProcessing(
        input_path="artifacts/raw/data.csv",
        output_path="artifacts/processed"
    )

    # Execute preprocessing pipeline (cleaning, encoding, splitting)
    processor.run()

    # -------------------------------------------------------------------
    # Stage 2: Model Training & Evaluation
    # -------------------------------------------------------------------
    trainer = ModelTraining(
        input_path="artifacts/processed",
        output_path="artifacts/models"
    )

    # Execute model training, evaluation, and persistence
    trainer.run()
