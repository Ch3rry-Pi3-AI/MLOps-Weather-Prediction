# 🌤️ **Flask Web Application — MLOps Weather Prediction**

This branch extends the **MLOps Weather Prediction** project into its **fourth stage**, introducing a fully interactive **Flask web application** for **inference and model serving**.
Users can now interact with the trained weather prediction model via a **simple, intuitive interface** that estimates **whether it will rain tomorrow** based on a few daily observations.

## 🧠 **Overview**

The **Flask application** acts as the **inference layer** of the MLOps pipeline.
It connects the trained XGBoost model (saved under `artifacts/models/model.pkl`) to an easy-to-use web frontend, enabling real-time predictions through a clean and responsive UI.

The system is designed with **non-technical users** in mind — only essential inputs (like temperature, humidity, and wind) are required, while all other meteorological features are **intelligently inferred** under the hood.

### 🔍 Core Responsibilities

| Stage | Component           | Description                                                              |
| ----: | ------------------- | ------------------------------------------------------------------------ |
|   1️⃣ | **Frontend (UI)**   | Interactive form built with HTML/CSS (Poppins theme, responsive grid).   |
|   2️⃣ | **Backend (Flask)** | Handles routing, form validation, and feature inference logic.           |
|   3️⃣ | **Model Inference** | Loads the pre-trained XGBoost model to predict “Rain Tomorrow” (Yes/No). |
|   4️⃣ | **Result Display**  | Renders human-readable prediction output in a styled result card.        |

## 🗂️ **Updated Project Structure**

```text
mlops_weather_prediction/
├── artifacts/
│   ├── raw/                       # 🌦️ Input dataset
│   ├── processed/                 # 💾 Preprocessed train/test data
│   └── models/
│       └── model.pkl              # 🧠 Trained XGBoost model used for inference
├── pipeline/
│   └── training_pipeline.py       # 🔄 Orchestrates full preprocessing + training workflow
├── src/
│   ├── data_processing.py         # 🌦️ Data preparation logic
│   ├── model_training.py          # ⚙️ Model training and evaluation
│   ├── logger.py                  # 🪵 Centralised logging
│   └── custom_exception.py        # ⚠️ Structured error handling
├── templates/
│   └── index.html                 # 🧩 Frontend page with input form and result display
├── static/
│   ├── style.css                  # 🎨 Styling for the web interface
│   └── img/
│       └── app_background.jpg     # 🌅 Background image (lightly faded overlay)
├── app.py                         # 🚀 Flask application (inference serving entrypoint)
├── requirements.txt               # 📦 Project dependencies
└── pyproject.toml                 # ⚙️ Project metadata and uv configuration
```

## ⚙️ **How to Run the Flask Application**

Make sure the trained model (`model.pkl`) exists in `artifacts/models/`, then run:

```bash
python app.py
```

By default, the app runs locally at:

> 🌐 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

To expose it for containerised or cloud testing, use:

```bash
python app.py --host=0.0.0.0
```

### ✅ **Expected Runtime Output**

```console
2025-11-08 14:02:37,120 - INFO - Model loaded from artifacts/models/model.pkl
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
127.0.0.1 - - [08/Nov/2025 14:02:58] "POST / HTTP/1.1" 200 -
2025-11-08 14:02:58,441 - INFO - Prediction successful: Rain Tomorrow: No
```

## 🧩 **User Interface Overview**

| Section             | Description                                                                                                                     |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| **Header**          | Displays project title and short subtitle guiding the user.                                                                     |
| **Guidance Cards**  | Compact cards showing measurement units, value ranges, and notes about smart defaults.                                          |
| **Input Form**      | Users provide minimal inputs: `Location`, `Date`, `MinTemp`, `MaxTemp`, `Humidity3pm`, `WindSpeed3pm`, and optional `Rainfall`. |
| **Prediction Card** | Shows model output — “Rain Tomorrow: Yes” or “Rain Tomorrow: No” — styled with green or red accents.                            |

### 💡 Smart Inference Behaviour

The app **automatically infers** missing features like:

* 🌞 **Sunshine hours**, ☁️ **Cloud cover**, 💨 **Wind direction**, and 📈 **Pressure**
* 🕘 Morning/afternoon temperatures (`Temp9am`, `Temp3pm`)
* 🌦️ `RainToday` boolean based on rainfall threshold (`> 0.2 mm`)

This makes the interface lightweight and user-friendly without compromising prediction accuracy.

## 🧠 **Implementation Highlights**

* **End-to-End Integration:**
  Connects the trained model directly to the Flask UI for live inference.

* **Simplified User Inputs:**
  Only key parameters are required; all other model features are inferred programmatically.

* **Modern Design:**
  The UI (`templates/index.html`) and stylesheet (`static/style.css`) create a clean, mobile-responsive interface using CSS Grid and variable-driven theming.

* **Robust Backend Logic:**
  The backend performs:

  * Input validation (type + range)
  * Feature inference (season-aware)
  * Logging and exception handling for transparency

* **Portable Deployment:**
  Can be run locally, in Docker, or deployed to a cloud platform (e.g. GCP, AWS, Render).

## 🧩 **Integration Overview**

| File                         | Purpose                                                                         |
| :--------------------------- | :------------------------------------------------------------------------------ |
| `app.py`                     | Hosts the Flask app, routes requests, validates input, and handles predictions. |
| `templates/index.html`       | Defines the frontend interface and Jinja2 placeholders for data binding.        |
| `static/style.css`           | Provides theming, responsive layout, and UX enhancements.                       |
| `artifacts/models/model.pkl` | Serialized XGBoost model loaded for prediction.                                 |
| `src/logger.py`              | Logs runtime activity and errors for traceability.                              |
| `src/custom_exception.py`    | Handles validation and inference exceptions with detailed context.              |

## ✅ **In summary**

This branch transforms the **MLOps Weather Prediction** project from a trained model into a **fully interactive, production-ready web application**.

It enables end-users to:

* Select their location and provide a few observations
* Instantly receive an AI-driven weather prediction
* Experience a clean, responsive UI powered by Flask

With this stage complete, the project now supports **end-to-end model inference**, marking the transition from experimentation to **user-facing deployment**.
