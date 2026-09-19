import numpy as np
from collections import deque


def characterize_activation_overlap(
    rule_a,
    rule_b,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50
):
    """
    Characterizes the topology of the region where two rules
    are simultaneously strongly active.

    The input space is discretized into a regular grid.
    Strongly overlapping grid points are grouped into
    connected components using axis-adjacent connectivity.
    """

    if rule_a.consequent == rule_b.consequent:
        return {
            "rule_1": rule_a.rule_id,
            "rule_2": rule_b.rule_id,
            "components": [],
            "component_count": 0,
            "reason": "Rules have identical consequents."
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

    grid_shape = mesh[0].shape

    active_mask = np.zeros(
        grid_shape,
        dtype=bool
    )

    joint_activation = np.zeros(
        grid_shape,
        dtype=float
    )

    for index in np.ndindex(grid_shape):

        inputs = {
            variables[i]: float(
                axes[i][index[i]]
            )
            for i in range(len(variables))
        }

        activation_a = rule_a.membership(inputs)
        activation_b = rule_b.membership(inputs)

        joint_activation[index] = min(
            activation_a,
            activation_b
        )

        if (
            activation_a >= activation_threshold
            and activation_b >= activation_threshold
        ):
            active_mask[index] = True

    visited = np.zeros(
        grid_shape,
        dtype=bool
    )

    components = []

    for start in np.ndindex(grid_shape):

        if (
            not active_mask[start]
            or visited[start]
        ):
            continue

        queue = deque([start])
        visited[start] = True
        component_indices = []

        while queue:

            current = queue.popleft()
            component_indices.append(current)

            for dimension in range(len(variables)):

                for direction in (-1, 1):

                    neighbour = list(current)
                    neighbour[dimension] += direction

                    if (
                        neighbour[dimension] < 0
                        or neighbour[dimension] >= grid_shape[dimension]
                    ):
                        continue

                    neighbour = tuple(neighbour)

                    if (
                        active_mask[neighbour]
                        and not visited[neighbour]
                    ):
                        visited[neighbour] = True
                        queue.append(neighbour)

        component_points = []

        for index in component_indices:

            point = {
                variables[i]: float(
                    axes[i][index[i]]
                )
                for i in range(len(variables))
            }

            component_points.append(point)

        maximum_activation = max(
            joint_activation[index]
            for index in component_indices
        )

        representative_index = max(
            component_indices,
            key=lambda index: joint_activation[index]
        )

        representative_point = {
            variables[i]: float(
                axes[i][representative_index[i]]
            )
            for i in range(len(variables))
        }

        bounds = {}

        for i, variable in enumerate(variables):

            values = [
                axes[i][index[i]]
                for index in component_indices
            ]

            bounds[variable] = {
                "minimum": float(min(values)),
                "maximum": float(max(values))
            }

        components.append({
            "point_count": len(component_indices),
            "bounds": bounds,
            "maximum_joint_activation": round(
                float(maximum_activation),
                4
            ),
            "representative_point": representative_point
        })

    components.sort(
        key=lambda component: component["maximum_joint_activation"],
        reverse=True
    )

    return {
        "rule_1": rule_a.rule_id,
        "rule_2": rule_b.rule_id,
        "activation_threshold": activation_threshold,
        "resolution": resolution,
        "component_count": len(components),
        "components": components,
        "reason": (
            "Strong activation overlap forms "
            f"{len(components)} connected region(s)."
            if components
            else
            "No strongly overlapping activation region found."
        )
    }


def characterize_conflict_overlaps(
    rules,
    conflicts,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50
):
    """
    Characterizes activation-overlap topology for all
    previously detected conflicts.
    """

    rule_lookup = {
        rule.rule_id: rule
        for rule in rules
    }

    results = []

    for conflict in conflicts:

        rule_a = rule_lookup[conflict["rule_1"]]
        rule_b = rule_lookup[conflict["rule_2"]]

        result = characterize_activation_overlap(
            rule_a,
            rule_b,
            variable_ranges,
            activation_threshold=activation_threshold,
            resolution=resolution
        )

        results.append(result)

    return results