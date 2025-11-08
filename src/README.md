# `src/` README — Core Utilities, Data Processing & Model Training

This folder contains the **core logic** for the **Weather Prediction MLOps pipeline**, including utilities for **error handling**, **logging**, **data preprocessing**, and **model training**.
Together, these modules establish a **reliable, reproducible, and modular foundation** for the project — covering every stage from **data ingestion** to **model evaluation** and eventual deployment.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py   # Unified and detailed exception handling
├─ logger.py             # Centralised logging configuration
├─ data_processing.py    # End-to-end preprocessing and dataset preparation
└─ model_training.py     # Model training, evaluation, and persistence
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Defines a **CustomException** class that captures detailed debugging context for any error that occurs in the pipeline — whether during **data ingestion**, **feature engineering**, **model fitting**, or **deployment**.

### Key Features

* Captures the **file name** and **line number** where the exception occurred
* Includes a formatted **traceback** for quick and consistent debugging
* Works with flexible inputs:

  * the `sys` module,
  * an explicit exception instance, or
  * no arguments (defaults to the current exception via `sys.exc_info()`)

### Example Usage

```python
from src.custom_exception import CustomException
import sys
import pandas as pd

try:
    df = pd.read_csv("data/raw/weather_data.csv")
    if df.empty:
        raise ValueError("Weather dataset is empty.")
except Exception as e:
    raise CustomException("Error during data ingestion", sys) from e
```

### Output Example

```
Error in /mlops-weather-prediction/src/data_ingestion.py, line 24: Error during data ingestion
Traceback (most recent call last):
  File "/mlops-weather-prediction/src/data_ingestion.py", line 24, in <module>
    df = pd.read_csv("data/raw/weather_data.csv")
ValueError: Weather dataset is empty.
```

This ensures all exceptions are reported in a **consistent, traceable format** throughout the Weather Prediction pipeline.

## 🪵 `logger.py` — Centralised Logging

### Purpose

Provides a **standardised logging system** for the Weather Prediction project.
Each log message is timestamped and written to a daily log file inside a `logs/` directory — maintaining a complete audit trail of all pipeline stages including **data processing**, **model training**, and **evaluation**.

### Log File Format

* Directory: `logs/`
* File name: `log_YYYY-MM-DD.log`
* Example: `logs/log_2025-11-08.log`

### Default Configuration

* Logging level: `INFO`
* Format:

  ```
  %(asctime)s - %(levelname)s - %(message)s
  ```

### Example Usage

```python
from src.logger import get_logger

logger = get_logger(__name__)

logger.info("Starting weather prediction model training.")
logger.warning("High variance detected in temperature data.")
logger.error("Model evaluation aborted due to missing test artefacts.")
```

### Output Example

```
2025-11-08 11:52:41,134 - INFO - Starting weather prediction model training.
2025-11-08 11:52:42,341 - WARNING - High variance detected in temperature data.
2025-11-08 11:52:43,002 - ERROR - Model evaluation aborted due to missing test artefacts.
```

## 🌦️ `data_processing.py` — End-to-End Data Preparation

### Purpose

Implements the **`DataProcessing`** class, which automates all preprocessing steps for weather data.
It handles **data loading**, **cleaning**, **date decomposition**, **encoding**, and **train/test splitting**, ensuring reproducible inputs for model development.

### Key Features

* Converts `Date` into **Year**, **Month**, and **Day** components
* Distinguishes between **categorical** and **numerical** columns automatically
* Fills missing numeric values using **mean imputation**
* Encodes categorical weather features using **label encoding**
* Splits data into **train/test sets** and saves them as `.pkl` artefacts

### Example Usage

```python
from src.data_processing import DataProcessing

processor = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
processor.run()
```

### Saved Artefacts

* `X_train.pkl`, `X_test.pkl` — feature matrices
* `y_train.pkl`, `y_test.pkl` — target vectors

### Log Example

```
INFO - Data loaded successfully. Shape: (145460, 23)
INFO - Basic data preprocessing completed.
INFO - Label encoding completed.
INFO - Data split and persistence completed successfully.
INFO - Data processing completed.
```

## ⚙️ `model_training.py` — Model Training and Evaluation

### Purpose

Implements the **`ModelTraining`** class, which trains and evaluates an **XGBoost classifier** using preprocessed data.
It loads artefacts from `artifacts/processed/`, fits the model, computes evaluation metrics, and saves the trained model for later inference or deployment.

### Key Features

* Loads preprocessed datasets from `artifacts/processed/`
* Trains an `XGBClassifier` on the weather features
* Computes **Accuracy**, **Precision**, **Recall**, and **F1-score**
* Persists the trained model to `artifacts/models/model.pkl`
* Integrates logging and exception handling throughout the workflow

### Example Usage

```python
from src.model_training import ModelTraining

trainer = ModelTraining("artifacts/processed", "artifacts/models")
trainer.run()
```

### Log Example

```
INFO - Model Training initialised.
INFO - Data loaded successfully.
INFO - Model trained and saved successfully at artifacts/models/model.pkl
INFO - Training model score: 0.91
INFO - Evaluation Results — Accuracy: 0.86 | Precision: 0.85 | Recall: 0.84 | F1-score: 0.84
INFO - Model evaluation completed successfully.
INFO - Model training and evaluation completed successfully.
```

## 🧩 Integration Guidelines

| Module Type        | Use `CustomException` for…                             | Use `get_logger` for…                                      | Use `DataProcessing` for…                         | Use `ModelTraining` for…                       |
| ------------------ | ------------------------------------------------------ | ---------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- |
| Data Ingestion     | File loading failures, schema mismatches, empty files  | File paths, record counts, schema summaries                | Reading and validating raw weather data           | —                                              |
| Preprocessing      | Missing values, encoding or datetime conversion errors | Feature engineering, imputations, outlier handling         | Expanding date fields and imputing numeric values | —                                              |
| Model Training     | Invalid targets, convergence issues, NaNs in features  | Training progress, hyperparameters, metrics per epoch      | Providing clean, structured inputs for training   | Fitting and persisting the XGBoost model       |
| Evaluation         | Metric computation, output file issues                 | Accuracy, precision, recall, and F1-score tracking         | —                                                 | Testing model performance and metric reporting |
| Inference/Serving  | Invalid payloads, missing model artefacts              | Request summaries, predicted outputs, confidence intervals | —                                                 | Reusing trained models for inference           |
| CI/CD & Scheduling | Failed task steps, API timeouts                        | Pipeline stage logs, run durations, cloud job statuses     | —                                                 | Automated retraining or scheduled evaluations  |

## ✅ In summary

* `custom_exception.py` ensures **consistent, contextual error handling**.
* `logger.py` enables **structured, timestamped logs** across all project modules.
* `data_processing.py` provides a **reproducible preprocessing workflow** for clean, model-ready datasets.
* `model_training.py` adds a **robust training and evaluation pipeline** powered by XGBoost.

Together, these modules form the **operational core** of the **MLOps Weather Prediction** system — delivering reliability, transparency, and full traceability across every stage of the machine learning lifecycle.
