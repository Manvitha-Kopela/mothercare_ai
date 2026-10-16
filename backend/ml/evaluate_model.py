
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Maternal Health Risk Data Set.csv"

features = [
    "Age",
    "SystolicBP",
    "DiastolicBP",
    "BS",
    "BodyTemp",
    "HeartRate",
]
target = "RiskLevel"

# Load the original data without modifying the CSV
df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()
df = df[features + [target]].dropna().copy()
df[target] = df[target].str.strip().str.lower()

# Preserve the current project's documented cleaning choice
df = df[df["HeartRate"] > 30].copy()

print("Rows after heart-rate filter:", len(df))

# Remove only exact duplicate rows, including the label
df = df.drop_duplicates().reset_index(drop=True)

print("Rows after exact duplicate removal:", len(df))
print("\nClass counts:")
print(df[target].value_counts())

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)

print("\nTraining rows:", len(X_train))
print("Test rows:", len(X_test))

model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("\nHeld-out test classification report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=["low risk", "mid risk", "high risk"],
        zero_division=0,
    )
)

print(
    "\nEvaluation limitation: records have no patient identifiers, "
    "so this split cannot guarantee independence between people."
)
print("Academic prototype only; not clinically validated.")
