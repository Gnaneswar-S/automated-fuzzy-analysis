# Automated Analysis of Fuzzy Rule-Based Systems

An integrated framework for automated verification, diagnosis, localization, repair, re-verification, behavioral validation, and controlled multi-defect interaction analysis of fuzzy rule-based systems.

## 1. Research Objective

Fuzzy rule-based systems can contain structurally overlapping or contradictory rules that are difficult to identify and repair manually.

This project develops a reproducible analysis pipeline that automatically:

1. verifies fuzzy rule bases for consistency and completeness,

2. localizes potentially conflicting rules and fuzzy regions,

3. provides explainable conflict diagnosis,

4. generates constrained repair candidates,

5. applies candidate repairs,

6. re-verifies the repaired rule base,

7. validates behavioral changes caused by repairs,

8. evaluates localization and repair performance using controlled benchmarks,

9. analyzes sensitivity to antecedent similarity and defect severity,

10. characterizes activation overlap between conflicting rules, and

11. studies interactions among multiple defect regions using controlled counterfactual repair interventions.

The project focuses on the integration of these stages into one reproducible analysis framework rather than claiming novelty for any individual fuzzy similarity, localization, or repair technique.

---

## 2. Analysis Pipeline

```text

Fuzzy Rule Base

       |

       v

Consistency + Completeness Verification

       |

       v

Rule-Level Localization

       |

       v

Fuzzy-Region Localization

       |

       v

Explainable Conflict Diagnosis

       |

       v

Repair Candidate Generation

       |

       v

Repair Application

       |

       v

Mandatory Structural Re-verification

       |

       v

Behavioral Repair Validation

       |

       v

Behavior-Aware Repair Selection

       |

       v

Controlled Benchmark Evaluation

       |

       +--> Localization Metrics

       |

       +--> Tie-Aware Localization

       |

       +--> Similarity / Threshold Analysis

       |

       +--> Defect Severity Analysis

       |

       +--> Activation-Aware Diagnosis

       |

       +--> Activation-Overlap Topology

       |

       +--> Multi-Defect Interaction Analysis

                    |

                    v

             Counterfactual Repair

                    |

                    v

          Behavioral / Diagnostic

              Dependency Analysis

```

---

## 3. Core Verification

The verification stage evaluates two complementary properties.

### Consistency

Potential conflicts are identified when rules have sufficiently similar antecedent conditions but different consequents.

The current conflict formulation is:

```text

conflict_score =

    antecedent_similarity

    *
    (1 - consequent_similarity)

```

The current benchmark configuration uses a consistency threshold of `0.7`.

### Completeness

The rule base is evaluated over the specified input space to identify uncovered regions.

A complete benchmark rule base should produce:

```text

Completeness score: 100.0

Uncovered regions: 0

Status: PASS

```

---

## 4. Localization and Diagnosis

Detected conflicts are localized at two levels:

### Rule level

Rules are assigned suspicion based on their involvement in detected conflicts.

### Fuzzy-region level

The system identifies regions of the input space where conflicting rules are simultaneously relevant.

Explainable diagnosis then reports information such as:

* conflicting rule pair,

* conflict severity,

* antecedent similarity,

* consequents,

* conflict-region information.

Activation-aware diagnosis further examines whether conflicting rules are simultaneously strongly active.

---

## 5. Repair

The framework generates constrained repair candidates such as:

* removing a conflicting rule,

* changing a conflicting rule's consequent.

Each candidate is applied to a copy of the rule base.

The repaired rule base is then independently re-verified.

A repair is considered structurally successful when it improves consistency without violating completeness.

The framework therefore does not treat generation of a repair candidate as proof that the repair is valid.

---

## 6. Behavioral Validation

Structural verification alone is insufficient because a repair can remove a structural conflict while changing system behavior elsewhere.

Behavioral validation therefore compares the original and repaired rule bases over a controlled input grid.

The analysis distinguishes:

* behavior changes inside the diagnosed conflict region,

* behavior changes outside the diagnosed conflict region,

* total behavioral changes,

* collateral behavioral changes.

This provides an additional validation layer beyond structural re-verification.

---

## 7. Benchmark Evaluation

The project includes controlled defect injection and benchmark evaluation.

A benchmark specifies:

* clean rule base,

* injected defect,

* target rule,

* original value,

* injected value,

* expected repair,

* expected corrected value.

