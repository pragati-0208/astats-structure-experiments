# Structure-Aware Statistical Inference (AStats Prototype)

## Overview
This project explores how early-stage dataset understanding impacts statistical correctness in agentic workflows.

A key challenge in automated statistical analysis is that incorrect assumptions about dataset structure (e.g., independence of samples) can lead to invalid conclusions **before test selection even occurs**.

This prototype demonstrates how incorporating **structure-aware reasoning** can improve statistical decision-making.

---

## Problem
Many statistical pipelines assume independence between samples.

However, real-world datasets often contain:
- repeated measures  
- grouping variables  
- dependent observations  

This can lead to:
- incorrect test selection  
- misleading p-values  
- invalid conclusions  

A common example is **pseudoreplication**, where repeated observations are treated as independent samples.

---

## Experiments

### 1. Simulated Repeated-Measures Failure Case

A synthetic dataset is used to demonstrate how incorrect assumptions affect results:

- Independent t-test → **p ≈ 0.07 (incorrect conclusion)**  
- Paired t-test → **p ≈ 0.0001 (correct conclusion)**  

✔ Shows that the failure occurs at the **structure interpretation stage**

✔ A simple heuristic detects:
- subject-level grouping  
- repeated-measures structure  

---

### 2. Real Dataset Experiment (Iris)

A real dataset is used to validate generalization:

- Detects grouping variable (`target`)  
- Applies appropriate statistical test (independent t-test)  
- Produces correct statistical interpretation  

✔ Demonstrates that structure-aware reasoning works beyond synthetic data  

---

## Key Insight

Incorrect structure assumptions can fundamentally alter statistical conclusions.

These errors occur:
> **before statistical testing — during dataset understanding**

A structure-aware layer can help detect:
- grouping variables  
- repeated-measures patterns  
- dependency structures  

and guide correct downstream analysis.

---

## Approach

This prototype introduces a simple **structure-aware layer** that:

- analyzes dataset columns  
- detects potential grouping variables  
- flags repeated-measures patterns  
- provides hints for correct test selection  

---

## Prototype Pipeline
Data → Structure Detection → Statistical Test Selection → Result


---

## Future Direction

- Extend to full **data profiling + structure inference pipeline**  
- Integrate with **agentic AI workflows (AStats)**  
- Incorporate **LLM-based reasoning (Claude / Codex / open-weight models)**  
- Support more complex statistical scenarios:
  - regression  
  - hierarchical models  
  - longitudinal data  

---

## Repository

GitHub: https://github.com/pragati-0208/astats-structure-experiments