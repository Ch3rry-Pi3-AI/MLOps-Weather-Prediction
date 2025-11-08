# 🧩 **Training Pipeline — MLOps Weather Prediction**

This branch extends the **MLOps Weather Prediction** project by introducing the **`training_pipeline.py`** file inside the `pipeline/` directory.
It marks the **third executable stage** of the project, where all previous workflow components — **data preprocessing** and **model training** — are orchestrated together into a single, reproducible **end-to-end pipeline**.

## 🧠 **Overview**

The `training_pipeline.py` script serves as the **workflow controller** of the Weather Prediction MLOps system.
It sequentially runs the preprocessing and model training modules defined in `src/`, transforming raw meteorological data into a fully trained and evaluated model — ready for deployment or continuous integration workflows.

### 🔍 Core Responsibilities

| Stage | Operation                  | Description                                                                                   |
| ----: | -------------------------- | --------------------------------------------------------------------------------------------- |
|   1️⃣ | **Run Data Processing**    | Executes the `DataProcessing` class to clean, encode, and split raw weather data.             |
|   2️⃣ | **Train & Evaluate Model** | Executes the `ModelTraining` class to train an XGBoost model and compute performance metrics. |

## 🗂️ **Updated Project Structure**

```text
mlops_weather_prediction/
├── .venv/                           # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── weather_data.csv         # 🌦️ Input weather dataset
│   ├── processed/                   # 💾 Data prepared by preprocessing
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   └── y_test.pkl
│   └── models/                      # 🧠 Trained model artefacts
│       └── model.pkl
├── pipeline/                        # 🔄 End-to-end workflow orchestration
│   └── training_pipeline.py         # Executes full pipeline (data + training)
├── src/
│   ├── __init__.py
│   ├── custom_exception.py          # Unified and detailed exception handling
│   ├── logger.py                    # Centralised logging configuration
│   ├── data_processing.py           # 🌦️ Data preparation and encoding
│   └── model_training.py            # ⚙️ Model training, evaluation, and persistence
├── static/                          # 🌐 Visual assets (optional)
├── templates/                       # 🧩 Placeholder for web/API templates
├── .gitignore                       # 🚫 Git ignore rules
├── .python-version                  # 🐍 Python version pin
├── pyproject.toml                   # ⚙️ Project metadata and uv configuration
├── requirements.txt                 # 📦 Python dependencies
├── setup.py                         # 🔧 Editable install support
└── uv.lock                          # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Training Pipeline**

After ensuring that the raw dataset is present at `artifacts/raw/data.csv`, you can execute the **entire pipeline** — from preprocessing to model training — using:

```bash
python pipeline/training_pipeline.py
```

### ✅ **Expected Successful Output**

```console
2025-11-08 13:12:45,931 - INFO - Data loaded successfully. Shape: (145460, 23)
2025-11-08 13:12:46,017 - INFO - Basic data preprocessing completed.
2025-11-08 13:12:46,043 - INFO - Label encoding completed.
2025-11-08 13:12:46,088 - INFO - Data split and persistence completed successfully.
2025-11-08 13:12:46,092 - INFO - Data processing completed.
2025-11-08 13:12:46,175 - INFO - Model Training initialised.
2025-11-08 13:12:46,209 - INFO - Data loaded successfully.
2025-11-08 13:12:46,581 - INFO - Model trained and saved successfully at artifacts/models/model.pkl
2025-11-08 13:12:46,722 - INFO - Training model score: 0.91
2025-11-08 13:12:46,741 - INFO - Evaluation Results — Accuracy: 0.86 | Precision: 0.85 | Recall: 0.84 | F1-score: 0.84
2025-11-08 13:12:46,758 - INFO - Model training and evaluation completed successfully.
```

This confirms that:

* The **preprocessing** stage produced all expected artefacts.
* The **XGBoost model** was trained and saved successfully.
* The **evaluation metrics** were computed and logged clearly.

## 🧩 **Integration Overview**

| File                            | Purpose                                                                                |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| `src/data_processing.py`        | Prepares the raw dataset by cleaning, encoding, and splitting it into train/test sets. |
| `src/model_training.py`         | Trains, evaluates, and persists the XGBoost model using processed artefacts.           |
| `pipeline/training_pipeline.py` | Combines both stages into one reproducible, end-to-end execution pipeline.             |
| `src/logger.py`                 | Handles consistent logging across all pipeline stages.                                 |
| `src/custom_exception.py`       | Provides detailed and contextual error reporting for debugging.                        |

## 🧠 **Implementation Highlights**

* **End-to-End Automation:**
  A single command runs the full workflow — from raw data to a trained model.

* **Reproducibility:**
  All artefacts (processed data, trained model) are versioned and saved in `artifacts/` for traceability.

* **Error Handling and Logging:**
  Every step includes robust exception handling and timestamped logs for transparency and debugging.

* **Modular Design:**
  Each component (`DataProcessing`, `ModelTraining`) can be developed, tested, or replaced independently.

## ✅ **In summary**

This branch introduces a **fully orchestrated training pipeline**, connecting preprocessing and training into one automated workflow.
It represents a significant milestone in the **MLOps Weather Prediction** project — transitioning from modular development to a **complete, operational ML pipeline** ready for:

* CI/CD integration (GitHub Actions, Jenkins, or CircleCI)
* Workflow automation (Airflow or Kubeflow Pipelines)
* Scalable model retraining and deployment in production environments.
