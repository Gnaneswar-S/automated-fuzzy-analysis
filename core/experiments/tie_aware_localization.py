def evaluate_tie_aware_localization(results):
    """
    Evaluates whether the actual defective rule
    appears among the highest-suspicion rules.

    This handles symmetric ambiguity where multiple
    rules receive the same suspicion score.
    """

    total_cases = len(results)
    correct_candidate_set = 0
    ambiguous_cases = 0

    case_results = []

    for result in results:
        evaluation = result["evaluation"]

        actual_rule = (
            evaluation["ground_truth"]["target_rule"]
        )

        localization = evaluation["localization"]

        if not localization:
            case_results.append({
                "case_id": result["benchmark_case"]["case_id"],
                "actual_rule": actual_rule,
                "top_candidates": [],
                "correct_in_candidate_set": False,
                "ambiguous": False
            })
            continue

        highest_score = localization[0]["suspicion_score"]

        top_candidates = [
            item["rule_id"]
            for item in localization
            if item["suspicion_score"] == highest_score
        ]

        correct = actual_rule in top_candidates

        if correct:
            correct_candidate_set += 1

        if len(top_candidates) > 1:
            ambiguous_cases += 1

        case_results.append({
            "case_id": result["benchmark_case"]["case_id"],
            "actual_rule": actual_rule,
            "top_candidates": top_candidates,
            "correct_in_candidate_set": correct,
            "ambiguous": len(top_candidates) > 1
        })

    accuracy = (
        correct_candidate_set / total_cases * 100
        if total_cases > 0
        else 0.0
    )

    ambiguity_rate = (
        ambiguous_cases / total_cases * 100
        if total_cases > 0
        else 0.0
    )

    return {
        "total_cases": total_cases,
        "candidate_set_accuracy": round(accuracy, 2),
        "ambiguous_case_rate": round(ambiguity_rate, 2),
        "case_results": case_results
    }