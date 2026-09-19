from copy import deepcopy


def inject_consequent_conflict(
    rules,
    target_rule_id,
    conflicting_consequent
):
    """
    Creates a defective copy of the rule base by
    changing the consequent of one selected rule.

    The original rule base is never modified.
    """

    defective_rules = deepcopy(rules)

    target_rule = None

    for rule in defective_rules:

        if rule.rule_id == target_rule_id:
            target_rule = rule
            break

    if target_rule is None:
        raise ValueError(
            f"Rule '{target_rule_id}' not found."
        )

    original_consequent = target_rule.consequent

    target_rule.consequent = conflicting_consequent

    return defective_rules, {
        "defect_type": "CONSEQUENT_CONFLICT",

        "target_rule": target_rule_id,

        "original_consequent":
            original_consequent,

        "injected_consequent":
            conflicting_consequent
    }