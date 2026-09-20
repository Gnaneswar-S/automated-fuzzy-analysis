from collections import defaultdict

from core.verification.verification import verify_rule_base
from core.fuzzy.fuzzy_sets import TriangularFuzzySet
from core.rules.rules import FuzzyRule

from core.diagnosis.diagnosis import (
    diagnose_conflicts as diagnose_explainable_conflicts
)

from core.repair.repair import generate_repair_candidates
from core.repair.repair_engine import evaluate_repair_candidate
from core.repair.ranking import rank_repair_candidates
from core.repair.behavioral_validation import evaluate_repair_behavior
from core.repair.behavior_aware_selection import (
    select_behaviorally_safe_repairs
)

from core.experiments.benchmark import create_benchmark_case
from core.experiments.defect_injection import inject_consequent_conflict
from core.experiments.evaluation import evaluate_benchmark_case

from core.experiments.localization_metrics import (
    calculate_localization_metrics
)

from core.experiments.benchmark_runner import (
    run_benchmark_case,
    aggregate_benchmark_results,
)

from core.diagnosis.localization import (
    calculate_rule_suspicion_scores,
    locate_conflict_regions
)

from core.experiments.tie_aware_localization import (
    evaluate_tie_aware_localization
)

from core.experiments.severity_experiment import (
    generate_shifted_fuzzy_sets,
    calculate_similarity_experiment,
    evaluate_thresholds,
    evaluate_generated_rule_pairs
)

from core.experiments.defect_severity_experiment import (
    evaluate_defect_severity
)

from core.diagnosis.conflict_diagnosis import (
    diagnose_conflicts as diagnose_activation_conflicts
)

from core.diagnosis.activation_overlap import (
    characterize_conflict_overlaps
)

# -----------------------------------------
# FUZZY SETS
# -----------------------------------------

temperature_low = TriangularFuzzySet(
    "low",
    0,
    20,
    40
)

temperature_medium = TriangularFuzzySet(
    "medium",
    30,
    50,
    70
)

temperature_high = TriangularFuzzySet(
    "high",
    60,
    80,
    100
)


# -----------------------------------------
# RULES
# -----------------------------------------

rule_1 = FuzzyRule(
    rule_id="R1",
    antecedent={
        "temperature": temperature_low
    },
    consequent="risk_low"
)

rule_2 = FuzzyRule(
    rule_id="R2",
    antecedent={
        "temperature": temperature_medium
    },
    consequent="risk_medium"
)

rule_3 = FuzzyRule(
    rule_id="R3",
    antecedent={
        "temperature": temperature_high
    },
    consequent="risk_high"
)

rule_4 = FuzzyRule(
    rule_id="R4",
    antecedent={
        "temperature":
            temperature_medium
    },
    consequent="risk_high"
)

rules = [
    rule_1,
    rule_2,
    rule_3,
    rule_4
]

# -----------------------------------------
# CLEAN BASELINE RULE BASE
# -----------------------------------------

clean_rules = [
    FuzzyRule(
        rule_id="R1",
        antecedent={
            "temperature": temperature_low
        },
        consequent="risk_low"
    ),

    FuzzyRule(
        rule_id="R2",
        antecedent={
            "temperature": temperature_medium
        },
        consequent="risk_medium"
    ),

    FuzzyRule(
        rule_id="R3",
        antecedent={
            "temperature": temperature_high
        },
        consequent="risk_high"
    ),

    FuzzyRule(
        rule_id="R4",
        antecedent={
            "temperature": temperature_medium
        },
        consequent="risk_medium"
    )
]

# -----------------------------------------
# INPUT RANGE
# -----------------------------------------

variable_ranges = {
    "temperature": (0, 100)
}


# -----------------------------------------
# UNIFIED VERIFICATION
# -----------------------------------------

result = verify_rule_base(
    rules,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
)
verification_result = result


# -----------------------------------------
# REPORT
# -----------------------------------------

print("\n============================================")
print("FUZZY RULE-BASE VERIFICATION REPORT")
print("============================================")


print(
    "\nRules analyzed:",
    result["rules_analyzed"]
)


# -----------------------------------------
# CONSISTENCY
# -----------------------------------------

print("\nConsistency")
print("--------------------------------------------")

print(
    "Potential conflicts:",
    result["consistency"]["conflict_count"]
)

print(
    "Status:",
    result["consistency"]["status"]
)


