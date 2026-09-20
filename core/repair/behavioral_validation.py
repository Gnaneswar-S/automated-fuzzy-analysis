from collections import defaultdict

import numpy as np


def _evaluate_behavior(rules, inputs):
    """
    Builds a consequent activation-profile signature for a fuzzy rule base.

    Consequents are currently represented as categorical labels rather than
    output fuzzy sets. Therefore, behavior is represented by the strongest
    activation associated with each consequent at the given input.
    """

    consequent_activation = defaultdict(float)
    rule_activation = {}

    for rule in rules:
        activation = float(rule.membership(inputs))
        rule_activation[rule.rule_id] = activation
        consequent_activation[rule.consequent] = max(
            consequent_activation[rule.consequent],
            activation
        )

    return {
        "consequent_activation": dict(consequent_activation),
        "rule_activation": rule_activation,
    }


def _behavior_changed(before, after, tolerance=1e-6):
    """Returns whether the consequent activation profile changed."""

    consequents = (
        set(before["consequent_activation"])
        | set(after["consequent_activation"])
    )

    for consequent in consequents:
        before_value = before["consequent_activation"].get(
            consequent,
            0.0
        )
        after_value = after["consequent_activation"].get(
            consequent,
            0.0
        )

        if abs(before_value - after_value) > tolerance:
            return True

    return False


def _is_in_affected_region(
    rules,
    inputs,
    conflicts,
    activation_threshold
):
    """
    Determines whether an input belongs to a diagnosed conflict region.

    A point is affected when at least one previously detected conflicting
    pair simultaneously activates at or above the same activation threshold.
    """

    rule_lookup = {
        rule.rule_id: rule
        for rule in rules
    }

    for conflict in conflicts:
        rule_a = rule_lookup.get(conflict["rule_1"])
        rule_b = rule_lookup.get(conflict["rule_2"])

        if rule_a is None or rule_b is None:
            continue

        activation_a = rule_a.membership(inputs)
        activation_b = rule_b.membership(inputs)

        if (
            activation_a >= activation_threshold
            and activation_b >= activation_threshold
            and rule_a.consequent != rule_b.consequent
        ):
            return True

    return False


def validate_repair_behavior(
    original_rules,
    repaired_rules,
    variable_ranges,
    conflicts,
    resolution=50,
    activation_threshold=0.7,
    tolerance=1e-6
):
    """
    Compares original and repaired rule-base behavior over the input space.

    The validation separates behavioral changes inside the diagnosed conflict
    region from collateral changes outside it. This is intentionally distinct
    from structural re-verification: a repair can remove every detected
    conflict while still changing behavior in regions unrelated to the defect.
    """

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

    grid_shape = mesh[0].shape

    changed_points = []
    affected_changes = []
    collateral_changes = []
    unchanged_points = 0

    for index in np.ndindex(grid_shape):
        inputs = {
            variables[i]: float(axes[i][index[i]])
            for i in range(len(variables))
        }

        before = _evaluate_behavior(
            original_rules,
            inputs
        )
        after = _evaluate_behavior(
            repaired_rules,
            inputs
        )

        changed = _behavior_changed(
            before,
            after,
            tolerance=tolerance
        )

        if not changed:
            unchanged_points += 1
            continue

        affected = _is_in_affected_region(
            original_rules,
            inputs,
            conflicts,
            activation_threshold
        )

        change = {
            "inputs": inputs,
            "affected_region": affected,
            "before": before["consequent_activation"],
            "after": after["consequent_activation"],
        }

        changed_points.append(change)

        if affected:
            affected_changes.append(change)
        else:
            collateral_changes.append(change)

    if collateral_changes:
        safety = "COLLATERAL_CHANGE"
    elif affected_changes:
        safety = "LOCALIZED_CHANGE"
    else:
        safety = "NO_BEHAVIOR_CHANGE"

    return {
        "resolution": resolution,
        "activation_threshold": activation_threshold,
        "tolerance": tolerance,
        "grid_points": int(np.prod(grid_shape)),
        "changed_point_count": len(changed_points),
        "unchanged_point_count": unchanged_points,
        "affected_change_count": len(affected_changes),
        "collateral_change_count": len(collateral_changes),
        "repair_safety": safety,
        "changed_points": changed_points,
        "affected_changes": affected_changes,
        "collateral_changes": collateral_changes,
    }


def evaluate_repair_behavior(
    original_rules,
    repaired_rules,
    variable_ranges,
    conflicts,
    resolution=50,
    activation_threshold=0.7,
    tolerance=1e-6
):
    """
    Public wrapper for counterfactual repair-behavior validation.
    """

    return validate_repair_behavior(
        original_rules,
        repaired_rules,
        variable_ranges,
        conflicts,
        resolution=resolution,
        activation_threshold=activation_threshold,
        tolerance=tolerance
    )
