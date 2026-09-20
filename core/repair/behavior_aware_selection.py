from core.repair.behavioral_validation import evaluate_repair_behavior


def select_behaviorally_safe_repairs(
    original_rules,
    evaluated_candidates,
    variable_ranges,
    conflicts,
    resolution=50,
    activation_threshold=0.7,
    tolerance=1e-6
):
    """
    Selects repair candidates that satisfy both structural and behavioral
    safety constraints.

    Structural verification is NOT repeated here. The evaluated candidate
    results produced by the existing repair-evaluation/ranking stage are
    consumed directly.

    A candidate is behaviorally acceptable only when:
    1. Structural repair verification has already succeeded.
    2. No collateral behavioral change occurs outside the diagnosed
       conflict region.

    No composite score is introduced. Behavioral safety is treated as a
    constraint rather than another ranking criterion.
    """

    evaluated = []
    safe_candidates = []

    for item in evaluated_candidates:

        candidate = item["candidate"]

        # Reuse the structural verification result already produced by
        # evaluate_repair_candidate() through rank_repair_candidates().
        if not item["repair_success"]:
            continue

        behavioral_result = evaluate_repair_behavior(
            original_rules,
            item["repaired_rules"],
            variable_ranges,
            conflicts,
            resolution=resolution,
            activation_threshold=activation_threshold,
            tolerance=tolerance
        )

        if behavioral_result["collateral_change_count"] == 0:
            decision = "BEHAVIORALLY_ACCEPTABLE"
        else:
            decision = "BEHAVIORALLY_REJECTED"

        evaluation_record = {
            "candidate": candidate,
            "score": item["score"],
            "behavioral_validation": behavioral_result,
            "decision": decision
        }

        evaluated.append(evaluation_record)

        if decision == "BEHAVIORALLY_ACCEPTABLE":
            safe_candidates.append(evaluation_record)

    return {
        "evaluated_candidates": evaluated,
        "safe_candidates": safe_candidates,
        "safe_candidate_count": len(safe_candidates),
        "evaluated_candidate_count": len(evaluated)
    }
