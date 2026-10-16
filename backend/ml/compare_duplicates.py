
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Maternal Health Risk Data Set.csv"

features = [
    "Age", "SystolicBP", "DiastolicBP",
    "BS", "BodyTemp", "HeartRate",
]
target = "RiskLevel"

df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()
df = df[features + [target]].dropna().copy()
df[target] = df[target].str.strip().str.lower()
df = df[df["HeartRate"] > 30].reset_index(drop=True)

versions = {
    "A - Keep duplicates": df.copy(),
    "B - Remove duplicates": df.drop_duplicates().reset_index(drop=True),
}

for name, data in versions.items():
    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )

    train_records = set(
        map(tuple, X_train.to_numpy().tolist())
    )
    test_records = list(
        map(tuple, X_test.to_numpy().tolist())
    )

    overlap = sum(
        record in train_records for record in test_records
    )

    print("Exact test-feature matches in training:", overlap)
    print("Test rows:", len(test_records))


    model = RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"\n{name}")
    print("Rows:", len(data))
    print("Test rows:", len(y_test))
    print(
        "Macro F1:",
        round(
            f1_score(
                y_test,
                predictions,
                average="macro",
                zero_division=0,
            ),
            3,
        ),
    )
    print(
        "Accuracy:",
        round(accuracy_score(y_test, predictions), 3),
    )

# Inspect identical measurements assigned different risk labels
original = pd.read_csv(DATA_FILE)
original.columns = original.columns.str.strip()

features_only = [
    "Age", "SystolicBP", "DiastolicBP",
    "BS", "BodyTemp", "HeartRate",
]

original = original[features_only + ["RiskLevel"]].dropna().copy()
original["RiskLevel"] = original["RiskLevel"].str.strip().str.lower()
original = original[original["HeartRate"] > 30]

label_counts = original.groupby(features_only)["RiskLevel"].nunique()
conflicts = label_counts[label_counts > 1]

print("\nUnique measurement combinations with conflicting labels:", len(conflicts))

if len(conflicts) > 0:
    print("\nExamples of conflicting combinations:")
    print(
        original.set_index(features_only)
        .loc[conflicts.index]
        .groupby(level=list(range(len(features_only))))["RiskLevel"]
        .value_counts()
        .head(20)
        .to_string()
    )

# Count unique feature combinations, ignoring the target label
unique_features = original[features_only].drop_duplicates()

print("\nRows after heart-rate filter:", len(original))
print("Unique feature combinations:", len(unique_features))
print(
    "Repeated feature combinations:",
    len(original) - len(unique_features),
)
print("Conflicting combinations:", len(conflicts))