The evaluation measures:

* defect detection,

* localization,

* repair action,

* repair target,

* repair value,

* repair success.

Additional localization measures include:

* precision,

* recall,

* F1-score,

* tie-aware candidate-set accuracy,

* ambiguous-case rate.

---

## 8. Important Localization Result

The controlled benchmark demonstrates an important limitation of rule-level localization.

When two rules are structurally symmetric, the system may correctly identify the conflicting candidate set without being able to uniquely identify which rule was originally corrupted.

For example, the four baseline benchmark cases produce:

```text

Candidate set: ['R2', 'R4']

Candidate-set accuracy: 100%

Ambiguous case rate: 100%

```

while conventional single-rule localization achieves lower accuracy.

This is treated as structural ambiguity rather than artificially resolving the benchmark through additional assumptions.

---

# 9. Controlled Similarity Experiment

The similarity experiment systematically shifts a triangular fuzzy set relative to a base set.

Observed similarities include:

```text

shift -20 : 0.1429

shift -15 : 0.2427

shift -10 : 0.3913

shift  -5 : 0.6203

shift   0 : 1.0000

shift  +5 : 0.6203

shift +10 : 0.3913

shift +15 : 0.2427

shift +20 : 0.1429

```

This experiment demonstrates how the selected similarity threshold affects conflict detection.

For the current threshold of `0.7`, similarity `0.6203` is below the detection threshold while identical antecedents produce a similarity of `1.0`.

---

# 10. Defect Severity Experiment

The controlled defect-severity experiment varies the antecedent position of an injected defect.

The experiment measures:

* antecedent similarity,

* conflict score,

* conflict detection,

* localized rule,

* repair candidate count,

* successful repair count,

* verification status.

The experiment therefore examines how structural separation between rule antecedents affects detectability under the selected threshold.

---

# 11. Activation-Aware Conflict Analysis

For structurally conflicting rules, the framework examines regions where both rules are strongly active.

For the baseline conflict:

```text

R2 <-> R4

```

the activation-aware analysis identifies a connected conflict region containing six sampled points at the configured resolution.

The analysis records:

* input coordinates,

* activation of each rule,

* consequents,

* activation threshold.

---

# 12. Activation-Overlap Topology

Activation overlap is further characterized as connected regions rather than only as a scalar similarity value.

For each overlap component the framework can report:

* number of sampled points,

* maximum joint activation,

* input-space bounds,

* representative point.

This distinguishes structural similarity from actual simultaneous activation in the fuzzy input space.

---

# 13. Multi-Defect Experiments

The project progressively evaluates multi-defect configurations.

## MD-2 - Independent Defect Regions

Two defect regions are deliberately separated.

Expected relationship:

```text

INDEPENDENT

```

Counterfactual repair produces no measurable dependency between the two regions under the configured experiment.

---

## MD-3 - Overlapping Defect Regions

Two defect regions have overlapping activation geometry without forming the stronger coupled conflict network used in MD-4.

The experiment demonstrates behavioral dependency under counterfactual repair while preserving the primary diagnosis of the remaining defect.

---

## MD-4 - Interacting Defect Regions

The two defect regions form a coupled conflict network.

The defective configuration contains multiple cross-region conflicts.

Under controlled counterfactual repair interventions, repair of one region changes both behavior and diagnostic context associated with the remaining region.

The result is interpreted as measured dependency within the specified experimental configuration, not as proof of a universal causal law.

---

# 14. Three-Region Experiments

## MD-5 - Three Independent Defect Regions

Three defect regions are positioned in separated fuzzy regions.

The counterfactual dependency matrix shows:

```text

A -> B : no dependency

A -> C : no dependency

B -> A : no dependency

B -> C : no dependency

C -> A : no dependency

C -> B : no dependency

```

This provides a multi-region baseline for comparison.

---

## MD-6 - Three Interacting Defect Regions

MD-6 introduces three geometrically shifted low-input regions:

```text

A = (0, 20, 40)

B = (2, 22, 42)

C = (4, 24, 44)

```

The resulting structure produces a coupled conflict network while preserving complete coverage.

The defective configuration contains:

```text

9 conflicts

100% completeness

PASS completeness status

```

The counterfactual experiment records behavioral dependency across all six directed region pairs.

Diagnostic changes are additionally observed for:

```text

A -> B

B -> A

B -> C

C -> B

```

