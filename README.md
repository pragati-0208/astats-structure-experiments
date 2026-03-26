# Structure-Aware Statistical Inference (AStats Prototype)

## Overview

This project explores a key failure mode in automated statistical pipelines:

> Incorrect statistical decisions often arise *before* test selection, due to misinterpretation of dataset structure.

To address this, I built a **structure-aware statistical pipeline** that integrates:
- data profiling
- structure detection
- ambiguity handling
- decision logic
- explainable reasoning

---

## Motivation

Many pipelines assume independence between samples by default.

However, real-world datasets may contain:
- repeated measures
- grouped observations
- hidden dependencies

Failing to detect this leads to:
- incorrect test selection  
- misleading p-values  
- invalid conclusions  

---

## Pipeline Architecture
Data
→ Profiling
→ Structure Detection
→ Ambiguity Detection
→ Decision Engine
→ LLM-style Reasoning
→ Statistical Test Execution


---

## Key Features

### 1. Structure Detection
- Identifies grouping columns  
- Detects repeated-measures patterns  
- Avoids misclassifying continuous variables as subjects  

---

### 2. Ambiguity Handling
- Detects unclear or conflicting structure  
- Prevents premature statistical decisions  
- Suggests user clarification when needed  

---

### 3. Decision Engine
- Chooses appropriate statistical test:
  - independent t-test  
  - paired t-test  

---

### 4. LLM-style Reasoning Layer
- Generates human-readable explanations  
- Explains *why* a test was selected  
- Mimics agent-style decision making  

---

## Demonstrations

### Simulated Repeated Measures Data

- Independent test → incorrect result  
- Paired test → correct result  

Shows that:
> Failure occurs at the structure interpretation stage, not test computation.

---

### Real Dataset (Iris)

- Correctly identifies independent grouping (`target`)  
- Selects appropriate independent test  
- Avoids false repeated-measures detection  

---

## Example Output

---

## Key Features

### 1. Structure Detection
- Identifies grouping columns  
- Detects repeated-measures patterns  
- Avoids misclassifying continuous variables as subjects  

---

### 2. Ambiguity Handling
- Detects unclear or conflicting structure  
- Prevents premature statistical decisions  
- Suggests user clarification when needed  

---

### 3. Decision Engine
- Chooses appropriate statistical test:
  - independent t-test  
  - paired t-test  

---

### 4. LLM-style Reasoning Layer
- Generates human-readable explanations  
- Explains *why* a test was selected  
- Mimics agent-style decision making  

---

## Demonstrations

### Simulated Repeated Measures Data

- Independent test → incorrect result  
- Paired test → correct result  

Shows that:
> Failure occurs at the structure interpretation stage, not test computation.

---

### Real Dataset (Iris)

- Correctly identifies independent grouping (`target`)  
- Selects appropriate independent test  
- Avoids false repeated-measures detection  

---

## Example Output
--- Structure Detection ---
{'group_column': 'target', 'repeated_measures': False, 'subject_column': None}

--- Ambiguity Check ---
{'is_ambiguous': False, 'reason': None}

--- Selected Test ---
independent_ttest

--- LLM Reasoning ---
No repeated structure detected → samples are treated as independent.
Therefore, an independent test is appropriate.


---

## Key Insight

> Statistical errors often originate from incorrect assumptions about data structure, not from the statistical tests themselves.

---

## Future Work

- richer statistical profiling (normality, variance, outliers)
- integration with LLM-based reasoning (Codex / Claude / open-weight models)
- interactive user-in-the-loop clarification
- extension to more statistical tests and workflows

---

## Repository

Prototype implementation:
https://github.com/pragati-0208/astats-structure-experiments