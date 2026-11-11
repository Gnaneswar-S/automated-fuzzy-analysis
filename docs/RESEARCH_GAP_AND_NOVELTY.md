# Research Gap and Candidate Contributions

**Status:** Provisional after the first structured literature pass (2026-11-11). Not a priority or state-of-the-art claim.

## Existing contribution to preserve

The project already integrates verification, conflict localization, diagnosis, constrained repair candidate generation/ranking, re-verification, behavior comparison, controlled defect injection, multi-region counterfactual analysis, and one system-specific JFML numerical validation. These are existing contributions and must not be presented as newly invented.

The README documents finite-grid and threshold dependence, structural ambiguity, and controlled benchmark scope. The supplied baseline also warns of a six-way repair-score tie and that structural improvement does not prove semantic correctness. Those are facts and limitations, not evidence that the system uniquely finds a correct repair.

## Literature implications

1. Structural fuzzy-rule verification has Petri-net and learning-oriented precedents (Scarpelli & Gomide, 1994; Yang et al., 2003; Gonzalez & Pérez, 1998).
2. Inconsistent-rule handling and repair by aggregation are established (Pal & Pal, 1999; Gegov et al., 2015, 2017; Xu et al., 2024).
3. Rule simplification already balances interpretability and accuracy using similarity, clustering, and constrained optimization.
4. Mutation testing is mature outside fuzzy logic; fuzzy-guided software testing is also being explored. Neither supports a broad claim of novelty for “mutation testing fuzzy systems.”
5. Fuzzy counterfactual explanation methods address nonuniqueness in relational settings. Any contribution must stay specific to rule-base diagnosis and repair.
6. JFML validation supports reproducibility, but one-model agreement is not general conformance.

## Candidate contributions

| Candidate | Novelty evidence now | Feasibility | Evaluation needed | Expected impact | Effort |
|---|---|---|---|---|---|
| **A. Typed mutation benchmark for fuzzy rule-base diagnosis and repair.** Define valid operators for consequent/antecedent substitutions, membership-function perturbations, and rule additions/deletions; preserve ground truth and symmetric/ambiguous cases. | Low–medium and unproven. Mutation and controlled benchmark code already exist; comparable fuzzy rule-base suites have not been ruled out. | High–medium; build on existing experiment modules and isolate operators from repair code. | Mutant validity/equivalence; detection/localization precision, recall, F1; tie-aware set accuracy; repair action/target/value accuracy; false positives; runtime by rule count and dimension. | Reproducibility and fair comparisons. | Medium. |
| **B. Ambiguity-aware, behavior-constrained repair assessment.** Return candidate sets/frontiers annotated with structural/completeness changes, region-scoped behavior change, edit cost, and non-identifiability instead of forcing one semantic winner. | Medium and unproven; strongest current fit. Ranking, behavior-aware selection, and tie-aware localization already exist. A possible gap is calibrated assessment across mutation benchmarks, pending direct comparison with aggregation and repair literature. | High; build on current repair, re-verification, and behavior-validation APIs. | Compare current ranking, reproducible consequent aggregation, edit-cost baselines, and behavior-aware selection. Measure set-valued/top-1 correctness, outside-region behavior change, completeness, remaining conflicts, ambiguity, and runtime over multiple rule bases and mutation classes. | Supports human-reviewed repair decisions and addresses structural versus semantic correctness. | Medium. |
| **C. Resolution-stability analysis for sampled conflict regions.** Measure how localization and repair-impact results change with grid resolution and threshold; evaluate adaptive refinement/convergence without claiming guarantees unless proved. | Low–medium and unproven. Sampling sensitivity is known; novelty depends on showing an accuracy/cost advantage. | Medium; current activation and behavior grids can be instrumented, but dimension growth is a risk. | Coarse/fine/adaptive sweeps against dense references; region stability, boundary error, missed-region rate, runtime, memory, dimensions, and threshold sensitivity. | Clarifies sampled point counts versus connected regions and exposes unstable results. | Medium–high. |

## Provisional selection

**Candidate B is the strongest direction to investigate next, not a confirmed novel method.** It connects to the observed ranking ambiguity and existing behavior-aware repair support. Call it a contribution only if it defines a reproducible assessment beyond existing alternatives and demonstrates value across multiple benchmark rule bases.

The selection is provisional because full-text comparisons with 2015/2017/2024 consequent aggregation and the source/output for the supplied 12-rule benchmark are missing. If prior work already covers the proposed output, reconsider Candidates A or C only after stronger evidence.

## Testable hypothesis

> For controlled fuzzy rule-base mutations, a set of structurally valid repair candidates annotated with region-scoped behavior change and ambiguity will provide more reliable information about ground-truth repair identification and collateral behavior than a single scalar repair score, while preserving completeness under the same verification protocol.

This is a hypothesis, not a result. It requires comparison with the current ranker and at least one reproducible conflict-resolution comparator. It does not imply a unique semantic repair in ambiguous cases.

## Minimum evidence before claiming a contribution

- Publish exact conflict, completeness, activation, and behavioral-change definitions with thresholds, grids, and inference semantics.
- Recover and reproduce the 12-rule benchmark source/output or exclude those figures from new evidence.
- Evaluate multiple defect types and rule bases with known ground truth; report ambiguity, false positives/negatives, and uncertainty.
- Compare with the current project and reproducible literature methods, especially consequent aggregation; document non-comparable assumptions.
- Preserve finite-grid caveats and distinguish sampled points from connected regions.
- Limit JFML claims to the selected model and tested points.
- Revise or reject the hypothesis if results do not show an informative improvement.

## Current evidence gap

The first review found direct repair and verification precedents but does not settle whether ambiguity-aware repair assessment is novel. Next, inspect full papers, follow citations around diagnosis/localization/automated repair, and search specifically for fuzzy multi-objective repair with behavior preservation and tie-aware ground-truth metrics. Until then, no “first,” “novel algorithm,” or “state-of-the-art” claim is supportable.
