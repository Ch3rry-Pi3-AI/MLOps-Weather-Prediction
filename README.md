# 🌦️ **MLOps Weather Prediction — End-to-End CI/CD Deployment (GitHub Actions Edition)**

This repository presents a **complete, standalone MLOps workflow** using a **weather dataset** to predict **“Will it rain tomorrow?”**, covering every stage from data preprocessing and model training to full web deployment through an automated **CI/CD (Continuous Integration and Continuous Deployment)** pipeline powered by **GitHub Actions** and deployed on **Google Cloud Platform (GCP)**.

<p align="center">
  <img src="img/flask/flask_app.gif" alt="Deployed Flask Weather Prediction Application" style="width:100%; height:auto;" />
</p>

While the use case — **rainfall prediction** — is conceptually simple, the project’s true focus is to demonstrate a **production-grade MLOps implementation** that brings together automation, containerisation, and cloud deployment via **Google Kubernetes Engine (GKE)**.

## 🧩 **Project Overview**

This project walks through the **entire lifecycle** of a machine learning system — from raw meteorological data to live deployment — within a **modular, reproducible, and cloud-ready architecture**.
Each stage builds upon the previous one to ensure full traceability, consistent execution, and scalability.

### 🌱 **Stage 00 — Project Setup**

A robust foundation was established through a structured repository and environment setup:

* Core directories: `src/`, `pipeline/`, `artifacts/`, and `img/`
* Dependency management using **`uv`** for reproducible environments
* Editable installation via `setup.py`
* Logging and exception-handling utilities to maintain transparency and reliability

This structure ensures clarity, maintainability, and consistency across the entire workflow.

### 🌦️ **Stage 01 — Data Processing**

The **`data_processing.py`** module handled all data preparation tasks:

* Loading and cleaning the weather dataset
* Encoding categorical variables and handling missing values
* Splitting the data into training and test subsets
* Persisting preprocessed artefacts (`X_train.pkl`, `y_test.pkl`, etc.)

Every transformation is reproducible, logged, and ready for integration into automated pipelines.

### 🧠 **Stage 02 — Model Training**

The **`model_training.py`** module trains an **XGBoost classifier** to predict the likelihood of rain the following day.
It includes full evaluation and persistence of model artefacts, generating:

* Accuracy, precision, recall, and F1-score metrics
* A confusion matrix (`confusion_matrix.png`)
* The final trained model (`model.pkl`)

Comprehensive logging and custom exceptions ensure reproducibility and robust error handling.

### ☀️ **Stage 03 — Flask Application**

A **Flask web application** serves the trained model through an intuitive and minimal UI.
Users provide basic weather inputs (Location, Date, MinTemp, MaxTemp, Humidity3pm, WindSpeed3pm, optional Rainfall), and the system **infers remaining features automatically** using season-aware logic.

This stage introduced:

* Interactive UI (`templates/index.html`)
* Polished CSS styling (`static/style.css`)
* A back-end inference engine (`app.py`) for real-time prediction

<p align="center">
  <img src="img/flask/flask_app.png" alt="Flask Weather Prediction Application" style="width:100%; height:auto;" />
</p>

### ⚙️ **Stage 04 — Training Pipeline**

The **`pipeline/training_pipeline.py`** file orchestrates data preprocessing and model training into a single executable workflow.
This modular design allows the entire pipeline to be triggered locally or as part of an automated CI/CD process, bridging local experimentation with cloud deployment.

### ☁️ **Stage 05 — Google Cloud Platform (GCP) Setup**

Infrastructure setup in **Google Cloud Platform** enables seamless cloud integration for containerised machine learning workloads.

Key configurations included:

* Enabling APIs: **Kubernetes Engine**, **Artifact Registry**, and **Compute Engine**
* Creating an **Artifact Registry** (`mlops-weather-prediction`) in `us-central1`
* Setting up a **Service Account** with IAM roles for secure authentication
* Creating a **GKE Autopilot cluster** (`autopilot-cluster-1`) for scalable deployment

This provides the foundation for continuous deployment and scalable retraining workflows.

### 🚀 **Stage 06 — CI/CD Deployment (GitHub Actions → GCP)**

The final stage integrates **GitHub Actions** for continuous delivery.
Each push to the `main` branch triggers a full pipeline defined in **`.github/workflows/deploy.yml`**, automating build, test, and deployment.

**Pipeline sequence:**

1. **Build** — Package the Flask app into a Docker image using the `Dockerfile`
2. **Push** — Upload the image to **Google Artifact Registry**
3. **Deploy** — Apply `kubernetes-deployment.yaml` to the **GKE Autopilot cluster**

The pipeline leverages official **`google-github-actions`** integrations for authentication, image management, and deployment.

<p align="center">
  <img src="img/github_actions/workflow_success.png" alt="GitHub Actions Workflow Success" style="width:100%; height:auto;" />
</p>

Once completed, the application becomes live and publicly accessible via a **GKE LoadBalancer endpoint**.

## 💡 **Why GitHub Actions?**

GitHub Actions provides a seamless, cloud-native automation experience — perfect for MLOps pipelines.

### ✅ **Key Advantages**

* **Native GitHub integration** — workflows trigger automatically on push or PR
* **Simple YAML configuration** under `.github/workflows/`
* **Secure secret management** for GCP credentials
* **Official support** for Google Cloud authentication and deployments
* **Zero server management** — runs on hosted runners
* **Fast, scalable execution** suitable for both training and deployment workflows

GitHub Actions unifies version control, CI/CD, and automation in a single platform — making it ideal for this project’s end-to-end workflow.

## 🗂️ **Final Project Structure**

```text
mlops_weather_prediction/
├── .venv/                          # 🧩 Local virtual environment (created by uv)
├── artifacts/                      # 💾 Raw, processed, and model artefacts
│   ├── raw/
│   ├── processed/
│   └── models/
├── pipeline/
│   └── training_pipeline.py         # Unified orchestration of preprocessing + training
├── src/
│   ├── data_processing.py
│   ├── model_training.py
│   ├── logger.py
│   └── custom_exception.py
├── templates/
│   └── index.html                   # Flask UI
├── static/
│   ├── style.css
│   └── img/app_background.jpg
├── img/
│   ├── flask/flask_app.gif          # Animated Flask app demo
│   ├── github_actions/              # Screenshots for GitHub Actions + GCP setup
│   └── gcp/
├── Dockerfile                       # 🐳 Container image definition
├── kubernetes-deployment.yaml       # ☸️ Kubernetes deployment configuration
├── .github/
│   └── workflows/
│       └── deploy.yml               # ⚙️ GitHub Actions CI/CD workflow
├── app.py                           # Flask application entry point
├── pyproject.toml                   # Project metadata and dependencies
├── setup.py                         # Editable install configuration
└── requirements.txt                 # Python dependencies
```

## 🌐 **End-to-End Workflow Summary**

1. **Data Processing** → clean, encode, and split the dataset
2. **Model Training** → train and evaluate the XGBoost classifier
3. **Flask App** → deploy an interactive prediction interface
4. **Pipeline Orchestration** → automate preprocessing + training
5. **GCP Setup** → configure cluster, registry, and IAM permissions
6. **CI/CD Deployment** → automate build → push → deploy via GitHub Actions

## ✅ **In Summary**

This standalone project transforms a straightforward **weather classification problem** into a **complete, automated MLOps workflow** using **GitHub Actions** and **Google Cloud Platform**.
It demonstrates how a traditional ML pipeline — data, model, and application — can be **operationalised end-to-end**, resulting in a **scalable, reproducible, and production-ready cloud deployment** triggered automatically with every code push.
