"""
Analysis for the toy paper: AI-tool adoption and job satisfaction,
Stack Overflow Annual Developer Survey.

Produces:
  - analysis/results_table.csv     (regression coefficients, for the LaTeX table)
  - analysis/descriptive_table.csv (group means/medians, for the LaTeX table)
  - paper/figures/fig1_satisfaction_by_ai_use.pdf
  - paper/figures/fig2_years_experience.pdf

Does not fabricate numbers: every figure used in the paper is read back out
of these two CSVs.
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = "../data/results.csv"
FIG_DIR = "../paper/figures"

df = pd.read_csv(DATA, low_memory=False)
n_raw = len(df)

# --- Build analysis variables -------------------------------------------------

ai_user_map = {
    "Yes, I use AI tools daily": 1,
    "Yes, I use AI tools weekly": 1,
    "Yes, I use AI tools monthly or infrequently": 1,
    "No, and I don't plan to": 0,
    "No, but I plan to soon": 0,
}
df["ai_user"] = df["AISelect"].map(ai_user_map)

top_devtypes = df["DevType"].value_counts().head(10).index
df["devtype_grp"] = np.where(df["DevType"].isin(top_devtypes), df["DevType"], "Other")
df.loc[df["DevType"].isna(), "devtype_grp"] = np.nan

df["work_exp"] = pd.to_numeric(df["WorkExp"], errors="coerce")
df["job_sat"] = pd.to_numeric(df["JobSat"], errors="coerce")

analysis = df.dropna(subset=["ai_user", "job_sat", "work_exp", "devtype_grp"]).copy()
n_analysis = len(analysis)

print(f"Raw N: {n_raw}, analysis-frame N: {n_analysis} ({n_analysis/n_raw:.1%})")

# --- Descriptive table: JobSat by AI-use intensity (full categories) ----------

intensity_order = [
    "No, and I don't plan to",
    "No, but I plan to soon",
    "Yes, I use AI tools monthly or infrequently",
    "Yes, I use AI tools weekly",
    "Yes, I use AI tools daily",
]
desc = (
    df.groupby("AISelect")["job_sat"]
    .agg(n="count", mean="mean", median="median", sd="std")
    .reindex(intensity_order)
    .reset_index()
)
desc.to_csv("descriptive_table.csv", index=False)
print("\n=== Descriptive table (JobSat by AISelect) ===")
print(desc)

# --- Regression 1: binary AI-use indicator -------------------------------------

m1 = smf.ols("job_sat ~ ai_user + work_exp + C(devtype_grp)", data=analysis).fit(cov_type="HC1")

# --- Regression 2: dose-response with full AISelect categories ----------------

analysis["aiselect_cat"] = pd.Categorical(
    analysis["AISelect"], categories=intensity_order, ordered=False
)
m2 = smf.ols(
    "job_sat ~ C(aiselect_cat, Treatment(reference=\"No, and I don't plan to\")) + work_exp + C(devtype_grp)",
    data=analysis,
).fit(cov_type="HC1")

with open("regression_summary.txt", "w", encoding="utf-8") as f:
    f.write("MODEL 1: job_sat ~ ai_user + work_exp + C(devtype_grp), HC1 robust SE\n")
    f.write(str(m1.summary()))
    f.write("\n\nMODEL 2: job_sat ~ C(AISelect, ref=non-user) + work_exp + C(devtype_grp), HC1 robust SE\n")
    f.write(str(m2.summary()))

print("\n=== Model 1 (binary AI-use) ===")
print(m1.summary())
print("\n=== Model 2 (AI-use intensity, dose-response) ===")
print(m2.summary())

# results table for LaTeX -------------------------------------------------------

rows = []
rows.append({
    "model": "M1", "term": "ai_user (uses AI vs. does not)",
    "coef": m1.params["ai_user"], "se": m1.bse["ai_user"], "p": m1.pvalues["ai_user"],
})
rows.append({"model": "M1", "term": "work_exp (years)", "coef": m1.params["work_exp"],
             "se": m1.bse["work_exp"], "p": m1.pvalues["work_exp"]})
rows.append({"model": "M1", "term": "N", "coef": int(m1.nobs), "se": np.nan, "p": np.nan})
rows.append({"model": "M1", "term": "R-squared", "coef": m1.rsquared, "se": np.nan, "p": np.nan})

for term in m2.params.index:
    if "aiselect_cat" in term:
        label = term.split("T.")[-1].rstrip("]")
        rows.append({"model": "M2", "term": label, "coef": m2.params[term],
                     "se": m2.bse[term], "p": m2.pvalues[term]})
rows.append({"model": "M2", "term": "work_exp (years)", "coef": m2.params["work_exp"],
             "se": m2.bse["work_exp"], "p": m2.pvalues["work_exp"]})
rows.append({"model": "M2", "term": "N", "coef": int(m2.nobs), "se": np.nan, "p": np.nan})
rows.append({"model": "M2", "term": "R-squared", "coef": m2.rsquared, "se": np.nan, "p": np.nan})

pd.DataFrame(rows).to_csv("results_table.csv", index=False)

# --- Figure 1: satisfaction by AI use -----------------------------------------

fig, ax = plt.subplots(figsize=(6, 4))
plot_d = desc.dropna(subset=["mean"])
labels = ["No,\ndon't plan", "No, but\nplan to", "Monthly/\ninfrequent", "Weekly", "Daily"]
ax.bar(labels, plot_d["mean"], yerr=plot_d["sd"] / np.sqrt(plot_d["n"]), capsize=4, color="#4C72B0")
ax.set_ylabel("Mean job satisfaction (0-10)")
ax.set_xlabel("Reported AI-tool use")
ax.set_title("Job satisfaction by reported AI-tool use")
ax.set_ylim(0, 10)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig1_satisfaction_by_ai_use.pdf")
plt.close(fig)

# --- Figure 2: distribution of years of professional experience ---------------

fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(analysis["work_exp"], bins=30, color="#55A868", edgecolor="white")
ax.set_xlabel("Years of professional work experience")
ax.set_ylabel("Number of respondents")
ax.set_title("Distribution of professional experience, analysis sample")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig2_years_experience.pdf")
plt.close(fig)

print("\nFigures written to", FIG_DIR)
print("Tables written: descriptive_table.csv, results_table.csv, regression_summary.txt")
