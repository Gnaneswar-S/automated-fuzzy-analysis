import numpy as np


def _build_input_grid(variable_ranges, resolution):
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

    return variables, axes


def calculate_rule_activation_footprint(
    original_rules,
    repaired_rules,
    target_rule_id,
    variable_ranges,
    resolution=50,
    tolerance=1e-6
):
    """
    Measures the direct activation footprint of a changed rule.

    A grid point belongs to the footprint when the target rule's
    activation differs between the original and changed rule bases
    by more than the specified tolerance.
    """

    variables, axes = _build_input_grid(
        variable_ranges,
        resolution
    )

    original_lookup = {
        rule.rule_id: rule
        for rule in original_rules
    }

    repaired_lookup = {
        rule.rule_id: rule
        for rule in repaired_rules
    }

    if target_rule_id not in original_lookup:
        raise ValueError(
            f"Target rule '{target_rule_id}' not found in original rules."
        )

    if target_rule_id not in repaired_lookup:
        raise ValueError(
            f"Target rule '{target_rule_id}' not found in repaired rules."
        )

    original_rule = original_lookup[target_rule_id]
    repaired_rule = repaired_lookup[target_rule_id]

    mesh = np.meshgrid(
        *axes,
        indexing="ij"
    )

    grid_shape = mesh[0].shape

    changed_points = []
    unchanged_points = 0
    maximum_activation_delta = 0.0

    for index in np.ndindex(grid_shape):

        inputs = {
            variables[i]: float(
                axes[i][index[i]]
            )
            for i in range(len(variables))
        }

        original_activation = float(
            original_rule.membership(inputs)
        )

        repaired_activation = float(
            repaired_rule.membership(inputs)
        )

        delta = abs(
            original_activation
            - repaired_activation
        )

        maximum_activation_delta = max(
            maximum_activation_delta,
            delta
        )

        if delta > tolerance:
            changed_points.append({
                "inputs": inputs,
                "original_activation": original_activation,
                "repaired_activation": repaired_activation,
                "activation_delta": delta
            })
        else:
            unchanged_points += 1

    return {
        "target_rule": target_rule_id,
        "resolution": resolution,
        "tolerance": tolerance,
        "grid_points": int(np.prod(grid_shape)),
        "changed_point_count": len(changed_points),
        "unchanged_point_count": unchanged_points,
        "maximum_activation_delta": float(
            maximum_activation_delta
        ),
        "changed_points": changed_points
    }


def evaluate_behavioral_footprint_containment(
    behavioral_result,
    activation_footprint
):
    """
    Determines whether aggregate behavioral changes are contained
    within the direct activation footprint of the changed rule.
    """

    footprint_points = {
        tuple(
            sorted(
                point["inputs"].items()
            )
        )
        for point in activation_footprint["changed_points"]
    }

    behavioral_changes = behavioral_result["changed_points"]

    inside_changes = []
    outside_changes = []

    for change in behavioral_changes:

        point_key = tuple(
            sorted(
                change["inputs"].items()
            )
        )

        if point_key in footprint_points:
            inside_changes.append(change)
        else:
            outside_changes.append(change)

    total_changes = len(behavioral_changes)
    inside_count = len(inside_changes)
    outside_count = len(outside_changes)

    if total_changes == 0:
        containment_percentage = 100.0
    else:
        containment_percentage = (
            inside_count
            / total_changes
            * 100.0
        )

    status = (
        "PASS"
        if outside_count == 0
        else
        "REVIEW"
    )

    return {
        "behavioral_change_count": total_changes,
        "inside_footprint_count": inside_count,
        "outside_footprint_count": outside_count,
        "containment_percentage": containment_percentage,
        "footprint_containment": status,
        "inside_footprint_changes": inside_changes,
        "outside_footprint_changes": outside_changes
    }
