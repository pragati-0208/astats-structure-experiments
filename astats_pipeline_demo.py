import pandas as pd
from scipy import stats
from sklearn.datasets import load_iris
import numpy as np

# -------------------------------
# STRUCTURE DETECTION
# -------------------------------
def detect_structure(df):
    structure = {
        "group_column": None,
        "repeated_measures": False
    }

    # Step 1: find categorical/group column
    for col in df.columns:
        unique_vals = df[col].nunique()

        if unique_vals <= 10:
            structure["group_column"] = col
            break

    # Step 2: detect subject-like column (high duplication)
    subject_col = None
    for col in df.columns:
        if df[col].duplicated().sum() > len(df) * 0.5:
            subject_col = col

    # Step 3: repeated measures condition
    if subject_col and structure["group_column"]:
        if subject_col != structure["group_column"]:
            structure["repeated_measures"] = True

    return structure


# -------------------------------
# DECISION LOGIC
# -------------------------------
def choose_test(structure):
    if structure["repeated_measures"]:
        return "paired_ttest"
    else:
        return "independent_ttest"


# -------------------------------
# EXECUTION
# -------------------------------
def run_pipeline(df, feature, group_col):
    structure = detect_structure(df)

    print("\n--- Detected Structure ---")
    print(structure)

    test_type = choose_test(structure)

    print("\n--- Selected Test ---")
    print(test_type)

    if test_type == "paired_ttest":
        before = df[df[group_col] == df[group_col].unique()[0]][feature]
        after = df[df[group_col] == df[group_col].unique()[1]][feature]

        stat, p = stats.ttest_rel(before, after)

    else:
        group0 = df[df[group_col] == df[group_col].unique()[0]][feature]
        group1 = df[df[group_col] == df[group_col].unique()[1]][feature]

        stat, p = stats.ttest_ind(group0, group1)

    print("\n--- Result ---")
    print(f"p-value: {p:.4f}")


# -------------------------------
# TEST WITH REAL DATA
# -------------------------------
iris = load_iris(as_frame=True)
df = iris.frame

print("Running pipeline on Iris dataset")

run_pipeline(df, "sepal length (cm)", "target")