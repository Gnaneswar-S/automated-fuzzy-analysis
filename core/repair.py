from copy import deepcopy


def generate_repair_candidates(
    rules,
    conflicts
):
    """
    Generates possible repair candidates for
    detected rule conflicts.

    Repairs are proposed but NOT automatically applied.
    """

    candidates = []

    for conflict in conflicts:

        rule_1_id = conflict["rule_1"]
        rule_2_id = conflict["rule_2"]

        rule_1 = next(
            rule for rule in rules
            if rule.rule_id == rule_1_id
        )

        rule_2 = next(
            rule for rule in rules
            if rule.rule_id == rule_2_id
        )

        # -----------------------------------------
        # CANDIDATE 1: REMOVE RULE 1
        # -----------------------------------------

        candidates.append({
            "conflict":
                f"{rule_1_id} <-> {rule_2_id}",

            "action":
                "REMOVE_RULE",

            "target_rule":
                rule_1_id,

            "description":
                f"Remove {rule_1_id} from the rule base."
        })

        # -----------------------------------------
        # CANDIDATE 2: REMOVE RULE 2
        # -----------------------------------------

        candidates.append({
            "conflict":
                f"{rule_1_id} <-> {rule_2_id}",

            "action":
                "REMOVE_RULE",

            "target_rule":
                rule_2_id,

            "description":
                f"Remove {rule_2_id} from the rule base."
        })

        # -----------------------------------------
        # CANDIDATE 3: CHANGE RULE 1 CONSEQUENT
        # -----------------------------------------

        candidates.append({
            "conflict":
                f"{rule_1_id} <-> {rule_2_id}",

            "action":
                "CHANGE_CONSEQUENT",

            "target_rule":
                rule_1_id,

            "new_consequent":
                rule_2.consequent,

            "description":
                f"Change {rule_1_id} consequent "
                f"from '{rule_1.consequent}' "
                f"to '{rule_2.consequent}'."
        })

        # -----------------------------------------
        # CANDIDATE 4: CHANGE RULE 2 CONSEQUENT
        # -----------------------------------------

        candidates.append({
            "conflict":
                f"{rule_1_id} <-> {rule_2_id}",

            "action":
                "CHANGE_CONSEQUENT",

            "target_rule":
                rule_2_id,

            "new_consequent":
                rule_1.consequent,

            "description":
                f"Change {rule_2_id} consequent "
                f"from '{rule_2.consequent}' "
                f"to '{rule_1.consequent}'."
        })

    return candidates