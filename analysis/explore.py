import pandas as pd

path = "../data/results.csv"
df = pd.read_csv(path, low_memory=False)

print("=== Shape ===")
print(df.shape)

print("\n=== Mean / median JobSat by AISelect ===")
print(df.groupby("AISelect")["JobSat"].agg(["count", "mean", "median", "std"]))

print("\n=== Mean / median JobSat by DevType (top 10 by count) ===")
top_devtypes = df["DevType"].value_counts().head(10).index
sub = df[df["DevType"].isin(top_devtypes)]
print(sub.groupby("DevType")["JobSat"].agg(["count", "mean", "median", "std"]).sort_values("count", ascending=False))

print("\n=== WorkExp by AISelect ===")
print(df.groupby("AISelect")["WorkExp"].agg(["count", "mean", "median"]))

print("\n=== Correlation matrix (numeric) ===")
num_cols = ["JobSat", "WorkExp", "ConvertedCompYearly"]
print(df[num_cols].apply(pd.to_numeric, errors="coerce").corr())

print("\n=== ConvertedCompYearly describe (raw) ===")
comp = pd.to_numeric(df["ConvertedCompYearly"], errors="coerce")
print(comp.describe())
print("missing pct:", comp.isna().mean())

print("\n=== Complete-case size on the four key analysis variables ===")
key = df[["AISelect", "JobSat", "WorkExp", "DevType"]]
complete = key.dropna()
print("Full N:", len(df), "Complete-case N:", len(complete), "Retention:", len(complete) / len(df))

print("\n=== Country top 10 ===")
print(df["Country"].value_counts().head(10))

print("\n=== RemoteWork distribution ===")
print(df["RemoteWork"].value_counts(dropna=False))
