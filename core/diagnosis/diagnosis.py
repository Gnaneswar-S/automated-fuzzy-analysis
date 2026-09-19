def diagnose_conflicts(
    rules,
    conflicts,
    conflict_regions
):
    """
    Produces an explainable diagnosis for
    detected fuzzy-rule conflicts.
    """

    diagnoses = []

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

        related_regions = [
            region
            for region in conflict_regions
            if (
                region["rule_1"] == rule_1_id
                and
                region["rule_2"] == rule_2_id
            )
            or (
                region["rule_1"] == rule_2_id
                and
                region["rule_2"] == rule_1_id
            )
        ]

        diagnosis = {
            "rule_1": rule_1_id,
            "rule_2": rule_2_id,

            "conflict_score":
                conflict["conflict_score"],

            "consequent_1":
                rule_1.consequent,

            "consequent_2":
                rule_2.consequent,

            "reason": (
                "The rules have highly similar "
                "antecedent conditions but different "
                "consequents."
            ),

            "conflict_region_count":
                len(related_regions),

            "conflict_regions":
                related_regions,

            "severity":
                (
                    "HIGH"
                    if conflict["conflict_score"] >= 0.9
                    else "MEDIUM"
                )
        }

        diagnoses.append(diagnosis)

    return diagnoses