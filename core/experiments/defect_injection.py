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
def inject_multiple_defects(
    rules,
    defects
):
    """
    Creates a defective copy of the rule base by applying
    multiple controlled consequent mutations.

    The original rule base is never modified.

    Parameters
    ----------
    rules : list
        Clean fuzzy rule base.

    defects : list of dict
        Each defect must contain:
            target_rule
            conflicting_consequent

    Returns
    -------
    defective_rules : list
        Deep-copied rule base containing all injected defects.

    defect_info : list of dict
        Ground-truth information for every injected defect.
    """

    defective_rules = deepcopy(rules)

    rule_lookup = {
        rule.rule_id: rule
        for rule in defective_rules
    }

    defect_info = []

    for defect in defects:

        target_rule_id = defect["target_rule"]
        conflicting_consequent = defect[
            "conflicting_consequent"
        ]

        if target_rule_id not in rule_lookup:
            raise ValueError(
                f"Rule '{target_rule_id}' not found."
            )

        target_rule = rule_lookup[target_rule_id]

        original_consequent = target_rule.consequent

        if original_consequent == conflicting_consequent:
            raise ValueError(
                f"Injected consequent for rule "
                f"'{target_rule_id}' is identical to "
                f"its original consequent."
            )

        target_rule.consequent = conflicting_consequent

        defect_info.append({
            "defect_type": "CONSEQUENT_CONFLICT",
            "target_rule": target_rule_id,
            "original_consequent": original_consequent,
            "injected_consequent": conflicting_consequent
        })

    return defective_rules, defect_info
