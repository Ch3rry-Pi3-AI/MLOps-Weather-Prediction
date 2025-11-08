# ⚙️ **Model Training — MLOps Weather Prediction**

This branch advances the **MLOps Weather Prediction** project by introducing the **`model_training.py`** module inside `src/`.
It represents the **second executable workflow stage** of the pipeline — focusing on **model training**, **evaluation**, and **persistence** using the preprocessed datasets generated in the previous data processing stage.

## 🧩 **Overview**

The `ModelTraining` class implements a **reproducible training and evaluation pipeline** built on **XGBoost**.
It loads the processed artefacts, trains a gradient-boosted tree classifier, evaluates performance using multiple metrics, and saves the trained model for later inference or deployment.

### 🔍 Core Responsibilities

| Stage | Operation          | Description                                                                                     |
| ----: | ------------------ | ----------------------------------------------------------------------------------------------- |
|   1️⃣ | **Load Data**      | Loads `X_train.pkl`, `X_test.pkl`, `y_train.pkl`, and `y_test.pkl` from `artifacts/processed/`. |
|   2️⃣ | **Train Model**    | Fits an `XGBClassifier` on the training data.                                                   |
|   3️⃣ | **Save Model**     | Serialises the trained model as `model.pkl` under `artifacts/models/`.                          |
|   4️⃣ | **Evaluate Model** | Computes accuracy, precision, recall, and F1-score using test data.                             |

## 🗂️ **Updated Project Structure**

```text
mlops_weather_prediction/
├── .venv/                           # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── weather_data.csv         # 🌦️ Input weather dataset
│   ├── processed/                   # 💾 Data prepared by the preprocessing stage
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   └── y_test.pkl
│   └── models/                      # 🧠 Trained model artefacts
│       └── model.pkl
├── pipeline/                        # ⚙️ Workflow orchestration (future automation)
├── src/
│   ├── __init__.py
│   ├── custom_exception.py          # Unified and detailed exception handling
│   ├── logger.py                    # Centralised logging configuration
│   ├── data_processing.py           # 🌦️ Weather data preparation pipeline
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

## ⚙️ **How to Run the Model Training Module**

After successfully running the data processing stage, ensure that the preprocessed artefacts exist in `artifacts/processed/`, then execute:

```bash
python src/model_training.py
```

### ✅ **Expected Successful Output**

```console
2025-11-08 12:04:02,584 - INFO - Model Training initialised...
2025-11-08 12:04:02,611 - INFO - Data loaded successfully...
2025-11-08 12:04:03,221 - INFO - Training and saving of model done...
2025-11-08 12:04:03,778 - INFO - Training model score : 0.91
2025-11-08 12:04:03,891 - INFO - Accuracy : 0.86 ; Precision : 0.85 ; Recall : 0.84 : F1-Score : 0.84
2025-11-08 12:04:03,912 - INFO - Model evaluation done..
2025-11-08 12:04:03,917 - INFO - Model training and evaluation completed successfully.
```

This confirms that:

* The processed data was loaded successfully.
* The XGBoost model was trained and persisted as `model.pkl`.
* Evaluation metrics were computed and logged clearly.

## 🧠 **Implementation Highlights**

* **Machine Learning Algorithm:**
  Uses `XGBClassifier` from **XGBoost**, a robust gradient-boosting algorithm suited for tabular datasets like weather data.

* **Integrated Logging** via `src/logger.py`
  Logs all major operations — including data loading, training progress, and metric results — with timestamps for full reproducibility.

* **Unified Exception Handling** via `src/custom_exception.py`
  Ensures consistent, contextualised error reporting in case of runtime or I/O failures.

* **Persisted Artefacts:**
  Trained models are saved under `artifacts/models/` to be reused for evaluation, inference, or deployment stages.

## 🧩 **Integration Guidelines**

| File                      | Purpose                                                  |
| ------------------------- | -------------------------------------------------------- |
| `src/model_training.py`   | Trains, evaluates, and saves the XGBoost model.          |
| `src/data_processing.py`  | Supplies preprocessed training and testing data.         |
| `src/custom_exception.py` | Provides structured, traceable error handling.           |
| `src/logger.py`           | Records all workflow steps and metrics for transparency. |

✅ **In summary:**
This branch transforms the project into a **fully functional training stage** — integrating data artefacts from preprocessing, training an XGBoost model, and generating key evaluation metrics.
It serves as the foundation for the upcoming **model evaluation**, **deployment**, and **CI/CD automation** phases in the **MLOps Weather Prediction** pipeline.
