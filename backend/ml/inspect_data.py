
from pathlib import Path
import pandas as pd

data_file = (
    Path(__file__).resolve().parent
    / "Maternal Health Risk Data Set.csv"
)

df = pd.read_csv(data_file)
df.columns = df.columns.str.strip()

print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isna().sum())

print("\nMeasurement summary:")
print(df.describe().round(2).to_string())

print("\nHeart-rate values at or below 30:")
print(df.loc[df["HeartRate"] <= 30].to_string(index=False))

print("\nRisk-level counts:")
print(df["RiskLevel"].value_counts(dropna=False))

# Check how often each exact measurement-and-label combination occurs
print("\nMost frequent repeated records:")
print(
    df.value_counts()
    .head(10)
    .to_string()
)

# Count duplicate records separately for each risk class
print("\nDuplicate rows by risk level:")
print(
    df[df.duplicated(keep="first")]["RiskLevel"]
    .value_counts()
    .to_string()
)
