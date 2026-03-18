import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(42)

# --- Create repeated measures dataset ---
subjects = np.repeat(np.arange(30), 2)  # same subject twice
condition = np.tile(["before", "after"], 30)

# same subjects → dependent data
# strong subject-specific baseline
subject_effect = np.repeat(np.random.normal(50, 5, 30), 2)

# small treatment effect
treatment_effect = np.where(condition == "after", 2, 0)

# final score = subject variation + small treatment
scores = subject_effect + treatment_effect + np.random.normal(0, 2, 60)
df = pd.DataFrame({
    "subject": subjects,
    "condition": condition,
    "score": scores
})

print("Dataset preview:")
print(df.head())

# --- WRONG APPROACH (independent test) ---
before = df[df["condition"] == "before"]["score"]
after = df[df["condition"] == "after"]["score"]

t_stat, p_val = stats.ttest_ind(before, after)
print("\n❌ Independent t-test (WRONG for repeated measures):")
print("p-value:", round(p_val, 4))

# --- CORRECT APPROACH (paired test) ---
before_sorted = df[df["condition"] == "before"].sort_values("subject")["score"]
after_sorted = df[df["condition"] == "after"].sort_values("subject")["score"]

t_stat_paired, p_val_paired = stats.ttest_rel(before_sorted, after_sorted)

print("\n✅ Paired t-test (CORRECT):")
print("p-value:", round(p_val_paired, 4))

print("\n--- Structure Hint Detection ---")

structure_hints = {
    "possible_group_column": None,
    "repeated_measures_suspected": False
}

# better grouping detection
candidate_cols = []

for col in df.columns:
    unique_ratio = df[col].nunique() / len(df)

    # avoid columns with too few or too many unique values
    if 0.05 < unique_ratio <= 0.6:
        candidate_cols.append(col)

# choose best candidate (highest repetition)
best_col = None
max_duplicates = 0

for col in candidate_cols:
    duplicates = df[col].duplicated().sum()
    if duplicates > max_duplicates:
        max_duplicates = duplicates
        best_col = col

structure_hints["possible_group_column"] = best_col

# repeated measures detection
if best_col and df[best_col].duplicated().sum() > len(df) * 0.3:
    structure_hints["repeated_measures_suspected"] = True

print(structure_hints)

print("\nConclusion:")
print("Incorrect structure assumption leads to incorrect statistical inference.")
print("Structure-aware detection can prevent this failure.")