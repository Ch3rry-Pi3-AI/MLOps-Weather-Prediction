# `src/` README — Core Utilities & Data Processing

This folder contains **foundational utilities** and **data-preparation logic** for the **Weather Prediction MLOps pipeline**.
These modules provide **consistent logging**, **structured error handling**, and a **reproducible preprocessing workflow** that together form the technical backbone of the pipeline — from **data ingestion** to **model training** and **deployment**.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py   # Unified and detailed exception handling
├─ logger.py             # Centralised logging configuration
└─ data_processing.py    # Complete preprocessing and dataset preparation workflow
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Defines a **CustomException** class that captures detailed debugging context for any error that occurs in the pipeline — whether during **weather data ingestion**, **feature engineering**, **model fitting**, or **API inference**.

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

This ensures all exceptions are reported in a **consistent, traceable format** across the Weather Prediction pipeline — from data preparation to inference.

## 🪵 `logger.py` — Centralised Logging

### Purpose

Provides a **standardised logging setup** for the Weather Prediction project.
Each log message is timestamped and written to a dated log file inside a `logs/` directory — enabling a clear audit trail across **data transformations**, **training runs**, and **prediction requests**.

### Log File Format

* Directory: `logs/`
* File name: `log_YYYY-MM-DD.log`
* Example: `logs/log_2025-11-06.log`

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

logger.info("Starting weather prediction pipeline.")
logger.warning("Missing temperature values detected. Applying linear interpolation.")
logger.error("Model training aborted due to invalid input features.")
```

### Output Example

```
2025-11-06 12:04:31,892 - INFO - Starting weather prediction pipeline.
2025-11-06 12:04:32,441 - WARNING - Missing temperature values detected. Applying linear interpolation.
2025-11-06 12:04:33,009 - ERROR - Model training aborted due to invalid input features.
```

## 🌦️ `data_processing.py` — End-to-End Data Preparation

### Purpose

Implements the **`DataProcessing`** class, which automates the key steps in preparing weather data for machine learning.
It performs **data loading**, **cleaning**, **feature extraction**, **encoding**, and **dataset splitting**, ensuring reproducible and consistent input for model training.

### Key Features

* Converts `Date` column into **Year, Month, and Day** components
* Automatically distinguishes **categorical** and **numerical** columns
* Applies **mean imputation** for missing numeric values
* Applies **label encoding** to weather-related categorical features
* Splits the dataset into **train/test** sets and saves them as `.pkl` artefacts

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

## 🧩 Integration Guidelines

| Module Type        | Use `CustomException` for…                             | Use `get_logger` for…                                      | Use `DataProcessing` for…                         |
| ------------------ | ------------------------------------------------------ | ---------------------------------------------------------- | ------------------------------------------------- |
| Data Ingestion     | File loading failures, schema mismatches, empty files  | File paths, record counts, schema summaries                | Reading and validating raw weather data           |
| Preprocessing      | Missing values, encoding or datetime conversion errors | Feature engineering, imputations, outlier handling         | Expanding date fields and imputing numeric values |
| Model Training     | Invalid targets, convergence issues, NaNs in features  | Training progress, hyperparameters, metrics per epoch      | Providing clean, structured inputs for training   |
| Evaluation         | Metric computation, output file issues                 | Validation metrics, error analysis, performance summaries  | —                                                 |
| Inference/Serving  | Invalid payloads, missing model artefacts              | Request summaries, predicted outputs, confidence intervals | —                                                 |
| CI/CD & Scheduling | Failed task steps, API timeouts                        | Pipeline stage logs, run durations, cloud job statuses     | —                                                 |

## ✅ In summary

* `custom_exception.py` provides **clear, contextual error messages** for every exception.
* `logger.py` enables **structured, timestamped logging** across all project modules.
* `data_processing.py` delivers a **reproducible preprocessing pipeline** that transforms raw weather data into model-ready artefacts.

Together, they form the **core reliability and preparation layer** of the **MLOps Weather Prediction** system — supporting traceability, debugging, and consistent experiment management throughout the workflow.
