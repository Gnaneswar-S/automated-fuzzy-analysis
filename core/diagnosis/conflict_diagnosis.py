import numpy as np


def diagnose_conflict_region(
    rule_a,
    rule_b,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50
):
    """
    Identifies input points where two conflicting rules
    are simultaneously strongly active.
    """

    if rule_a.consequent == rule_b.consequent:
        return {
            "rule_1": rule_a.rule_id,
            "rule_2": rule_b.rule_id,
            "conflict": False,
            "reason": "Rules have identical consequents.",
            "diagnostic_points": []
        }

    variables = list(variable_ranges.keys())

    axes = []

    for variable in variables:
        minimum, maximum = variable_ranges[variable]

        axes.append(
            np.linspace(
                minimum,
                maximum,
                resolution
            )
        )

    mesh = np.meshgrid(
        *axes,
        indexing="ij"
    )

    points = np.stack(
        [
            axis.flatten()
            for axis in mesh
        ],
        axis=-1
    )

    diagnostic_points = []

    for point in points:

        inputs = {
            variables[i]: float(point[i])
            for i in range(len(variables))
        }

        activation_a = rule_a.membership(inputs)
        activation_b = rule_b.membership(inputs)

        if (
            activation_a >= activation_threshold
            and activation_b >= activation_threshold
        ):
            diagnostic_points.append({
                "inputs": inputs,
                "activation_1": round(
                    activation_a,
                    4
                ),
                "activation_2": round(
                    activation_b,
                    4
                ),
                "consequent_1": rule_a.consequent,
                "consequent_2": rule_b.consequent
            })

    return {
        "rule_1": rule_a.rule_id,
        "rule_2": rule_b.rule_id,
        "conflict": len(diagnostic_points) > 0,
        "reason": (
            "Both rules are simultaneously strongly active "
            "with different consequents."
            if diagnostic_points
            else
            "No strongly overlapping activation region found."
        ),
        "diagnostic_points": diagnostic_points
    }


def diagnose_conflicts(
    rules,
    conflicts,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50
):
    """
    Performs activation-aware diagnosis for all
    previously detected conflicts.
    """

    rule_lookup = {
        rule.rule_id: rule
        for rule in rules
    }

    diagnoses = []

    for conflict in conflicts:

        rule_1_id = conflict["rule_1"]
        rule_2_id = conflict["rule_2"]

        rule_a = rule_lookup[rule_1_id]
        rule_b = rule_lookup[rule_2_id]

        diagnosis = diagnose_conflict_region(
            rule_a,
            rule_b,
            variable_ranges,
            activation_threshold=activation_threshold,
            resolution=resolution
        )

        diagnoses.append(diagnosis)

    return diagnoses
