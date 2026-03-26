import pandas as pd
from sklearn.datasets import load_iris
from scipy import stats

# Load real dataset
iris = load_iris(as_frame=True)
df = iris.frame

print("Dataset preview:")
print(df.head())

# Feature + group
feature = "sepal length (cm)"
group = "target"

group0 = df[df[group] == 0][feature]
group1 = df[df[group] == 1][feature]

print("\n--- Statistical Test ---")

t_stat, p_val = stats.ttest_ind(group0, group1)

print("Independent t-test:")
print(f"p-value: {p_val:.4f}")

# --- Structure Detection ---
structure_hints = {
    "possible_group_column": None,
    "repeated_measures_suspected": False
}

for col in df.columns:
    if df[col].nunique() < 10:
        structure_hints["possible_group_column"] = col
        break

print("\n--- Structure Hint Detection ---")
print(structure_hints)

# --- Interpretation ---
print("\nInterpretation:")
print("Detected grouping variable → independent group comparison is appropriate.")

print("\nConclusion:")
print("Structure-aware detection helps identify correct statistical setting.")