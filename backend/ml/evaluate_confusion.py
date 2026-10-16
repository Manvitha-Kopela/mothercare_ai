
from pathlib import Path

import pandas as pd
import joblib
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Maternal Health Risk Data Set.csv"
MODEL_FILE = BASE_DIR / "maternal_risk_model.joblib"

features = [
    "Age", "SystolicBP", "DiastolicBP",
    "BS", "BodyTemp", "HeartRate",
]
classes = ["low risk", "mid risk", "high risk"]

df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()
df = df[features + ["RiskLevel"]].dropna().copy()
df["RiskLevel"] = df["RiskLevel"].str.strip().str.lower()
df = df[df["HeartRate"] > 30].drop_duplicates().reset_index(drop=True)

X = df[features]
y = df["RiskLevel"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

saved = joblib.load(MODEL_FILE)
model = saved["model"]

predictions = model.predict(X_test)

print("\nClassification report:")
print(classification_report(
    y_test, predictions, labels=classes, zero_division=0
))

matrix = confusion_matrix(y_test, predictions, labels=classes)
print("\nConfusion matrix (rows = actual, columns = predicted):")
print(pd.DataFrame(
    matrix,
    index=[f"Actual {c}" for c in classes],
    columns=[f"Predicted {c}" for c in classes],
))

print("\nResearch prototype only; not clinically validated.")
