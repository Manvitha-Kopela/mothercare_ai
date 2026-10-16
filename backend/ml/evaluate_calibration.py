
from pathlib import Path

import joblib
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import log_loss
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

probabilities = model.predict_proba(X_test)
model_classes = list(model.classes_)

# Align probability columns to the expected class order.
prob_df = pd.DataFrame(probabilities, columns=model_classes)
prob_df = prob_df.reindex(columns=classes, fill_value=0.0)
probabilities = prob_df.to_numpy()

y_true = y_test.to_numpy()
y_onehot = pd.get_dummies(
    pd.Categorical(y_true, categories=classes)
).to_numpy()

print("Multiclass log loss (lower is better):")

metric_classes = sorted(classes)
metric_probabilities = prob_df.reindex(
    columns=metric_classes,
    fill_value=0.0,
).to_numpy()

print(round(
    log_loss(
        y_true,
        metric_probabilities,
        labels=metric_classes,
    ),
    4,
))

print("\nMean predicted probability vs observed frequency")
print("(One-vs-rest, using 5 bins where possible):")

for i, label in enumerate(classes):
    observed = (y_true == label).astype(int)
    predicted = probabilities[:, i]

    fraction_positive, mean_predicted = calibration_curve(
        observed,
        predicted,
        n_bins=5,
        strategy="quantile",
    )

    print(f"\n{label}:")
    for mean_p, observed_p in zip(mean_predicted, fraction_positive):
        print(
            f"  Mean predicted={mean_p:.3f}, "
            f"Observed frequency={observed_p:.3f}"
        )

print(
    "\nResearch diagnostic only. Small test set and dataset limitations "
    "mean these results do not establish clinical calibration."
)