if result["consistency"]["conflicts"]:

    print("\nDetected conflicts:")

    for conflict in result["consistency"]["conflicts"]:

        print(
            f"  {conflict['rule_1']} <-> "
            f"{conflict['rule_2']} | "
            f"score = "
            f"{conflict['conflict_score']}"
        )


# -----------------------------------------
# COMPLETENESS
# -----------------------------------------

print("\nCompleteness")
print("--------------------------------------------")

print(
    "Coverage:",
    result["completeness"]["score"],
    "%"
)

print(
    "Uncovered regions:",
    result["completeness"]["uncovered_count"]
)

print(
    "Status:",
    result["completeness"]["status"]
)


# -----------------------------------------
# OVERALL STATUS
# -----------------------------------------

print("\nOverall status")
print("--------------------------------------------")

print(
    result["overall_status"]
)

print("\n============================================")
# -----------------------------------------
# RULE LOCALIZATION
# -----------------------------------------

localization = calculate_rule_suspicion_scores(
    rules,
    variable_ranges,
    consistency_threshold=0.7
)


print("\nRule Localization")
print("--------------------------------------------")

for item in localization:

    print(
        f"{item['rule_id']} | "
        f"suspicion = "
        f"{item['suspicion_score']} | "
        f"conflicts = "
        f"{item['conflict_count']}"
    )
# -----------------------------------------
# FUZZY-REGION LOCALIZATION
# -----------------------------------------

regions = locate_conflict_regions(
    rules,
    variable_ranges,
    threshold=0.7,
    resolution=50
)


print("\nFuzzy-Region Localization")
print("--------------------------------------------")

print(
    "Conflict-region points:",
    len(regions)
)


if regions:

    print("\nExample conflict regions:")

    for region in regions[:10]:

        print(
            f"{region['inputs']} | "
            f"{region['rule_1']} <-> "
            f"{region['rule_2']} | "
            f"strength = "
            f"{region['conflict_strength']}"
        )

else:

    print(
        "No conflict regions detected."
    )

# -----------------------------------------
# EXPLAINABLE DIAGNOSIS
# -----------------------------------------

diagnoses = diagnose_explainable_conflicts(
    rules,
    result["consistency"]["conflicts"],
    regions
)

print("\nExplainable Diagnosis")
print("--------------------------------------------")

for diagnosis in diagnoses:

    print(
        f"Conflict: "
        f"{diagnosis['rule_1']} <-> "
        f"{diagnosis['rule_2']}"
    )

    print(
        f"Severity: "
        f"{diagnosis['severity']}"
    )

    print(
        f"Reason: "
        f"{diagnosis['reason']}"
    )

    print(
        f"Consequents: "
        f"{diagnosis['consequent_1']} "
        f"vs "
        f"{diagnosis['consequent_2']}"
    )

    print(
        f"Conflict-region points: "
        f"{diagnosis['conflict_region_count']}"
    )
# -----------------------------------------
# REPAIR CANDIDATES
# -----------------------------------------

repair_candidates = generate_repair_candidates(
    rules,
    result["consistency"]["conflicts"]
)

print("\nRepair Candidates")
print("--------------------------------------------")

for index, candidate in enumerate(
    repair_candidates,
    start=1
):

    print(
        f"{index}. "
        f"{candidate['action']} | "
        f"{candidate['target_rule']}"
    )

    print(
        f"   {candidate['description']}"
    )
# -----------------------------------------
# REPAIR APPLICATION + RE-VERIFICATION
# -----------------------------------------

print("\nRepair Application + Mandatory Re-verification")
print("--------------------------------------------")


# Select one candidate for controlled testing.
# Here we change R4 from risk_high to risk_medium.

repair_candidate = {
    "action": "CHANGE_CONSEQUENT",
    "target_rule": "R4",
    "new_consequent": "risk_medium",
    "description":
        "Change R4 consequent from "
        "'risk_high' to 'risk_medium'."
}


repair_result = evaluate_repair_candidate(
    rules,
    repair_candidate,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
)


# -----------------------------------------
# BEFORE
# -----------------------------------------

before = repair_result["before"]

print("\nBEFORE REPAIR")
print("--------------------------------------------")

print(
    "Conflicts:",
    before["consistency"]["conflict_count"]
)

print(
    "Completeness:",
    before["completeness"]["score"],
    "%"
)

