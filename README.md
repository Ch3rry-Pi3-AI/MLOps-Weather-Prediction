
# 🌸 **MLOps Iris Classifier — End-to-End CI/CD Deployment (GitHub Actions Edition)**

This repository demonstrates a **complete MLOps workflow** using the classic **Iris dataset**, progressing from data preprocessing and model training to full web deployment through an automated **CI/CD (Continuous Integration and Continuous Deployment)** pipeline built with **GitHub Actions** and deployed to **Google Cloud Platform (GCP)**.

<p align="center">
  <img src="img/flask/flask_app.gif" alt="Deployed Flask Iris Classifier Application" style="width:100%; height:auto;" />
</p>

While the machine learning use case — **Iris species classification** — is intentionally simple, the project’s main objective is to showcase a **production-grade MLOps workflow** using **GitHub Actions** for automation, containerisation, and cloud deployment via **Google Kubernetes Engine (GKE)**.

## 🧩 **Project Overview**

This project walks through the **entire lifecycle** of a machine learning system — from raw data to live deployment — using a modular, reproducible, and scalable architecture.
Each stage builds on the previous one, ensuring consistent execution and traceability throughout the pipeline.

### 🌱 **Stage 00 — Project Setup**

A structured repository layout was established, introducing:

* Core directories: `src/`, `pipeline/`, `artifacts/`, and `img/`
* Dependency management with **`uv`** for reproducible environments
* Editable package installation via `setup.py`
* Logging and exception-handling frameworks for traceable experimentation

This created the foundation for the remaining stages.

### 💾 **Stage 01 — Data Processing**

The **`data_processing.py`** module handled the complete preprocessing workflow:

* Loading and cleaning the Iris dataset
* Handling outliers and missing values
* Splitting data into training and test sets
* Persisting processed artefacts (`X_train.pkl`, `y_test.pkl`, etc.)

All transformations were reproducible and logged to ensure consistent results.

### 🧠 **Stage 02 — Model Training**

The **`model_training.py`** module trained a **Decision Tree Classifier** and performed model evaluation, generating key metrics:

* Accuracy, precision, recall, and F1-score
* A confusion matrix (`confusion_matrix.png`)
* A serialised model file (`model.pkl`)

Exception handling and centralised logging ensured reliability during training.

### 🌸 **Stage 03 — Flask Application**

A **Flask web interface** was built to deploy the trained model as an interactive web app.
Users can input sepal and petal dimensions and receive predictions in real time.

This stage introduced:

* A responsive HTML front-end (`templates/index.html`)
* CSS styling (`static/style.css`)
* Flask integration via `app.py` for live inference

<p align="center">
  <img src="img/flask/flask_app.png" alt="Flask Iris Classifier Application" style="width:100%; height:auto;" />
</p>

### ⚙️ **Stage 04 — Training Pipeline**

The **`pipeline/training_pipeline.py`** script unified **data processing** and **model training** into a single orchestrated pipeline, automating every key step.

It provides a reproducible execution workflow that can be triggered locally or by external automation tools (e.g. CI/CD).
This was the bridge between local experimentation and cloud automation.

### ☁️ **Stage 05 — Google Cloud Platform (GCP) Setup**

The cloud infrastructure was configured within **Google Cloud Platform** to support containerised ML workloads.

Key setup tasks included:

* Enabling APIs for **Kubernetes Engine**, **Artifact Registry**, and **Compute Engine**
* Creating an **Artifact Registry** repository (`mlops-iris-iii`) in `us-central1`
* Generating a **Service Account** with roles for Artifact Registry and Kubernetes deployment
* Creating a **GKE Autopilot cluster** (`autopilot-cluster-1`) for managed workloads

This established the secure, scalable backbone for automated deployment.

### 🚀 **Stage 06 — CI/CD Deployment (GitHub Actions → GCP)**

Finally, the project integrated **GitHub Actions** to automate the build-and-deploy workflow.
Each push to the `main` branch triggers the pipeline defined in **`.github/workflows/deploy.yml`**.

The CI/CD sequence:

1. **Build** — Create a Docker image for the Flask app using the `Dockerfile`
2. **Push** — Upload the image to **Google Artifact Registry**
3. **Deploy** — Apply `kubernetes-deployment.yaml` to **GKE** to update the live application

The pipeline uses the official **`google-github-actions`** modules for authentication, image management, and Kubernetes deployment.

<p align="center">
  <img src="img/github_actions/workflow_success.png" alt="GitHub Actions Workflow Success" style="width:100%; height:auto;" />
</p>

Once completed, the application becomes publicly available through the external **LoadBalancer endpoint** exposed by GKE.

## 💡 **Why GitHub Actions?**

GitHub Actions was chosen for its **tight integration**, **ease of setup**, and **robust cloud support**.

### ✅ **Key Advantages**

* **Native integration** — workflows trigger automatically on push or pull requests
* **Simple YAML configuration** stored under `.github/workflows/`
* **Secure secret management** through repository settings
* **First-class GCP support** with official authentication actions
* **Zero-infrastructure overhead** — runs on GitHub-hosted runners
* **Fast, scalable execution** — ideal for iterative machine learning workflows

These features make **GitHub Actions** a clean, lightweight, and powerful choice for modern CI/CD in MLOps.

## 🗂️ **Final Project Structure**

```text
mlops_iris_classifier/
├── .venv/                          # 🧩 Local virtual environment (created by uv)
├── artifacts/                      # 💾 Raw, processed, and model artefacts
│   ├── raw/
│   ├── processed/
│   └── models/
├── pipeline/
│   └── training_pipeline.py         # Unified data processing + model training
├── src/
│   ├── data_processing.py
│   ├── model_training.py
│   ├── logger.py
│   └── custom_exception.py
├── templates/
│   └── index.html                  # Flask UI
├── static/
│   ├── style.css
│   └── img/app_background.jpg
├── img/
│   ├── flask/flask_app.gif         # Animated Flask app demo
│   ├── github_actions/             # Screenshots for GitHub + GCP setup
│   └── gcp/
├── Dockerfile                      # 🐳 Container image definition
├── kubernetes-deployment.yaml      # ☸️ Kubernetes deployment specification
├── .github/
│   └── workflows/
│       └── deploy.yml              # ⚙️ GitHub Actions CI/CD pipeline
├── app.py                          # Flask application entry point
├── pyproject.toml                  # Project metadata and dependencies
├── setup.py                        # Editable install support
└── requirements.txt                # Python dependencies
```

## 🌐 **End-to-End Workflow Summary**

1. **Data Processing** → clean, split, and persist artefacts
2. **Model Training** → train and evaluate the Decision Tree Classifier
3. **Flask Application** → serve predictions via web interface
4. **Pipeline Orchestration** → unify preprocessing + training
5. **GCP Setup** → configure cluster, registry, and permissions
6. **CI/CD Deployment** → automate build → push → deploy to GKE

## ✅ **In Summary**

This project transforms a simple Iris classification task into a **fully automated MLOps pipeline** using **GitHub Actions** and **Google Cloud Platform**.
It demonstrates how to take a traditional ML workflow — data, model, and app — and operationalise it through a reproducible, cloud-native CI/CD system that delivers scalable, production-ready deployments with every code push.