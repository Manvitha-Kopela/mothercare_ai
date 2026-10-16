
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "maternal_risk_model.joblib"

saved = joblib.load(MODEL_FILE)
model = saved["model"]
features = saved["features"]

# Synthetic example for software testing only—not a real patient.
sample = pd.DataFrame(
    [[25, 120, 80, 7.0, 98.6, 75]],
    columns=features,
)

predicted_class = model.predict(sample)[0]

print("Synthetic input:")
print(sample.to_string(index=False))
print("\nPredicted class:", predicted_class)

if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(sample)[0]
    print("\nModel probability estimates:")
    for label, probability in zip(model.classes_, probabilities):
        print(f"{label}: {probability:.3f}")

print("\nSoftware test only—not a medical assessment.")