print(
    "Overall status:",
    before["overall_status"]
)


# -----------------------------------------
# AFTER
# -----------------------------------------

after = repair_result["after"]

print("\nAFTER REPAIR")
print("--------------------------------------------")

print(
    "Conflicts:",
    after["consistency"]["conflict_count"]
)

print(
    "Completeness:",
    after["completeness"]["score"],
    "%"
)

print(
    "Overall status:",
    after["overall_status"]
)


# -----------------------------------------
# COMPARISON
# -----------------------------------------

comparison = repair_result["comparison"]

print("\nRepair Evaluation")
print("--------------------------------------------")

print(
    "Conflict improvement:",
    comparison["conflict_improved"]
)

print(
    "Completeness preserved:",
    comparison["completeness_preserved"]
)

print(
    "Repair verification:",
    "SUCCESS"
    if comparison["repair_success"]
    else "FAILED"
)

# -----------------------------------------
# BEHAVIORAL REPAIR VALIDATION
# -----------------------------------------

behavioral_validation = evaluate_repair_behavior(
    rules,
    repair_result["repaired_rules"],
    variable_ranges,
    result["consistency"]["conflicts"],
    resolution=50,
    activation_threshold=0.7
)

print("\nBehavioral Repair Validation")
print("--------------------------------------------")

print(
    "Grid points:",
    behavioral_validation["grid_points"]
)

print(
    "Behavior changes:",
    behavioral_validation["changed_point_count"]
)

print(
    "Changes inside diagnosed conflict region:",
    behavioral_validation["affected_change_count"]
)

print(
    "Changes outside diagnosed conflict region:",
    behavioral_validation["collateral_change_count"]
)

print(
    "Repair safety:",
    behavioral_validation["repair_safety"]
)

# -----------------------------------------
# REPAIR CANDIDATE RANKING
# -----------------------------------------

ranked_candidates = rank_repair_candidates(
    rules,
    repair_candidates,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
)


print("\nRepair Candidate Ranking")
print("--------------------------------------------")


for index, item in enumerate(
    ranked_candidates,
    start=1
):

    candidate = item["candidate"]

    print(
        f"{index}. "
        f"{candidate['action']} | "
        f"{candidate['target_rule']}"
    )

    print(
        f"   Score: "
        f"{item['score']}"
    )

    print(
        f"   Conflicts: "
        f"{item['conflicts_before']} "
        f"-> "
        f"{item['conflicts_after']}"
    )

    print(
        f"   Completeness: "
        f"{item['completeness_before']}% "
        f"-> "
        f"{item['completeness_after']}%"
    )

    print(
        f"   Verification: "
        f"{'SUCCESS' if item['repair_success'] else 'FAILED'}"
    )

    print()
# -----------------------------------------
# BEHAVIOR-AWARE REPAIR SELECTION
# -----------------------------------------

behavior_aware_selection = select_behaviorally_safe_repairs(
    rules,
    ranked_candidates,
    variable_ranges,
    result["consistency"]["conflicts"],
    resolution=50,
    activation_threshold=0.7
)

print("\nBehavior-Aware Repair Selection")
print("--------------------------------------------")

print(
    "Structurally successful candidates evaluated:",
    behavior_aware_selection["evaluated_candidate_count"]
)

print(
    "Behaviorally safe candidates:",
    behavior_aware_selection["safe_candidate_count"]
)

if behavior_aware_selection["safe_candidate_count"] == 0:

    print(
        "Selection result:",
        "NO BEHAVIORALLY SAFE CANDIDATE"
    )

else:

    print(
        "Behaviorally safe candidates:"
    )

    for index, item in enumerate(
        behavior_aware_selection["safe_candidates"],
        start=1
    ):

        candidate = item["candidate"]

        print(
            f"{index}. "
            f"{candidate['action']} | "
            f"{candidate['target_rule']}"
        )

        print(
            f"   Ranking score: "
            f"{item['score']}"
        )

        print(
            "   Collateral behavior changes:",
            item["behavioral_validation"]
            ["collateral_change_count"]
        )

        print(
            "   Decision:",
            "BEHAVIORALLY ACCEPTABLE"
        )

# -----------------------------------------
# CONTROLLED DEFECT INJECTION EXPERIMENT
# -----------------------------------------

defective_rules, defect_info = inject_consequent_conflict(
    clean_rules,
    target_rule_id="R4",
    conflicting_consequent="risk_high"
)


