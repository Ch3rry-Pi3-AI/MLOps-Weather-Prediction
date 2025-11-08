# 🧱 **`pipeline/` README — End-to-End Workflow Orchestration**

This folder contains the **workflow orchestration layer** of the **MLOps Weather Prediction** project.
It brings together all major stages — **data preprocessing**, **model training**, and **evaluation** — into a single, reproducible execution pipeline.

Where the `src/` directory contains the **modular building blocks** of the system, the `pipeline/` directory defines **how** those modules interact to produce a complete machine learning workflow.

## 📁 Folder Overview

```text
pipeline/
└── training_pipeline.py   # Orchestrates preprocessing, training, and evaluation
```

## ⚙️ **Purpose**

The pipeline automates the **end-to-end model development process** — from raw data to a trained and evaluated model — by sequentially invoking the core components in `src/`:

1. **Data Processing Stage**
   Conducts cleaning, feature extraction, encoding, and splitting of the raw weather dataset into training and testing artefacts.

2. **Model Training Stage**
   Trains an XGBoost model using the processed artefacts, evaluates its performance (Accuracy, Precision, Recall, F1-score), and saves the final trained model.

This orchestration ensures that every run follows a **consistent, traceable, and reproducible workflow**, ready for integration into future **CI/CD or Kubeflow pipelines**.

## 🔄 **Workflow Overview**

| Stage | Module Used                          | Description                                                                           |
| ----: | ------------------------------------ | ------------------------------------------------------------------------------------- |
|   1️⃣ | `src.data_processing.DataProcessing` | Loads, cleans, encodes, and splits weather data into training/testing artefacts.      |
|   2️⃣ | `src.model_training.ModelTraining`   | Trains and evaluates the XGBoost classifier, saving the model to `artifacts/models/`. |

## 🧩 **How to Run the Training Pipeline**

After completing environment setup and ensuring that the raw weather dataset exists at `artifacts/raw/data.csv`, execute:

```bash
python pipeline/training_pipeline.py
```

### ✅ **Expected Successful Output**

```console
2025-11-08 12:10:21,004 - INFO - Data loaded successfully. Shape: (145460, 23)
2025-11-08 12:10:21,175 - INFO - Basic data preprocessing completed.
2025-11-08 12:10:21,211 - INFO - Label encoding completed.
2025-11-08 12:10:21,242 - INFO - Data split and persistence completed successfully.
2025-11-08 12:10:21,250 - INFO - Data processing completed.
2025-11-08 12:10:21,372 - INFO - Model trained and saved successfully at artifacts/models/model.pkl
2025-11-08 12:10:21,498 - INFO - Training model score: 0.91
2025-11-08 12:10:21,543 - INFO - Evaluation Results — Accuracy: 0.86 | Precision: 0.85 | Recall: 0.84 | F1-score: 0.84
2025-11-08 12:10:21,571 - INFO - Model training and evaluation completed successfully.
```

This output confirms the successful completion of both pipeline stages — preprocessing and model training — with detailed logging at each step.

## 🧠 **Implementation Highlights**

* **Modular Integration:**
  Each component (data processing, training) is self-contained, enabling easy updates or substitutions without breaking the workflow.

* **Comprehensive Logging:**
  Every stage logs detailed progress and results using `src/logger.py`, ensuring full traceability of each pipeline execution.

* **Robust Exception Handling:**
  All errors are wrapped in `CustomException` from `src/custom_exception.py` for consistent debugging across modules.

* **Reproducibility:**
  The pipeline outputs versioned artefacts (`processed/` data and `models/` folder) for deterministic retraining.

## 🧩 **Integration Guidelines**

| Component       | Source Module         | Output Artefacts                                                             | Description                                                      |
| --------------- | --------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Data Processing | `src.data_processing` | `artifacts/processed/X_train.pkl`, `X_test.pkl`, `y_train.pkl`, `y_test.pkl` | Cleans and prepares weather data.                                |
| Model Training  | `src.model_training`  | `artifacts/models/model.pkl`                                                 | Trains, evaluates, and saves the final weather prediction model. |

## ✅ **In summary**

The `pipeline/` directory serves as the **operational backbone** of the MLOps Weather Prediction project.
It connects all core modules into a single, coherent workflow — transforming raw meteorological data into a fully trained and validated prediction model with just one command:

```bash
python pipeline/training_pipeline.py
```

This structure sets the stage for future automation via **GitHub Actions**, **Kubeflow Pipelines**, or **Airflow DAGs**, forming the foundation for a scalable, production-ready MLOps system.
