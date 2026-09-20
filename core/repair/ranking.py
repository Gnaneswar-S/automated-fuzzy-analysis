def calculate_repair_score(
    candidate,
    before_result,
    after_result
):
    """
    Calculates a transparent ranking score for a repair candidate.

    Higher score = more desirable repair.

    Current criteria:
    1. Conflict resolution
    2. Completeness preservation
    3. Structural preservation
    4. Repair simplicity
    """

    conflicts_before = (
        before_result["consistency"]["conflict_count"]
    )

    conflicts_after = (
        after_result["consistency"]["conflict_count"]
    )

    completeness_before = (
        before_result["completeness"]["score"]
    )

    completeness_after = (
        after_result["completeness"]["score"]
    )

    # -----------------------------------------
    # 1. CONFLICT RESOLUTION
    # -----------------------------------------

    if conflicts_before == 0:
        conflict_resolution = 0.0
    else:
        conflict_resolution = (
            conflicts_before - conflicts_after
        ) / conflicts_before

    # -----------------------------------------
    # 2. COMPLETENESS PRESERVATION
    # -----------------------------------------

    completeness_preservation = (
        completeness_after / completeness_before
        if completeness_before > 0
        else 0.0
    )

    completeness_preservation = min(
        completeness_preservation,
        1.0
    )

    # -----------------------------------------
    # 3. STRUCTURAL PRESERVATION
    # -----------------------------------------

    action = candidate["action"]

    if action == "CHANGE_CONSEQUENT":
        structural_preservation = 1.0

    elif action == "REMOVE_RULE":
        structural_preservation = 0.5

    else:
        structural_preservation = 0.0

    # -----------------------------------------
    # 4. REPAIR SIMPLICITY
    # -----------------------------------------

    if action == "CHANGE_CONSEQUENT":
        repair_simplicity = 1.0

    elif action == "REMOVE_RULE":
        repair_simplicity = 0.5

    else:
        repair_simplicity = 0.0

    # -----------------------------------------
    # WEIGHTED SCORE
    # -----------------------------------------

    score = (
        0.40 * conflict_resolution
        + 0.30 * completeness_preservation
        + 0.20 * structural_preservation
        + 0.10 * repair_simplicity
    )

    return {
        "conflict_resolution": round(
            conflict_resolution, 4
        ),

        "completeness_preservation": round(
            completeness_preservation, 4
        ),

        "structural_preservation": round(
            structural_preservation, 4
        ),

        "repair_simplicity": round(
            repair_simplicity, 4
        ),

        "ranking_score": round(
            score, 4
        )
    }


def rank_repair_candidates(
    rules,
    candidates,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100
):
    """
    Applies and evaluates every repair candidate
    independently, then ranks them.

    Original rule base is never modified.
    """

    from .repair_engine import (
        evaluate_repair_candidate
    )

    ranked_candidates = []

    for candidate in candidates:

        evaluation = evaluate_repair_candidate(
            rules,
            candidate,
            variable_ranges,
            consistency_threshold=consistency_threshold,
            completeness_resolution=completeness_resolution
        )

        score_details = calculate_repair_score(
            candidate,
            evaluation["before"],
            evaluation["after"]
        )

        ranked_candidates.append({
            "candidate": candidate,

            "repaired_rules":
                evaluation["repaired_rules"],

            "score": score_details["ranking_score"],

            "conflicts_before":
                evaluation["before"]
                ["consistency"]
                ["conflict_count"],

            "conflicts_after":
                evaluation["after"]
                ["consistency"]
                ["conflict_count"],

            "completeness_before":
                evaluation["before"]
                ["completeness"]
                ["score"],

            "completeness_after":
                evaluation["after"]
                ["completeness"]
                ["score"],

            "repair_success":
                evaluation["comparison"]
                ["repair_success"],

            "score_details":
                score_details
        })

    ranked_candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_candidates