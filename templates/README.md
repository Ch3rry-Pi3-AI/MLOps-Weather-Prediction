# 🖼️ `templates/index.html` — Weather Prediction Frontend Interface

This HTML template defines the **user-facing interface** for the **Weather Prediction Flask web application**.
It enables users to enter a few weather observations and receive a machine learning–based prediction of whether it will **rain tomorrow**.

The design is intentionally **minimalist and guided**, with **smart defaults** inferred on the backend to reduce input complexity for non-technical users.

## 🎯 Purpose

The page acts as the **primary user interface** for interacting with the trained weather model.
It collects only a small number of key features, while other required model inputs (e.g., sunshine hours, cloud cover, wind direction, pressure, and morning observations) are inferred automatically by the Flask backend logic.

Users can:

* Select a **location** and **date**
* Enter basic observations like **temperature**, **humidity**, **wind speed**, and **rainfall**
* Submit the form to obtain a prediction about rainfall tomorrow

## 🧩 Structure Overview

| Section   | Description                                                                                            |
| :-------- | :----------------------------------------------------------------------------------------------------- |
| `<head>`  | Metadata, Google Fonts, external stylesheet (`style.css`), and background image injection.             |
| `<body>`  | Contains the main app layout: a background overlay, header, guidance cards, form, and output section.  |
| `.stats`  | A pair of cards providing quick reference on units and “smart defaults”.                               |
| `<form>`  | The input grid for user interaction; all values are dynamically rendered from Flask context variables. |
| `.result` | Displays the model’s prediction (e.g., “Rain Tomorrow: Yes”).                                          |

## 🗂️ File Location

```
project_root/
├── app.py                     # Flask backend (serves predictions)
├── static/
│   ├── style.css              # Stylesheet defining layout and theme
│   └── img/
│       └── app_background.jpg # Subtle background image
└── templates/
    └── index.html             # This file (frontend template)
```

## ⚙️ Context Variables from Flask

This template is rendered via `render_template("index.html", ...)` in `app.py`.
It expects the following variables to be passed from the Flask context:

| Variable     | Type   | Purpose                                                    |
| :----------- | :----- | :--------------------------------------------------------- |
| `inputs`     | `dict` | Prefilled values for form persistence and defaults.        |
| `ranges`     | `dict` | Range constraints for numeric fields (min, max, step).     |
| `choices`    | `dict` | Option lists for select menus (e.g., available locations). |
| `prediction` | `str`  | Text of model output, displayed after submission.          |
| `error`      | `str`  | Error message shown in red alert box, if applicable.       |

### Example Context in `app.py`

```python
return render_template(
    "index.html",
    prediction=prediction,
    error=error,
    inputs={
        "Location": "Sydney",
        "Date": "2025-11-08",
        "MinTemp": 13.0,
        "MaxTemp": 23.0,
        "Humidity3pm": 55,
        "WindSpeed3pm": 20,
        "Rainfall": 0.0
    },
    ranges={
        "MinTemp": {"min": -10, "max": 45, "step": 0.1},
        "MaxTemp": {"min": -10, "max": 50, "step": 0.1},
        "Humidity3pm": {"min": 0, "max": 100, "step": 1},
        "WindSpeed3pm": {"min": 0, "max": 100, "step": 1},
        "Rainfall": {"min": 0, "max": 200, "step": 0.1},
    },
    choices={"locations": ["Sydney", "Melbourne", "Perth", "Darwin"]},
)
```

## 🧠 Design Features

* **📋 Guided Simplicity**
  The form uses intuitive labels, placeholders, and unit hints to ensure non-technical users can provide realistic inputs.

* **🎨 Clean Visuals**
  The `static/style.css` file defines a modern card layout with rounded edges, shadows, and balanced whitespace.
  The background image (`app_background.jpg`) is faded using a translucent overlay for subtle depth.

* **🧮 Smart Defaults**
  Users only enter essential features. The backend automatically infers all other model-required variables:

  * Cloud cover estimated from humidity
  * Wind direction and pressure based on typical patterns
  * `RainToday` derived from rainfall threshold (> 0.2 mm)
  * Temperature relationships used to derive morning and afternoon values

* **🧾 Responsive Layout**
  The `form-grid` and `stats-grid` use CSS grid with a two-column layout on desktop and a single-column layout on smaller screens.

## 🚀 How to Use

1. Ensure your Flask application is running (e.g., `python app.py`).
2. Open a browser and visit `http://127.0.0.1:5000/`.
3. Select a **location** and **date**.
4. Enter the observed values for:

   * Minimum temperature
   * Maximum temperature
   * Humidity (3pm)
   * Wind speed (3pm)
   * Optional rainfall today
5. Click **“Predict Rain Tomorrow”**.
6. The model will return the prediction (e.g., “Rain Tomorrow: Yes”).

## 🧩 Integration with Backend

| Component    | Function                                                                                                                  |
| :----------- | :------------------------------------------------------------------------------------------------------------------------ |
| `app.py`     | Loads the XGBoost model, processes user inputs, infers additional features, and sends prediction results to the template. |
| `index.html` | Renders the interface and displays predictions and errors.                                                                |
| `style.css`  | Provides the visual styling and layout structure.                                                                         |

## ✅ Example Output

```
Prediction: Rain Tomorrow: Yes
```

When submitted, the page dynamically updates to display the result below the form.

## 💡 Developer Notes

* This file uses **Jinja2 templating syntax** (`{{ ... }}` and `{% ... %}`) for Flask variable injection and control structures.
* Ensure the `templates/` folder is located at the same level as your Flask app file (`app.py`).
* The `novalidate` attribute on the form disables native browser validation, allowing Flask to handle all validation server-side.
