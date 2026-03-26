import pandas as pd
from sklearn.datasets import load_iris
from scipy import stats

# Load real dataset
iris = load_iris(as_frame=True)
df = iris.frame

print("Dataset preview:")
print(df.head())

# Assume:
# - target = species (group)
# - feature = sepal length

feature = "sepal length (cm)"
group = "target"

# Split groups
group0 = df[df[group] == 0][feature]
group1 = df[df[group] == 1][feature]

print("\n--- Statistical Test Comparison ---")

# Independent t-test (correct here)
t_stat, p_val = stats.ttest_ind(group0, group1)

print("Independent t-test:")
print(f"p-value: {p_val:.4f}")

# Simple structure detection heuristic
def detect_structure(df):
    for col in df.columns:
        if df[col].nunique() < 10:
            return {"possible_group_column": col, "repeated_measures_suspected": False}
    return {"possible_group_column": None, "repeated_measures_suspected": False}

print("\n--- Structure Hint Detection ---")
print(detect_structure(df))

print("\nConclusion:")
print("Detected grouping structure helps guide correct statistical test selection.")