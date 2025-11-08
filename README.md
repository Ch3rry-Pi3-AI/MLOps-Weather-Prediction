# 🌦️ **Data Processing — MLOps Weather Prediction**

This branch builds upon the **initial setup** by introducing the **`data_processing.py`** module inside `src/`.
It marks the **first executable workflow stage** of the **MLOps Weather Prediction** pipeline — responsible for loading raw weather data, cleaning and transforming it, encoding categorical features, and saving train/test splits for model training.

## 🧩 **Overview**

The `DataProcessing` class implements a **reproducible preprocessing pipeline** with integrated logging and unified exception handling.
It prepares clean, structured datasets ready for downstream weather forecasting models.

### 🔍 Core Responsibilities

| Stage | Operation          | Description                                                                               |
| ----: | ------------------ | ----------------------------------------------------------------------------------------- |
|   1️⃣ | **Load Data**      | Reads input CSV from `artifacts/raw/weather_data.csv`.                                    |
|   2️⃣ | **Preprocess**     | Expands `Date` into `Year`, `Month`, and `Day`, imputes missing values.                   |
|   3️⃣ | **Label Encode**   | Converts categorical columns (e.g., wind directions, rain indicators) into numeric codes. |
|   4️⃣ | **Split Data**     | Creates 80/20 train/test splits for features and target (`RainTomorrow`).                 |
|   5️⃣ | **Save Artefacts** | Writes `X_train.pkl`, `X_test.pkl`, `y_train.pkl`, and `y_test.pkl` to disk.              |

## 🗂️ **Updated Project Structure**

```text
mlops_weather_prediction/
├── .venv/                          # 🧩 Local virtual environment (created by uv)
├── artifacts/
│   ├── raw/
│   │   └── weather_data.csv        # 🌦️ Input weather dataset
│   └── processed/                  # 💾 Output directory for processed data
│       ├── X_train.pkl
│       ├── X_test.pkl
│       ├── y_train.pkl
│       └── y_test.pkl
├── mlops_weather_prediction.egg-info/ # 📦 Package metadata (auto-generated)
├── pipeline/                       # ⚙️ Pipeline orchestration (future stage)
├── src/
│   ├── __init__.py
│   ├── custom_exception.py         # Unified and detailed exception handling
│   ├── logger.py                   # Centralised logging configuration
│   └── data_processing.py          # 🌦️ End-to-end weather data preparation
├── static/                         # 🌐 Visual assets (optional)
├── templates/                      # 🧩 Placeholder for web/API templates
├── .gitignore                      # 🚫 Git ignore rules
├── .python-version                 # 🐍 Python version pin
├── pyproject.toml                  # ⚙️ Project metadata and uv configuration
├── requirements.txt                # 📦 Python dependencies
├── setup.py                        # 🔧 Editable install support
└── uv.lock                         # 🔒 Locked dependency versions
```

## ⚙️ **How to Run the Data Processing Module**

After activating the virtual environment and ensuring your dataset is located at `artifacts/raw/weather_data.csv`, run:

```bash
python src/data_processing.py
```

### ✅ **Expected Successful Output**

```console
2025-11-08 11:25:55,985 - INFO - Basic data preprocessing completed.
2025-11-08 11:25:56,012 - INFO - Label mapping for Location: {'Adelaide': 0, 'Albury': 1, 'AliceSprings': 2, ...}
2025-11-08 11:25:56,071 - INFO - Label mapping for WindDir9am: {'E': 0, 'ENE': 1, 'ESE': 2, ...}
2025-11-08 11:25:56,123 - INFO - Label mapping for RainToday: {'No': 0, 'Yes': 1}
2025-11-08 11:25:56,155 - INFO - Label mapping for RainTomorrow: {'No': 0, 'Yes': 1}
2025-11-08 11:25:56,155 - INFO - Label encoding completed.
2025-11-08 11:25:56,167 - INFO - Feature columns: ['Location', 'MinTemp', 'MaxTemp', ... 'Month', 'Day']
2025-11-08 11:25:56,243 - INFO - Data split and persistence completed successfully.
2025-11-08 11:25:56,248 - INFO - Data processing completed.
```

This confirms that:

* The raw dataset was successfully read and parsed.
* Missing values were imputed and date features were expanded.
* Categorical columns were encoded into numeric representations.
* Train/test datasets were created and saved under `artifacts/processed/`.

## 🧠 **Implementation Highlights**

* **Integrated Logging** via `src/logger.py`
  Each step logs detailed, timestamped progress messages for full pipeline traceability.

* **Unified Exception Handling** via `src/custom_exception.py`
  Any failure during data loading or transformation raises structured, context-rich errors.

* **Modular, Extensible Design**
  The `DataProcessing` class is importable and designed for integration with later stages — including training, evaluation, and Kubeflow orchestration.

## 🧩 **Integration Guidelines**

| File                      | Purpose                                                      |
| ------------------------- | ------------------------------------------------------------ |
| `src/data_processing.py`  | Executes the weather data preprocessing workflow end-to-end. |
| `src/custom_exception.py` | Provides consistent, traceable error reporting.              |
| `src/logger.py`           | Ensures structured, timestamped logs for reproducibility.    |

✅ **In summary:**
This branch transforms the repository from a static scaffold into a **functional preprocessing stage** for the Weather Prediction pipeline — producing reproducible artefacts, clean datasets, and structured logs that will power the upcoming **model training and evaluation stages**.