print("\nControlled Defect Injection Experiment")
print("--------------------------------------------")

print(
    "Defect type:",
    defect_info["defect_type"]
)

print(
    "Target rule:",
    defect_info["target_rule"]
)

print(
    "Original consequent:",
    defect_info["original_consequent"]
)

print(
    "Injected consequent:",
    defect_info["injected_consequent"]
)


# -----------------------------------------
# VERIFY CLEAN BASELINE
# -----------------------------------------

clean_result = verify_rule_base(
    clean_rules,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
)


print("\nClean Baseline Verification")
print("--------------------------------------------")

print(
    "Conflicts:",
    clean_result["consistency"]["conflict_count"]
)

print(
    "Completeness:",
    clean_result["completeness"]["score"],
    "%"
)

print(
    "Overall status:",
    clean_result["overall_status"]
)


# -----------------------------------------
# VERIFY DEFECTIVE BASELINE
# -----------------------------------------

defective_result = verify_rule_base(
    defective_rules,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
)


print("\nDefective Rule Base Verification")
print("--------------------------------------------")

print(
    "Rules analyzed:",
    defective_result["rules_analyzed"]
)

print(
    "Conflicts:",
    defective_result["consistency"]["conflict_count"]
)

print(
    "Completeness:",
    defective_result["completeness"]["score"],
    "%"
)

print(
    "Overall status:",
    defective_result["overall_status"]
)
# -----------------------------------------
# BENCHMARK CASE 001
# -----------------------------------------

benchmark_case = create_benchmark_case(
    case_id="CASE-001",

    clean_rules=clean_rules,

    defect_type="CONSEQUENT_CONFLICT",

    target_rule="R4",

    original_value="risk_medium",

    injected_value="risk_high",

    expected_repair_action="CHANGE_CONSEQUENT"
)


print("\nBenchmark Case")
print("--------------------------------------------")

print(
    "Case ID:",
    benchmark_case["case_id"]
)

print(
    "Defect type:",
    benchmark_case["defect"]["type"]
)

print(
    "Target rule:",
    benchmark_case["defect"]["target_rule"]
)

print(
    "Original value:",
    benchmark_case["defect"]["original_value"]
)

print(
    "Injected value:",
    benchmark_case["defect"]["injected_value"]
)

print(
    "Expected repair:",
    benchmark_case["ground_truth"]["repair_action"]
)

print(
    "Expected target:",
    benchmark_case["ground_truth"]["target_rule"]
)

print(
    "Expected value:",
    benchmark_case["ground_truth"]["correct_value"]
)

# ============================================================
# STEP 27: AUTOMATED BENCHMARK EVALUATION
# ============================================================

benchmark_evaluation = evaluate_benchmark_case(
    benchmark_case,
    defective_rules,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
)

print("\nAutomated Benchmark Evaluation")
print("--------------------------------------------")

print(
    "Case ID:",
    benchmark_evaluation["case_id"]
)

print(
    "Defect detected:",
    benchmark_evaluation["evaluation"]
    ["defect_detected"]
)

print(
    "Predicted localized rule:",
    benchmark_evaluation["prediction"]
    ["localized_rule"]
)

print(
    "Actual defective rule:",
    benchmark_evaluation["ground_truth"]
    ["target_rule"]
)

print(
    "Localization correct:",
    benchmark_evaluation["evaluation"]
    ["localization_correct"]
)

print(
    "Predicted repair:",
    benchmark_evaluation["prediction"]
    ["repair_action"]
)

print(
    "Expected repair:",
    benchmark_evaluation["ground_truth"]
    ["repair_action"]
)

print(
    "Predicted repair target:",
    benchmark_evaluation["prediction"]
    ["repair_target"]
)

print(
    "Expected repair target:",
    benchmark_evaluation["ground_truth"]
    ["target_rule"]
)

print(
    "Predicted repair value:",
    benchmark_evaluation["prediction"]
    ["repair_value"]
)

print(
    "Expected repair value:",
    benchmark_evaluation["ground_truth"]
    ["correct_value"]
)

print(
    "Repair prediction correct:",
    benchmark_evaluation["evaluation"]
    ["repair_prediction_correct"]
)
# ============================================================
# STEP 29: MULTI-CASE BENCHMARK EVALUATION
# ============================================================

benchmark_results = []

