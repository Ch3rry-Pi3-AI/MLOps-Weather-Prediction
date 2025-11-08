"""
model_training.py
=================
Implements the ``ModelTraining`` class for the Weather Prediction workflow.

Overview
--------
This module defines the training and evaluation stage of the MLOps Weather Prediction pipeline.
It:
1) Loads preprocessed data artefacts (``X_train.pkl``, ``y_train.pkl`` etc.)
2) Trains an XGBoost classifier
3) Evaluates model performance using multiple metrics
4) Persists the trained model for later inference and deployment

Notes
-----
- The model is trained using ``XGBClassifier`` from the XGBoost library.
- Evaluation metrics include Accuracy, Precision, Recall, and F1-score.
- Saved artefacts:
  * ``model.pkl`` — serialised model object for reuse in later stages.

Examples
--------
>>> trainer = ModelTraining("artifacts/processed", "artifacts/models")
>>> trainer.run()
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard & third-party imports
# -------------------------------------------------------------------
import os
import joblib
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

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
# Class: ModelTraining
# -------------------------------------------------------------------
class ModelTraining:
    """
    A reproducible training and evaluation workflow using XGBoost.

    Parameters
    ----------
    input_path : str
        Directory containing preprocessed training and test artefacts.
        (e.g., ``artifacts/processed``)
    output_path : str
        Directory where the trained model will be saved.
        (e.g., ``artifacts/models``)

    Attributes
    ----------
    input_path : str
        Directory for input artefacts.
    output_path : str
        Directory for output model artefacts.
    model : xgb.XGBClassifier
        Instance of the XGBoost classifier.
    X_train, X_test, y_train, y_test : pd.DataFrame | None
        Training and testing splits loaded from disk.
    """

    def __init__(self, input_path: str, output_path: str) -> None:
        # Paths for loading data and saving models
        self.input_path: str = input_path
        self.output_path: str = output_path

        # Initialise XGBoost classifier
        self.model: xgb.XGBClassifier = xgb.XGBClassifier()

        # Placeholders for datasets
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        # Ensure output directory exists
        os.makedirs(self.output_path, exist_ok=True)

        # Log initialisation
        logger.info("Model Training initialised.")

    # -------------------------------------------------------------------
    # Method: load_data
    # -------------------------------------------------------------------
    def load_data(self) -> None:
        """
        Load preprocessed datasets from ``self.input_path``.

        Raises
        ------
        CustomException
            If any artefact file cannot be loaded.
        """
        try:
            # Load feature and label datasets
            self.X_train = joblib.load(os.path.join(self.input_path, "X_train.pkl"))
            self.X_test = joblib.load(os.path.join(self.input_path, "X_test.pkl"))
            self.y_train = joblib.load(os.path.join(self.input_path, "y_train.pkl"))
            self.y_test = joblib.load(os.path.join(self.input_path, "y_test.pkl"))

            # Log success
            logger.info("Preprocessed data loaded successfully.")
        except Exception as e:
            # Log and raise wrapped exception
            logger.error("Error while loading data: %s", e)
            raise CustomException("Failed to load data", e)

    # -------------------------------------------------------------------
    # Method: train_model
    # -------------------------------------------------------------------
    def train_model(self) -> None:
        """
        Train the XGBoost classifier and persist the model to disk.

        Raises
        ------
        CustomException
            If training or persistence fails.
        """
        try:
            # Fit model to training data
            self.model.fit(self.X_train, self.y_train)

            # Save trained model to disk
            model_path = os.path.join(self.output_path, "model.pkl")
            joblib.dump(self.model, model_path)

            # Log successful training
            logger.info("Model trained and saved successfully at %s", model_path)
        except Exception as e:
            # Log and raise wrapped exception
            logger.error("Error while training model: %s", e)
            raise CustomException("Failed to train model", e)

    # -------------------------------------------------------------------
    # Method: eval_model
    # -------------------------------------------------------------------
    def eval_model(self) -> None:
        """
        Evaluate the trained model on the test dataset using standard metrics.

        Metrics computed
        ----------------
        - Accuracy
        - Precision (weighted)
        - Recall (weighted)
        - F1-score (weighted)

        Raises
        ------
        CustomException
            If evaluation fails.
        """
        try:
            # Compute training score directly from model
            training_score = self.model.score(self.X_train, self.y_train)
            logger.info("Training model score: %.4f", training_score)

            # Predict on test data
            y_pred = self.model.predict(self.X_test)

            # Compute evaluation metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average="weighted")
            recall = recall_score(self.y_test, y_pred, average="weighted")
            f1 = f1_score(self.y_test, y_pred, average="weighted")

            # Log results
            logger.info(
                "Evaluation Results — Accuracy: %.4f | Precision: %.4f | Recall: %.4f | F1-score: %.4f",
                accuracy,
                precision,
                recall,
                f1,
            )

            # Log completion
            logger.info("Model evaluation completed successfully.")
        except Exception as e:
            logger.error("Error while evaluating model: %s", e)
            raise CustomException("Failed to evaluate model", e)

    # -------------------------------------------------------------------
    # Method: run
    # -------------------------------------------------------------------
    def run(self) -> None:
        """
        Execute the complete model-training workflow:
        1) Load data
        2) Train model
        3) Evaluate model
        """
        # Load preprocessed artefacts
        self.load_data()

        # Train and save model
        self.train_model()

        # Evaluate performance
        self.eval_model()

        # Final log message
        logger.info("Model training and evaluation completed successfully.")


# -------------------------------------------------------------------
# Script entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Default input/output paths
    trainer = ModelTraining("artifacts/processed", "artifacts/models")

    # Execute full training workflow
    trainer.run()
