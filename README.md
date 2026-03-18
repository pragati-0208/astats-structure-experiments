# Structure-Aware Statistical Inference (AStats Prototype)

## Problem
Statistical pipelines often assume independence between samples.
However, many real-world datasets contain repeated measures.

This leads to incorrect test selection and misleading conclusions.

## Demonstration
Using a simulated dataset:

- Independent t-test → p ≈ 0.07 (incorrect conclusion)
- Paired t-test → p ≈ 0.0001 (correct conclusion)

## Insight
Failure occurs BEFORE test selection — at the stage of structure understanding.

## Approach
A simple heuristic layer was added to:
- detect grouping columns
- identify repeated measures

## Output
The system correctly identifies:
- subject-level grouping
- repeated measures structure

## Future Direction
Integrate structure-aware profiling into agentic workflows to prevent early-stage statistical errors.