# ------------------------------------------------------------
# CASE 001
# R4 is intentionally corrupted
# ------------------------------------------------------------

case_001 = run_benchmark_case(
    case_id="CASE-001",
    clean_rules=clean_rules,
    variable_ranges=variable_ranges,
    target_rule="R4",
    conflicting_consequent="risk_high",
    expected_repair_action="CHANGE_CONSEQUENT"
)

benchmark_results.append(case_001)


# ------------------------------------------------------------
# CASE 002
# R2 is intentionally corrupted
# ------------------------------------------------------------

case_002 = run_benchmark_case(
    case_id="CASE-002",
    clean_rules=clean_rules,
    variable_ranges=variable_ranges,
    target_rule="R2",
    conflicting_consequent="risk_high",
    expected_repair_action="CHANGE_CONSEQUENT"
)

benchmark_results.append(case_002)


# ------------------------------------------------------------
# CASE 003
# R4 is corrupted with a different consequent
# ------------------------------------------------------------

case_003 = run_benchmark_case(
    case_id="CASE-003",
    clean_rules=clean_rules,
    variable_ranges=variable_ranges,
    target_rule="R4",
    conflicting_consequent="risk_low",
    expected_repair_action="CHANGE_CONSEQUENT"
)

benchmark_results.append(case_003)


# ------------------------------------------------------------
# CASE 004
# R2 is corrupted with another conflicting consequent
# ------------------------------------------------------------

case_004 = run_benchmark_case(
    case_id="CASE-004",
    clean_rules=clean_rules,
    variable_ranges=variable_ranges,
    target_rule="R2",
    conflicting_consequent="risk_low",
    expected_repair_action="CHANGE_CONSEQUENT"
)

benchmark_results.append(case_004)


# ------------------------------------------------------------
# AGGREGATE RESULTS
# ------------------------------------------------------------

benchmark_metrics = aggregate_benchmark_results(
    benchmark_results
)


print("\nMulti-Case Benchmark Evaluation")
print("--------------------------------------------")

print(
    "Total cases:",
    benchmark_metrics["total_cases"]
)

print(
    "Detection accuracy:",
    round(
        benchmark_metrics["detection_accuracy"],
        2
    ),
    "%"
)

print(
    "Localization accuracy:",
    round(
        benchmark_metrics["localization_accuracy"],
        2
    ),
    "%"
)

print(
    "Repair action accuracy:",
    round(
        benchmark_metrics["repair_action_accuracy"],
        2
    ),
    "%"
)

print(
    "Repair target accuracy:",
    round(
        benchmark_metrics["repair_target_accuracy"],
        2
    ),
    "%"
)

print(
    "Repair value accuracy:",
    round(
        benchmark_metrics["repair_value_accuracy"],
        2
    ),
    "%"
)

print(
    "Repair success rate:",
    round(
        benchmark_metrics["repair_success_rate"],
        2
    ),
    "%"
)
localization_metrics = calculate_localization_metrics(
    benchmark_results
)

print("\nLocalization Metrics")
print("--------------------------------------------")
print(
    "True positives:",
    localization_metrics["true_positive"]
)
print(
    "False positives:",
    localization_metrics["false_positive"]
)
print(
    "False negatives:",
    localization_metrics["false_negative"]
)
print(
    "Precision:",
    localization_metrics["precision"],
    "%"
)
print(
    "Recall:",
    localization_metrics["recall"],
    "%"
)
print(
    "F1-score:",
    localization_metrics["f1_score"],
    "%"
)
tie_aware_metrics = evaluate_tie_aware_localization(
    benchmark_results
)

print("\nTie-Aware Localization")
print("--------------------------------------------")
print(
    "Candidate-set accuracy:",
    tie_aware_metrics["candidate_set_accuracy"],
    "%"
)
print(
    "Ambiguous case rate:",
    tie_aware_metrics["ambiguous_case_rate"],
    "%"
)

print("\nCase-level results")

for case in tie_aware_metrics["case_results"]:
    print(
        case["case_id"],
        "| actual =", case["actual_rule"],
        "| candidates =", case["top_candidates"],
        "| correct =", case["correct_in_candidate_set"],
        "| ambiguous =", case["ambiguous"]
    )
    print("\nControlled Similarity Experiment")
print("--------------------------------------------")

base_set = TriangularFuzzySet(
    "base",
    20,
    40,
    60
)

