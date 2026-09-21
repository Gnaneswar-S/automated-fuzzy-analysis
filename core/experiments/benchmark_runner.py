from .evaluation import evaluate_benchmark_case
from .defect_injection import inject_consequent_conflict
from .benchmark import create_benchmark_case


def run_benchmark_case(
    case_id,
    clean_rules,
    variable_ranges,
    target_rule,
    conflicting_consequent,
    expected_repair_action,
    consistency_threshold=0.7,
    completeness_resolution=100
):
    """
    Creates, injects, evaluates, and returns
    one complete benchmark case.
    """

    # --------------------------------------------------
    # 1. INJECT DEFECT
    # --------------------------------------------------

    defective_rules, defect_info = inject_consequent_conflict(
        clean_rules,
        target_rule_id=target_rule,
        conflicting_consequent=conflicting_consequent
    )

    # --------------------------------------------------
    # 2. CREATE GROUND TRUTH
    # --------------------------------------------------

    benchmark_case = create_benchmark_case(
        case_id=case_id,
        clean_rules=clean_rules,
        defect_type=defect_info["defect_type"],
        target_rule=target_rule,
        original_value=defect_info["original_consequent"],
        injected_value=defect_info["injected_consequent"],
        expected_repair_action=expected_repair_action
    )

    # --------------------------------------------------
    # 3. EVALUATE
    # --------------------------------------------------

    evaluation = evaluate_benchmark_case(
        benchmark_case,
        defective_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    return {
        "benchmark_case": benchmark_case,
        "defect_info": defect_info,
        "evaluation": evaluation
    }


def aggregate_benchmark_results(results):
    """
    Aggregates benchmark results into quantitative metrics.
    """

    total_cases = len(results)

    if total_cases == 0:
        return {
            "total_cases": 0,
            "detection_accuracy": 0.0,
            "localization_accuracy": 0.0,
            "repair_action_accuracy": 0.0,
            "repair_target_accuracy": 0.0,
            "repair_value_accuracy": 0.0,
            "repair_success_rate": 0.0
        }

    detected = 0
    localized = 0
    action_correct = 0
    target_correct = 0
    value_correct = 0
    repair_correct = 0

    for result in results:

        evaluation = result["evaluation"]
        metrics = evaluation["evaluation"]

        if metrics["defect_detected"]:
            detected += 1

        if metrics["localization_correct"]:
            localized += 1

        if metrics["repair_action_correct"]:
            action_correct += 1

        if metrics["repair_target_correct"]:
            target_correct += 1

        if metrics["repair_value_correct"]:
            value_correct += 1

        if metrics["repair_prediction_correct"]:
            repair_correct += 1

    return {
        "total_cases": total_cases,

        "detection_accuracy":
            detected / total_cases * 100,

        "localization_accuracy":
            localized / total_cases * 100,

        "repair_action_accuracy":
            action_correct / total_cases * 100,

        "repair_target_accuracy":
            target_correct / total_cases * 100,

        "repair_value_accuracy":
            value_correct / total_cases * 100,

        "repair_success_rate":
            repair_correct / total_cases * 100
    }
def run_multi_defect_benchmark_case(
    case_id,
    clean_rules,
    variable_ranges,
    defects,
    expected_repairs,
    consistency_threshold=0.7,
    completeness_resolution=100
):
    """
    Creates and injects a multi-defect benchmark case.

    This infrastructure stage intentionally stops after
    controlled defect injection and structural verification.

    Full multi-defect localization and repair evaluation
    will be implemented separately in the Step 39 experiment.
    """

    from .defect_injection import inject_multiple_defects
    from .benchmark import create_multi_defect_benchmark_case
    from ..verification.verification import verify_rule_base

    defective_rules, defect_info = inject_multiple_defects(
        clean_rules,
        defects
    )

    benchmark_case = create_multi_defect_benchmark_case(
        case_id=case_id,
        clean_rules=clean_rules,
        defect_info=defect_info,
        expected_repairs=expected_repairs
    )

    verification = verify_rule_base(
        defective_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    return {
        "benchmark_case": benchmark_case,
        "defect_info": defect_info,
        "defective_rules": defective_rules,
        "verification": verification
    }
