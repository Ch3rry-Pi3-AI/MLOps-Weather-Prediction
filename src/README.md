# `src/` README — Core Utilities (Custom Exception & Logger)

This folder contains **foundational utilities** for the **Weather Prediction MLOps pipeline**.
These modules provide **consistent logging** and **structured error handling** across all workflow stages — including **data ingestion**, **preprocessing**, **model training**, **evaluation**, and **deployment**.

## 📁 Folder Overview

```text
src/
├─ custom_exception.py   # Unified and detailed exception handling
└─ logger.py             # Centralised logging configuration
```

## ⚠️ `custom_exception.py` — Unified Error Handling

### Purpose

Defines a **CustomException** class that captures detailed debugging context for any error that occurs in the pipeline — whether during **weather data ingestion**, **feature standardisation**, **model fitting**, or **API inference**.

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

This ensures all exceptions are reported in a **consistent, traceable format** across the Weather Prediction pipeline — from data preparation to model inference.

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

## 🧩 Integration Guidelines

| Module Type        | Use `CustomException` for…                            | Use `get_logger` for…                                      |
| ------------------ | ----------------------------------------------------- | ---------------------------------------------------------- |
| Data Ingestion     | File loading failures, schema mismatches, empty files | File paths, record counts, schema summaries                |
| Preprocessing      | Missing values, scaling or encoding errors            | Feature engineering, imputations, outlier handling         |
| Model Training     | Invalid targets, convergence issues, NaNs in features | Training progress, hyperparameters, metrics per epoch      |
| Evaluation         | Metric computation, output file issues                | Validation metrics, error analysis, performance summaries  |
| Inference/Serving  | Invalid payloads, missing model artefacts             | Request summaries, predicted outputs, confidence intervals |
| CI/CD & Scheduling | Failed task steps, API timeouts                       | Pipeline stage logs, run durations, cloud job statuses     |

**Tip:** Combine both tools for robust debugging and traceability:

```python
from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def forecast(model, X):
    try:
        logger.info(f"Inference started for {len(X)} weather records.")
        predictions = model.predict(X)
        logger.info("Weather prediction inference completed successfully.")
        return predictions
    except Exception as e:
        logger.error("Inference step failed.")
        raise CustomException("Weather prediction inference error", sys) from e
```

## ✅ In summary

* `custom_exception.py` provides **clear, contextual error messages** for every exception.
* `logger.py` enables **structured, timestamped logging** across all project modules.

Together they form the **core reliability backbone** of the **MLOps Weather Prediction** pipeline — supporting reproducibility, debugging, and transparent experiment tracking throughout the lifecycle.
