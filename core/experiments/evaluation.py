from ..verification.verification import verify_rule_base
from ..diagnosis.localization import calculate_rule_suspicion_scores
from ..repair.repair import generate_repair_candidates
from ..repair.ranking import rank_repair_candidates

def evaluate_benchmark_case(
    benchmark_case,
    defective_rules,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
):
    """
    Evaluates the automated fuzzy rule-base analysis
    against benchmark ground truth.
    """

    # --------------------------------------------------
    # 1. VERIFY DEFECTIVE RULE BASE
    # --------------------------------------------------

    verification_result = verify_rule_base(
        defective_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    # --------------------------------------------------
    # 2. RULE-LEVEL LOCALIZATION
    # --------------------------------------------------

    localization_result = calculate_rule_suspicion_scores(
        defective_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold
    )

    # --------------------------------------------------
    # 3. GENERATE REPAIR CANDIDATES
    # --------------------------------------------------

    repair_candidates = generate_repair_candidates(
        defective_rules,
        verification_result["consistency"]["conflicts"]
    )

    # --------------------------------------------------
    # 4. RANK REPAIR CANDIDATES
    # --------------------------------------------------

    ranked_candidates = rank_repair_candidates(
        defective_rules,
        repair_candidates,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    # --------------------------------------------------
    # 5. GROUND TRUTH
    # --------------------------------------------------

    ground_truth = benchmark_case["ground_truth"]

    target_rule = ground_truth["target_rule"]
    expected_action = ground_truth["repair_action"]
    correct_value = ground_truth["correct_value"]

    # --------------------------------------------------
    # 6. CHECK TOP LOCALIZED RULE
    # --------------------------------------------------

    predicted_rule = None

    if localization_result:
        predicted_rule = localization_result[0]["rule_id"]

    localization_correct = (
        predicted_rule == target_rule
    )

    # --------------------------------------------------
    # 7. CHECK TOP REPAIR CANDIDATE
    # --------------------------------------------------

    predicted_action = None
    predicted_target = None
    predicted_value = None

    if ranked_candidates:

        top_candidate = ranked_candidates[0]["candidate"]

        predicted_action = top_candidate["action"]
        predicted_target = top_candidate["target_rule"]

        if predicted_action == "CHANGE_CONSEQUENT":
            predicted_value = top_candidate["new_consequent"]

    repair_action_correct = (
        predicted_action == expected_action
    )

    repair_target_correct = (
        predicted_target == target_rule
    )

    repair_value_correct = (
        predicted_value == correct_value
    )

    # --------------------------------------------------
    # 8. OVERALL REPAIR PREDICTION
    # --------------------------------------------------

    repair_prediction_correct = (
        repair_action_correct
        and repair_target_correct
        and repair_value_correct
    )

    # --------------------------------------------------
    # 9. RETURN EVALUATION
    # --------------------------------------------------

    return {
        "case_id": benchmark_case["case_id"],

        "ground_truth": {
            "target_rule": target_rule,
            "repair_action": expected_action,
            "correct_value": correct_value
        },

        "prediction": {
            "localized_rule": predicted_rule,
            "repair_action": predicted_action,
            "repair_target": predicted_target,
            "repair_value": predicted_value
        },

        "evaluation": {
            "defect_detected": (
                verification_result["consistency"]
                ["conflict_count"] > 0
            ),

            "localization_correct":
                localization_correct,

            "repair_action_correct":
                repair_action_correct,

            "repair_target_correct":
                repair_target_correct,

            "repair_value_correct":
                repair_value_correct,

            "repair_prediction_correct":
                repair_prediction_correct
        },

        "verification": verification_result,

        "localization": localization_result,

        "ranked_candidates": ranked_candidates
    }