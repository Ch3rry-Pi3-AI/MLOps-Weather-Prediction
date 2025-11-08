"""
app.py
======
Flask web app for Weather Prediction (Rain Tomorrow) with a simplified UI.

Overview
--------
This application serves a trained XGBoost model behind a minimal, end-user
interface. Users provide a small set of inputs (Location, Date, MinTemp,
MaxTemp, Humidity3pm, WindSpeed3pm, optional Rainfall), and the app
deterministically infers the remaining model features using season-aware
heuristics before making a prediction.

Design
------
- Minimal inputs for normal users: Location, Date, MinTemp, MaxTemp,
  Humidity3pm, WindSpeed3pm, (optional) Rainfall today.
- Everything else (sunshine, cloud, pressure, wind directions, 9am features,
  Temp3pm, gusts, RainToday boolean) is inferred from the posted inputs.

Notes
-----
- Category encodings (e.g., wind directions, locations, Yes/No) must match
  the encoders used during training.
- The UI is defined in ``templates/index.html`` and uses ``static/style.css``.
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard library imports
# -------------------------------------------------------------------
import datetime as dt
from typing import Any, Dict, List

# -------------------------------------------------------------------
# Third-party imports
# -------------------------------------------------------------------
import joblib
import numpy as np
from flask import Flask, render_template, request

# -------------------------------------------------------------------
# Internal logging/exception setup (fallbacks if not installed)
# -------------------------------------------------------------------
try:
    from src.logger import get_logger
    from src.custom_exception import CustomException

    logger = get_logger(__name__)
except Exception:  # pragma: no cover - defensive fallback if src/* unavailable
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class CustomException(Exception):
        """Fallback CustomException if src modules are not yet available."""
        pass


# -------------------------------------------------------------------
# App & Model
# -------------------------------------------------------------------
# Create Flask application
app = Flask(__name__)

# Path to the trained model artefact
MODEL_PATH: str = "artifacts/models/model.pkl"

# Load model at import time (fail fast if missing)
model = joblib.load(MODEL_PATH)
logger.info("Model loaded from %s", MODEL_PATH)


# -------------------------------------------------------------------
# Encoders / Choices (must match training encodings exactly)
# -------------------------------------------------------------------
WIND_DIRS: List[str] = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
]
WIND_DIR_MAP: Dict[str, int] = {d: i for i, d in enumerate(WIND_DIRS)}

YES_NO_MAP: Dict[str, int] = {"No": 0, "Yes": 1}

LOCATIONS: List[str] = [
    "Adelaide", "Albury", "AliceSprings", "BadgerysCreek", "Ballarat", "Bendigo",
    "Brisbane", "Cairns", "Canberra", "Cobar", "CoffsHarbour", "Dartmoor", "Darwin",
    "GoldCoast", "Hobart", "Katherine", "Launceston", "Melbourne", "MelbourneAirport",
    "Mildura", "Moree", "MountGambier", "MountGinini", "Nhil", "NorahHead",
    "NorfolkIsland", "Nuriootpa", "PearceRAAF", "Penrith", "Perth", "PerthAirport",
    "Portland", "Richmond", "Sale", "SalmonGums", "Sydney", "SydneyAirport",
    "Townsville", "Tuggeranong", "Uluru", "WaggaWagga", "Walpole", "Watsonia",
    "Williamtown", "Witchcliffe", "Wollongong", "Woomera",
]
LOCATION_MAP: Dict[str, int] = {loc: i for i, loc in enumerate(LOCATIONS)}

# Typical prevailing wind direction by broad region (rough defaults; tweak as needed)
PREVAILING_BY_LOCATION: Dict[str, str] = {
    "Sydney": "NE", "SydneyAirport": "NE", "Wollongong": "NE",
    "Melbourne": "SW", "MelbourneAirport": "SW", "Geelong": "SW",
    "Perth": "SW", "PerthAirport": "SW",
    "Brisbane": "SE", "GoldCoast": "SE", "Cairns": "SE", "Townsville": "SE",
    "Hobart": "W", "Launceston": "W",
    "Darwin": "NW", "Katherine": "NW",
}


# -------------------------------------------------------------------
# UI ranges & defaults
# -------------------------------------------------------------------
RANGES: Dict[str, Dict[str, float]] = {
    "MinTemp":      {"min": -10, "max": 45,  "step": 0.1},
    "MaxTemp":      {"min": -10, "max": 50,  "step": 0.1},
    "Rainfall":     {"min": 0,   "max": 200, "step": 0.1},
    "WindSpeed3pm": {"min": 0,   "max": 100, "step": 1},
    "Humidity3pm":  {"min": 0,   "max": 100, "step": 1},
}

DEFAULTS: Dict[str, Any] = {
    "Location": "Sydney",
    "Date": dt.date.today().isoformat(),
    "MinTemp": 13.0,
    "MaxTemp": 23.0,
    "Humidity3pm": 55,
    "WindSpeed3pm": 20,
    "Rainfall": 0.0,  # optional; if > 0.2 → RainToday = Yes
}


# -------------------------------------------------------------------
# Helpers: parsing
# -------------------------------------------------------------------
def _parse_float(name: str, value: str) -> float:
    """
    Convert a posted string value to float.

    Parameters
    ----------
    name : str
        Logical field name for error messages.
    value : str
        Raw posted string value.

    Returns
    -------
    float
        Parsed float value.

    Raises
    ------
    CustomException
        If conversion fails.
    """
    try:
        return float(value)
    except Exception as e:
        raise CustomException(f"{name}: value must be numeric.") from e


def _parse_float_in_range(name: str, value: str, lo: float, hi: float) -> float:
    """
    Parse a float and validate that it lies within [lo, hi].
    """
    x = _parse_float(name, value)
    if x < lo or x > hi:
        raise CustomException(f"{name}: {x} out of range [{lo}, {hi}].")
    return x


def _parse_int_in_range(name: str, value: str, lo: float, hi: float) -> int:
    """
    Parse a float in range and return the rounded integer value.
    """
    x = _parse_float_in_range(name, value, lo, hi)
    return int(round(x))


def _parse_date(value: str) -> dt.date:
    """
    Parse YYYY-MM-DD into a date object.

    Raises
    ------
    CustomException
        If the format is invalid.
    """
    try:
        return dt.date.fromisoformat(value)
    except Exception as e:
        raise CustomException("Date: invalid format (expected YYYY-MM-DD).") from e


# -------------------------------------------------------------------
# Helpers: inference (season/region heuristics)
# -------------------------------------------------------------------
def _season_of(month: int) -> str:
    """
    Map month to season (southern hemisphere).

    Returns
    -------
    str
        One of {'summer','autumn','winter','spring'}.
    """
    if month in (12, 1, 2):
        return "summer"
    if month in (3, 4, 5):
        return "autumn"
    if month in (6, 7, 8):
        return "winter"
    return "spring"


def _prevailing_dir_for_location(loc: str) -> str:
    """
    Get a typical prevailing wind direction for a location.
    """
    return PREVAILING_BY_LOCATION.get(loc, "SW")


def _infer_missing_features(form: Dict[str, str]) -> Dict[str, Any]:
    """
    Infer the full feature vector from minimal inputs.

    Parameters
    ----------
    form : Dict[str, str]
        Posted form dictionary.

    Returns
    -------
    Dict[str, Any]
        Mapping of all model feature names to numeric values, ready to be
        ordered and fed to the model.
    """
    # Parse minimal inputs
    loc = form.get("Location", DEFAULTS["Location"])
    date = _parse_date(form.get("Date", DEFAULTS["Date"]))

    min_temp = _parse_float_in_range(
        "MinTemp", form.get("MinTemp", str(DEFAULTS["MinTemp"])),
        RANGES["MinTemp"]["min"], RANGES["MinTemp"]["max"],
    )
    max_temp = _parse_float_in_range(
        "MaxTemp", form.get("MaxTemp", str(DEFAULTS["MaxTemp"])),
        RANGES["MaxTemp"]["min"], RANGES["MaxTemp"]["max"],
    )
    hum_3pm = _parse_int_in_range(
        "Humidity3pm", form.get("Humidity3pm", str(DEFAULTS["Humidity3pm"])),
        RANGES["Humidity3pm"]["min"], RANGES["Humidity3pm"]["max"],
    )
    spd_3pm = _parse_int_in_range(
        "WindSpeed3pm", form.get("WindSpeed3pm", str(DEFAULTS["WindSpeed3pm"])),
        RANGES["WindSpeed3pm"]["min"], RANGES["WindSpeed3pm"]["max"],
    )
    rainfall = _parse_float_in_range(
        "Rainfall", form.get("Rainfall", str(DEFAULTS["Rainfall"])),
        RANGES["Rainfall"]["min"], RANGES["Rainfall"]["max"],
    )

    # Calendar fields
    year, month, day = date.year, date.month, date.day
    season = _season_of(month)

    # Temperature heuristics
    # 3pm temperature tends towards daily max; lightly season-weighted
    temp3pm = min(max_temp, max(min_temp, (min_temp + 0.7 * max_temp) / 1.7))
    # 9am temperature closer to daily min
    temp9am = max(min_temp, min(max_temp, (0.6 * min_temp + 0.4 * max_temp)))

    # Sunshine hours by season (fallbacks)
    sunshine = {"summer": 9.0, "autumn": 7.0, "winter": 5.0, "spring": 8.0}.get(season, 7.0)

    # Cloud (oktas 0–8) from humidity
    cloud3pm = int(round((hum_3pm / 100.0) * 8))
    cloud3pm = max(0, min(8, cloud3pm))
    cloud9am = cloud3pm

    # Pressure heuristic (hPa): base 1015 − small humidity adjustment
    pressure3pm = float(round(1015.0 - 0.08 * (hum_3pm - 50), 1))
    pressure9am = pressure3pm

    # Wind directions: use prevailing for location
    dir3pm = _prevailing_dir_for_location(loc)
    dir9am = dir3pm
    gust_dir = dir3pm  # preserved for clarity, encoded below

    # Gust speed ≈ 3pm wind + 20, bounded
    gust_speed = int(min(150, max(spd_3pm + 20, spd_3pm)))

    # 9am wind typically a little lighter
    spd_9am = int(max(0, spd_3pm - 3))

    # Evaporation: function of sunshine & diurnal range (empirical)
    evaporation = max(0.0, 0.12 * sunshine + 0.03 * (max_temp - min_temp))

    # RainToday derived from rainfall threshold
    rain_today = "Yes" if rainfall > 0.2 else "No"

    # Encode categoricals to integers matching training
    loc_enc = LOCATION_MAP.get(loc, 0)
    dir3pm_enc = WIND_DIR_MAP.get(dir3pm, WIND_DIR_MAP["SW"])
    dir9am_enc = dir3pm_enc
    gust_dir_enc = dir3pm_enc
    rain_today_enc = YES_NO_MAP[rain_today]

    # Assemble all inferred fields
    return {
        "Location": loc_enc,
        "MinTemp": min_temp,
        "MaxTemp": max_temp,
        "Rainfall": rainfall,
        "Evaporation": evaporation,
        "Sunshine": sunshine,
        "WindGustDir": gust_dir_enc,
        "WindGustSpeed": gust_speed,
        "WindDir9am": dir9am_enc,
        "WindDir3pm": dir3pm_enc,
        "WindSpeed9am": spd_9am,
        "WindSpeed3pm": spd_3pm,
        "Humidity9am": hum_3pm,
        "Humidity3pm": hum_3pm,
        "Pressure9am": pressure9am,
        "Pressure3pm": pressure3pm,
        "Cloud9am": cloud9am,
        "Cloud3pm": cloud3pm,
        "Temp9am": temp9am,
        "Temp3pm": temp3pm,
        "RainToday": rain_today_enc,
        "Year": year,
        "Month": month,
        "Day": day,
    }


def _build_feature_vector_from_inferred(vals: Dict[str, Any]) -> np.ndarray:
    """
    Pack values into the exact training order expected by the model.

    Parameters
    ----------
    vals : Dict[str, Any]
        Dictionary of all model features after inference/encoding.

    Returns
    -------
    np.ndarray
        A single-row 2D array (shape: (1, n_features)).
    """
    ordered = [
        vals["Location"], vals["MinTemp"], vals["MaxTemp"], vals["Rainfall"],
        vals["Evaporation"], vals["Sunshine"], vals["WindGustDir"], vals["WindGustSpeed"],
        vals["WindDir9am"], vals["WindDir3pm"], vals["WindSpeed9am"], vals["WindSpeed3pm"],
        vals["Humidity9am"], vals["Humidity3pm"], vals["Pressure9am"], vals["Pressure3pm"],
        vals["Cloud9am"], vals["Cloud3pm"], vals["Temp9am"], vals["Temp3pm"],
        vals["RainToday"], vals["Year"], vals["Month"], vals["Day"],
    ]
    return np.array([ordered], dtype=float)


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the form (GET) or process a prediction (POST).

    Workflow
    --------
    1) Copy DEFAULTS to preserve UI state.
    2) On POST, parse inputs and infer the remaining features.
    3) Build the ordered feature vector, predict, and render the result.
    """
    prediction: str | None = None
    error: str | None = None

    # Maintain user inputs across requests
    inputs = DEFAULTS.copy()

    if request.method == "POST":
        try:
            # Infer all model features from minimal inputs
            inferred = _infer_missing_features(request.form)

            # Build the single-row feature matrix in training order
            X = _build_feature_vector_from_inferred(inferred)

            # Reflect posted UI values back into the form
            for k in inputs:
                if k in request.form and request.form[k]:
                    inputs[k] = request.form[k]

            # Run model inference
            y_pred = model.predict(X)[0]
            prediction = "Rain Tomorrow: Yes" if int(y_pred) == 1 else "Rain Tomorrow: No"
            logger.info("Prediction successful: %s", prediction)

        except Exception as e:  # keep broad to surface validation errors to UI
            error = str(e)
            logger.error("Prediction failed: %s", error)

    # Render the Jinja template with current state
    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        inputs=inputs,
        ranges=RANGES,
        choices={"locations": LOCATIONS},
    )


# -------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Expose on all interfaces for containerised runs; disable debug in production.
    app.run(host="0.0.0.0", port=5000, debug=True)