shifts = [
    -20,
    -15,
    -10,
    -5,
    0,
    5,
    10,
    15,
    20
]

shifted_sets = generate_shifted_fuzzy_sets(
    base_set,
    shifts
)

similarity_results = calculate_similarity_experiment(
    base_set,
    shifted_sets,
    0,
    100
)

print("\nMeasured fuzzy-set similarity")

for result in similarity_results:
    print(
        result["set"],
        "| shift =",
        round(result["a"] - base_set.a, 2),
        "| similarity =",
        result["similarity"]
    )

thresholds = [
    0.5,
    0.6,
    0.7,
    0.8,
    0.9
]

threshold_evaluations = evaluate_thresholds(
    similarity_results,
    thresholds
)

print("\nThreshold detection")

for threshold in thresholds:
    print(
        "\nThreshold:",
        threshold
    )

    for evaluation in threshold_evaluations:
        if evaluation["threshold"] == threshold:
            print(
                "  ",
                evaluation["set"],
                "| similarity =",
                evaluation["similarity"],
                "| detected =",
                evaluation["detected"]
            )
print("--------------------------------------------")
# Step 32: Controlled Similarity Experiment

# ... your existing Step 32 code ...

# Actual Rule-Pair Verification Experiment
print("\nActual Rule-Pair Verification Experiment")
print("--------------------------------------------")

rule_pair_results = evaluate_generated_rule_pairs(
    base_set,
    shifted_sets,
    0,
    100,
    thresholds
)

for threshold in thresholds:
    print(
        "\nThreshold:",
        threshold
    )

    for result in rule_pair_results:
        if result["threshold"] == threshold:
            print(
                "  ",
                result["set"],
                "| shift =",
                result["shift"],
                "| similarity =",
                result["similarity"],
                "| conflict =",
                result["conflict_score"],
                "| detected =",
                result["detected"]
            )
print("\nControlled Defect Severity Benchmark")
print("--------------------------------------------")

severity_shifts = [
    -20,
    -15,
    -10,
    -5,
    0,
    5,
    10,
    15,
    20
]

severity_results = evaluate_defect_severity(
    clean_rules,
    variable_ranges,
    target_rule_id="R4",
    variable="temperature",
    shifts=severity_shifts,
    conflicting_consequent="risk_high",
    consistency_threshold=0.7,
    completeness_resolution=100
)

for result in severity_results:
    print(
        "shift =",
        result["shift"],
        "| similarity =",
        result["antecedent_similarity"],
        "| conflict =",
        result["conflict_score"],
        "| detected =",
        result["conflict_detected"],
        "| top_rule =",
        result["top_localized_rule"],
        "| repairs =",
        result["repair_candidate_count"],
        "| successful_repairs =",
        result["successful_repair_count"],
        "| status =",
        result["overall_status"]
    )
print("\nActivation-Aware Conflict Diagnosis")
print("--------------------------------------------")

conflicts = verification_result["consistency"]["conflicts"]

diagnoses = diagnose_activation_conflicts(
    rules,
    conflicts,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50
)

for diagnosis in diagnoses:
    print(
        "Conflict:",
        diagnosis["rule_1"],
        "<->",
        diagnosis["rule_2"]
    )

    print(
        "Reason:",
        diagnosis["reason"]
    )

    print(
        "Diagnostic points:",
        len(diagnosis["diagnostic_points"])
    )

    for point in diagnosis["diagnostic_points"]:
        print(
            point["inputs"],
            "| activation_1 =",
            point["activation_1"],
            "| activation_2 =",
            point["activation_2"],
            "| consequents =",
            point["consequent_1"],
            "vs",
            point["consequent_2"]
        )
print("\nActivation-Overlap Topology Characterization")
print("--------------------------------------------")

overlap_results = characterize_conflict_overlaps(
    rules,
    conflicts,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50
)

for result in overlap_results:
    print(
        "Conflict:",
        result["rule_1"],
        "<->",
        result["rule_2"]
    )
    print("Reason:", result["reason"])
    print("Connected components:", result["component_count"])

    for index, component in enumerate(
        result["components"],
        start=1
    ):
        print(
            "Component",
            index,
            "| points =",
            component["point_count"],
            "| max joint activation =",
            component["maximum_joint_activation"]
        )
        print(
            "Bounds:",
            component["bounds"]
        )
        print(
            "Representative point:",
            component["representative_point"]
        )