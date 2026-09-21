from collections import defaultdict

from ..diagnosis.localization import (
    calculate_rule_suspicion_scores
)


def calculate_conflict_count_ranking(
    rules,
    conflicts
):
    """
    Rank rules by the number of detected conflict
    pairs in which each rule participates.

    This is a simple conflict-participation baseline.
    It uses the same conflict set produced by the
    existing consistency detector.
    """

    conflict_counts = defaultdict(int)

    for conflict in conflicts:

        conflict_counts[
            conflict["rule_1"]
        ] += 1

        conflict_counts[
            conflict["rule_2"]
        ] += 1

    results = []

    for rule in rules:

        rule_id = rule.rule_id

        results.append({
            "rule_id": rule_id,
            "conflict_count":
                conflict_counts.get(
                    rule_id,
                    0
                )
        })

    results.sort(
        key=lambda item:
            item["conflict_count"],
        reverse=True
    )

    return results


def calculate_weighted_suspicion_ranking(
    rules,
    variable_ranges,
    consistency_threshold=0.7
):
    """
    Return the existing weighted suspicion ranking.

    The production localization implementation is reused
    directly so the baseline comparison does not alter it.
    """

    return calculate_rule_suspicion_scores(
        rules,
        variable_ranges,
        consistency_threshold=consistency_threshold
    )


def _ranking_position(
    ranking,
    target_rule,
    score_key
):
    """
    Return 1-based competition rank.

    Rules with the same score share the same rank.
    """

    target_score = None

    for item in ranking:

        if item["rule_id"] == target_rule:
            target_score = item[score_key]
            break

    if target_score is None:
        return None

    return (
        1
        + sum(
            1
            for item in ranking
            if item[score_key] > target_score
        )
    )


def _top_candidate_set(
    ranking,
    score_key
):
    """
    Return every rule tied at the highest score.
    """

    if not ranking:
        return []

    highest_score = ranking[0][score_key]

    return [
        item["rule_id"]
        for item in ranking
        if item[score_key] == highest_score
    ]


def compare_localization_methods(
    rules,
    conflicts,
    variable_ranges,
    target_rule,
    consistency_threshold=0.7
):
    """
    Compare conflict-count localization with the
    existing weighted suspicion localization.

    Both methods are evaluated against the same
    controlled ground-truth target rule.
    """

    count_ranking = calculate_conflict_count_ranking(
        rules,
        conflicts
    )

    weighted_ranking = calculate_weighted_suspicion_ranking(
        rules,
        variable_ranges,
        consistency_threshold=consistency_threshold
    )

    count_top_candidates = _top_candidate_set(
        count_ranking,
        "conflict_count"
    )

    weighted_top_candidates = _top_candidate_set(
        weighted_ranking,
        "suspicion_score"
    )

    return {
        "target_rule": target_rule,

        "conflict_count_baseline": {
            "ranking": count_ranking,
            "target_rank": _ranking_position(
                count_ranking,
                target_rule,
                "conflict_count"
            ),
            "top_candidates":
                count_top_candidates,
            "target_in_top_set":
                target_rule in count_top_candidates
        },

        "weighted_suspicion": {
            "ranking": weighted_ranking,
            "target_rank": _ranking_position(
                weighted_ranking,
                target_rule,
                "suspicion_score"
            ),
            "top_candidates":
                weighted_top_candidates,
            "target_in_top_set":
                target_rule in weighted_top_candidates
        }
    }
