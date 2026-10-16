
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "maternal_risk_model.joblib"

saved = joblib.load(MODEL_FILE)
model = saved["model"]
features = saved["features"]

if not hasattr(model, "feature_importances_"):
    print("This saved model does not provide Random Forest feature importances.")
else:
    importance = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_,
    })

    importance = importance.sort_values(
        "Importance", ascending=False
    ).reset_index(drop=True)

    print("Exploratory feature importance:")
    print(importance.to_string(index=False))
    print("\nThese values describe this model's splits, not medical causation.")
