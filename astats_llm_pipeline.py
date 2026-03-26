import pandas as pd
from scipy import stats
from sklearn.datasets import load_iris
import numpy as np

# -------------------------------
# PROFILING
# -------------------------------
def profile_data(df):
    profile = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "column_types": {}
    }

    for col in df.columns:
        if df[col].dtype == "object":
            profile["column_types"][col] = "categorical"
        elif np.issubdtype(df[col].dtype, np.number):
            profile["column_types"][col] = "numeric"
        else:
            profile["column_types"][col] = "other"

    return profile


# -------------------------------
# STRUCTURE DETECTION
# -------------------------------
def detect_structure(df):
    structure = {
        "group_column": None,
        "repeated_measures": False,
        "subject_column": None
    }

    # --- Detect grouping column (categorical-like) ---
    for col in df.columns:
        if df[col].nunique() <= 10:
            structure["group_column"] = col
            break

    # --- Detect subject-like column (ID-like, not continuous) ---
    for col in df.columns:
        unique_vals = df[col].nunique()

    # subject column must:
    # 1. NOT be continuous numeric (avoid float columns)
    # 2. have repeated values (same entity appears multiple times)
    # 3. not be too low-cardinality like group labels

        if not np.issubdtype(df[col].dtype, np.floating):  # avoid continuous numeric
            if unique_vals > 10 and unique_vals < len(df):
                if df[col].duplicated().sum() > len(df) * 0.3:
                    structure["subject_column"] = col

    # --- Repeated measures detection (CORRECT LOGIC) ---
    if structure["subject_column"] and structure["group_column"]:
        cross_counts = df.groupby(structure["subject_column"])[structure["group_column"]].nunique()

        if (cross_counts > 1).any():
            structure["repeated_measures"] = True

    return structure


# -------------------------------
# DECISION ENGINE
# -------------------------------
def choose_test(structure):
    if structure["repeated_measures"]:
        return "paired_ttest"
    else:
        return "independent_ttest"


# -------------------------------
# LLM-LIKE REASONING LAYER
# -------------------------------
def generate_reasoning(profile, structure, test_type):
    reasoning = []

    reasoning.append(f"Dataset contains {profile['num_rows']} rows and {profile['num_columns']} columns.")

    if structure["group_column"]:
        reasoning.append(f"Column '{structure['group_column']}' appears to represent grouping information.")

    if structure["subject_column"]:
        reasoning.append(f"Column '{structure['subject_column']}' appears to represent entity/subject identity.")

    if structure["repeated_measures"]:
        reasoning.append("Detected repeated observations for the same entity across groups → dependent samples.")
        reasoning.append("Therefore, a paired statistical test is appropriate.")
    else:
        reasoning.append("No repeated structure detected → samples are treated as independent.")
        reasoning.append("Therefore, an independent test is appropriate.")

    reasoning.append(f"Final decision: {test_type}")

    return "\n".join(reasoning)


def detect_ambiguity(df, structure):
    ambiguity = {
        "is_ambiguous": False,
        "reason": None
    }

    # case 1: no group column
    if structure["group_column"] is None:
        ambiguity["is_ambiguous"] = True
        ambiguity["reason"] = "No clear grouping column detected."

    # case 2: multiple possible group columns
    candidate_groups = [col for col in df.columns if df[col].nunique() <= 10]
    if len(candidate_groups) > 1:
        ambiguity["is_ambiguous"] = True
        ambiguity["reason"] = f"Multiple possible grouping columns detected: {candidate_groups}"

    return ambiguity

# -------------------------------
# PIPELINE EXECUTION
# -------------------------------
def run_pipeline(df, feature, group_col):
    print("\n=== AStats Pipeline Execution ===")

    # profiling
    profile = profile_data(df)
    print("\n--- Profiling ---")
    print(profile)

    # structure
    structure = detect_structure(df)
    print("\n--- Structure Detection ---")
    print(structure)

    # ambiguity check
    ambiguity = detect_ambiguity(df, structure)

    print("\n--- Ambiguity Check ---")
    print(ambiguity)

    if ambiguity["is_ambiguous"]:
        print("\n⚠️ Ambiguity detected:")
        print(ambiguity["reason"])
        print("Suggestion: User clarification required before proceeding.")
        return

    # decision
    test_type = choose_test(structure)
    print("\n--- Selected Test ---")
    print(test_type)

    # reasoning
    reasoning = generate_reasoning(profile, structure, test_type)
    print("\n--- LLM Reasoning ---")
    print(reasoning)

    # execution
    if test_type == "paired_ttest":
        before = df[df[group_col] == df[group_col].unique()[0]][feature]
        after = df[df[group_col] == df[group_col].unique()[1]][feature]
        _, p = stats.ttest_rel(before, after)
    else:
        group0 = df[df[group_col] == df[group_col].unique()[0]][feature]
        group1 = df[df[group_col] == df[group_col].unique()[1]][feature]
        _, p = stats.ttest_ind(group0, group1)

    print("\n--- Result ---")
    print(f"p-value: {p:.4f}")


# -------------------------------
# TEST WITH REAL DATA
# -------------------------------
iris = load_iris(as_frame=True)
df = iris.frame

run_pipeline(df, "sepal length (cm)", "target")