
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Maternal Health Risk Data Set.csv"
MODEL_FILE = BASE_DIR / "maternal_risk_model.joblib"

# 1. Load and validate the dataset
df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()

target = "RiskLevel"
required_columns = {
    "Age", "SystolicBP", "DiastolicBP",
    "BS", "BodyTemp", "HeartRate", target,
}

missing = required_columns - set(df.columns)
if missing:
    raise ValueError(f"Dataset is missing columns: {sorted(missing)}")

df = df[list(required_columns)].copy()
df = df.dropna()

print("Original valid rows:", len(df))
print("Duplicate rows:", int(df.duplicated().sum()))

# Remove exact duplicates before splitting
df = df.drop_duplicates().reset_index(drop=True)

# Exclude the clearly implausible heart-rate entries identified
# during data inspection; document this cleaning decision.
df = df[df["HeartRate"] > 30].reset_index(drop=True)

# 2. Basic data checks
features = [
    "Age", "SystolicBP", "DiastolicBP",
    "BS", "BodyTemp", "HeartRate",
]

if not set(df[target].unique()).issubset(
    {"low risk", "mid risk", "high risk"}
):
    raise ValueError(
        "Unexpected RiskLevel labels: "
        f"{sorted(df[target].unique())}"
    )

X = df[features]
y = df[target].str.strip().str.lower()

print("\nRows after duplicate removal:", len(df))
print("\nClass counts:")
print(y.value_counts())

# 3. Hold out a test set
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)


# 4. Define both models
models = {
    "Logistic Regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=42,
        ),
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
    ),
}

# Cross-validate on training data only
smallest_class = int(y_train.value_counts().min())
if smallest_class < 2:
    raise ValueError("Too few training examples in a class.")

folds = min(5, smallest_class)
cv = StratifiedKFold(
    n_splits=folds, shuffle=True, random_state=42
)

# 5. Compare models
best_model = None
best_score = -1.0

for name, candidate in models.items():
    scores = cross_val_score(
        candidate,
        X_train,
        y_train,
        cv=cv,
        scoring="f1_macro",
    )

    print(
        f"\n{name} cross-validation macro F1: "
        f"{scores.mean():.3f} +/- {scores.std():.3f}"
    )

    if scores.mean() > best_score:
        best_score = scores.mean()
        best_model = candidate

# Evaluate the selected model once on the held-out test set
best_model.fit(X_train, y_train)
predictions = best_model.predict(X_test)

print("\nSelected model:", type(best_model).__name__)
print("\nHeld-out test classification report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=["low risk", "mid risk", "high risk"],
        zero_division=0,
    )
)

model = best_model


# 6. Save model and expected input order
joblib.dump(
    {"model": model, "features": features},
    MODEL_FILE,
)
print(f"\nModel saved to: {MODEL_FILE}")
print("Prototype only; not clinically validated.")