The A/C directions exhibit behavioral dependency without the same diagnostic-context change under the configured measurements.

These observations are specific to the benchmark geometry, activation threshold, sampling resolution, and repair interventions.

---

# 15. Counterfactual Interaction Analysis

For a target defect region, the framework:

1. records the original defective state,

2. repairs only the selected target region,

3. re-verifies the resulting rule base,

4. compares the conflict structure,

5. compares behavior over the input grid,

6. evaluates each remaining defect region independently.

This creates a directed dependency matrix.

A dependency is detected when the counterfactual repair produces either:

* a diagnostic change, or

* a measured behavioral change

in another defect region.

The experiment therefore distinguishes:

```text

structural defect persistence

diagnostic dependency

behavioral dependency

```

Changed-point counts are grid-sampled measurements and should not be interpreted as universal invariants.

---

# 16. Experimental Interpretation

The controlled experiments support the following bounded observation:

> Across the evaluated configurations, increasing coupling from independent regions to overlapping regions and then to an interacting conflict network produced progressively different measured effects of counterfactual repair.

This should be interpreted within the defined benchmark configurations and parameter settings.

The experiments do not establish a universal causal law for arbitrary fuzzy rule bases.

---

# 17. Repository Structure

```text
automated_fuzzy_analysis/
|-- main.py
|-- data/
|   |-- sample_rules.py
|-- core/
|   |-- rules/
|   |-- fuzzy/
|   |-- verification/
|   |-- diagnosis/
|   |-- repair/
|   |-- experiments/
|-- results/
|   |-- .gitkeep
|-- README.md
|-- .gitignore
```

# 18. Running the Project

Create and activate a Python environment, install the dependencies required by the project, and run:

```powershell

python main.py

```

The main execution demonstrates the baseline verification, diagnosis, repair, benchmark, localization, similarity, severity, and activation-analysis pipeline.

The multi-defect experiment functions can be imported from:

```text

core.experiments.multi_defect_experiment

```

The principal multi-defect constructors are:

```text

create_independent_experiment_case()

create_overlapping_experiment_case()

create_interacting_experiment_case()

create_three_region_independent_experiment_case()

create_three_region_interacting_experiment_case()

```

The counterfactual analysis functions are:

```text

run_interacting_counterfactual_experiment()

run_multi_region_counterfactual_experiment()

```

---

# 19. Reproducibility Parameters

Important experimental parameters include:

```text

Consistency threshold:       0.7

Activation threshold:        0.7

Typical activation grid:     resolution = 50

Completeness resolution:     100

Multi-region completeness:   30

```

Changing these parameters can change conflict detection, activation regions, behavioral-change counts, and counterfactual dependency results.

Therefore reported numerical results should always be interpreted together with their experimental configuration.

---

# 20. Limitations

The current framework has several important limitations.

### Controlled benchmark scope

The benchmark experiments use deliberately constructed fuzzy rule bases. They demonstrate behavior under controlled conditions rather than representing all real-world fuzzy systems.

### Sampling dependence

Activation overlap and behavioral validation use finite grids. Reported point counts depend on the selected resolution.

### Threshold dependence

Conflict detection depends on the configured antecedent-similarity threshold.

### Ambiguous localization

Structurally symmetric conflicts can prevent unique identification of the originally corrupted rule.

### Repair assumptions

The benchmark ground truth specifies the intended repair. Real-world rule bases may not provide an unambiguous correct consequent.

### Counterfactual interpretation

Observed dependency is measured under controlled repair interventions. It should not be interpreted as proof of a general causal relationship.

---

# 21. Research Contribution

The primary contribution of this project is an integrated and reproducible framework connecting:

```text

verification

    +

localization

    +

explainable diagnosis

    +

repair

    +

re-verification

    +

behavioral validation

    +

controlled benchmarking

    +

activation analysis

    +

multi-defect counterfactual analysis

```

The work emphasizes traceable transitions between structural verification, diagnosis, repair, and empirical evaluation.

Individual components such as fuzzy-set similarity, conflict detection, activation analysis, and rule repair are treated as established techniques rather than being presented as independently novel algorithms.

---

# 22. Current Status

The implementation includes:

* single-defect verification and repair,

* controlled benchmark evaluation,

* localization metrics,

* tie-aware localization,

* similarity sensitivity analysis,

* defect-severity analysis,

* activation-aware diagnosis,

* activation-overlap topology,

