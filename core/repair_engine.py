from copy import deepcopy

from .verification import verify_rule_base


def apply_repair_candidate(rules, candidate):
    """
    Applies a repair candidate to a COPY of the rule base.

    The original rule base is never modified.
    """

    repaired_rules = deepcopy(rules)

    action = candidate["action"]
    target_rule = candidate["target_rule"]

    if action == "REMOVE_RULE":

        repaired_rules = [
            rule
            for rule in repaired_rules
            if rule.rule_id != target_rule
        ]

    elif action == "CHANGE_CONSEQUENT":

        new_consequent = candidate["new_consequent"]

        for rule in repaired_rules:

            if rule.rule_id == target_rule:
                rule.consequent = new_consequent
                break

    else:

        raise ValueError(
            f"Unsupported repair action: {action}"
        )

    return repaired_rules


def evaluate_repair_candidate(
    rules,
    candidate,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=100,
    activation_threshold=0.0
):
    """
    Applies a repair candidate to a copied rule base
    and mandatory re-verifies the repaired rule base.
    """

    # -----------------------------------------
    # BEFORE REPAIR
    # -----------------------------------------

    before = verify_rule_base(
        rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution,
        activation_threshold=activation_threshold
    )

    # -----------------------------------------
    # APPLY REPAIR
    # -----------------------------------------

    repaired_rules = apply_repair_candidate(
        rules,
        candidate
    )

    # -----------------------------------------
    # AFTER REPAIR
    # -----------------------------------------

    after = verify_rule_base(
        repaired_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution,
        activation_threshold=activation_threshold
    )

    # -----------------------------------------
    # COMPARISON
    # -----------------------------------------

    conflicts_before = (
        before["consistency"]["conflict_count"]
    )

    conflicts_after = (
        after["consistency"]["conflict_count"]
    )

    completeness_before = (
        before["completeness"]["score"]
    )

    completeness_after = (
        after["completeness"]["score"]
    )

    conflict_improved = (
        conflicts_after < conflicts_before
    )

    completeness_preserved = (
        completeness_after >= completeness_before
    )

    repair_success = (
        conflict_improved
        and completeness_preserved
    )

    return {
        "candidate": candidate,

        "before": before,

        "after": after,

        "repaired_rules": repaired_rules,

        "comparison": {
            "conflicts_before": conflicts_before,
            "conflicts_after": conflicts_after,

            "completeness_before": completeness_before,
            "completeness_after": completeness_after,

            "conflict_improved": conflict_improved,
            "completeness_preserved": completeness_preserved,

            "repair_success": repair_success
        }
    }