
from pathlib import Path

import joblib
import pandas as pd


# The trained model is stored in backend/ml/
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_FILE = BASE_DIR / "ml" / "maternal_risk_model.joblib"

_saved_model = None


def load_model():
    """Load the saved model once, when first needed."""
    global _saved_model

    if _saved_model is None:
        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Trained model file not found: {MODEL_FILE}"
            )
        _saved_model = joblib.load(MODEL_FILE)

    return _saved_model


def predict_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    """Return an experimental ML prediction for software testing."""
    saved = load_model()
    model = saved["model"]
    features = saved["features"]

    sample = pd.DataFrame(
        [[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]],
        columns=[
            "Age",
            "SystolicBP",
            "DiastolicBP",
            "BS",
            "BodyTemp",
            "HeartRate",
        ],
    )

    predicted_class = model.predict(sample)[0]
    probabilities = model.predict_proba(sample)[0]

    return {
        "predicted_class": str(predicted_class),
        "probability_estimates": {
            str(label): round(float(probability), 4)
            for label, probability in zip(model.classes_, probabilities)
        },
        "model_features": features,
        "model_version": "experimental",
        "clinical_validation": False,
        "disclaimer": (
            "Research prototype only. This prediction is not a diagnosis "
            "and must not be used to make patient-care or referral decisions."
        ),
    }