* two-region multi-defect experiments,

* three-region independent experiments,

* three-region interacting experiments,

* counterfactual interaction analysis,

* regression validation across MD-2 through MD-6.

The complete implementation has been validated through regression execution and controlled experiment execution.

---

## 23. External JFML Validation

The framework includes an external numerical validation against the independently sourced **JFML v1.3** implementation using the official JFML example:

`Examples/XMLFiles/InvertedPendulumMamdani1.xml`

The validation is deliberately limited to the inference semantics established for this selected Mamdani system. It is not intended to claim general equivalence with arbitrary JFML systems.

### External system

The selected rule base contains:

- 19 rules
- 2 input variables: `Angle` and `ChangeAngle`
- 1 output variable: `Force`
- input and output domains: `0` to `255`
- Mamdani inference
- `MIN` rule activation
- `MIN` antecedent aggregation
- `MAX` output accumulation
- Center of Gravity (`COG`) defuzzification
- triangular and trapezoidal membership functions

The JFML implementation was inspected directly from `JFML-v1.3.jar` to establish the inference and defuzzification behavior used by this validation.

For the continuous COG defuzzifier, JFML uses 2000 regular discretization points across the output domain and additionally inserts membership-function breakpoint values into the discretization map. For this rule base, the resulting output discretization contains 2006 points.

### Independent reference implementation

An independent numerical implementation is provided in:

`core/experiments/jfml_independent_reference.py`

It does not import JFML or invoke the JFML Java implementation. It reproduces only the established semantics required for the selected Inverted Pendulum M1 system, using NumPy `float32` arithmetic.

The independent implementation therefore provides a separate numerical calculation against which the external JFML results can be compared.

### Systematic validation

The validation fixture:

`core/experiments/jfml_validation_sweep.csv`

contains 289 JFML evaluations over a 17 x 17 input grid spanning the complete input domain.

The comparison script:

`core/experiments/compare_jfml_validation.py`

uses a **predeclared absolute-error tolerance of `1e-5`**.

Observed results:

| Metric | Result |
|---|---:|
| JFML evaluations | 289 |
| Independent evaluations | 289 |
| Maximum absolute error | `4.92178742206e-10` |
| Mean absolute error | `2.62975406925e-10` |
| Comparisons within tolerance | 289 |
| Comparisons above tolerance | 0 |
| NaN mismatches | 0 |

All 289 systematic evaluations agreed within the predeclared tolerance.

### Boundary and transition validation

A separate fixture:

`core/experiments/jfml_boundary_sweep.csv`

evaluates the Cartesian product of the principal membership-function transition and domain-boundary values:

`0, 48, 88, 128, 168, 208, 255`

This produces 49 evaluations.

The comparison script:

`core/experiments/compare_jfml_boundary.py`

uses the same predeclared absolute-error tolerance of `1e-5`.

Observed results:

| Metric | Result |
|---|---:|
| JFML evaluations | 49 |
| Independent evaluations | 49 |
| Maximum absolute error | `3.67180064131e-10` |
| Mean absolute error | `2.60321107074e-10` |
| Comparisons within tolerance | 49 |
| Comparisons above tolerance | 0 |
| NaN mismatches | 0 |

All 49 boundary/transition evaluations agreed within the predeclared tolerance.

### Reproducibility

The validation artifacts are version-controlled in this repository:

- `core/experiments/jfml_independent_reference.py`
- `core/experiments/jfml_validation_sweep.csv`
- `core/experiments/jfml_boundary_sweep.csv`
- `core/experiments/compare_jfml_validation.py`
- `core/experiments/compare_jfml_boundary.py`
- `requirements.txt`

The Java JFML library itself is not vendored into this repository. The validation therefore records the external reference results as reproducible fixtures while keeping the independent implementation separate from the external implementation.

### Scope of the claim

This validation supports numerical agreement between the independent implementation and JFML for the selected **Inverted Pendulum Mamdani M1** rule base and the tested input points.

It does not establish equivalence for:

- arbitrary JFML rule bases,
- unsupported JFML membership-function types,
- unsupported inference operators,
- TSK or Tsukamoto systems,
- circular membership-function definitions,
- alternative accumulation operators, or
- other defuzzification methods.

The external validation is therefore treated as a **system-specific semantic validation**, rather than as a claim of general JFML compatibility.

## License

Add the appropriate project license before public release.
