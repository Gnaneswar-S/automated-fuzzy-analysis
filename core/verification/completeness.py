import numpy as np


def generate_input_grid(
    variable_ranges,
    resolution=30
):
    """
    Generates a grid covering the complete
    input space.
    """

    variables = list(
        variable_ranges.keys()
    )

    axes = [
        np.linspace(
            variable_ranges[variable][0],
            variable_ranges[variable][1],
            resolution
        )
        for variable in variables
    ]

    mesh = np.meshgrid(
        *axes,
        indexing="ij"
    )

    points = np.stack(
        [axis.flatten() for axis in mesh],
        axis=-1
    )

    return variables, points


def calculate_point_coverage(
    rules,
    inputs,
    activation_threshold=0.0
):
    """
    Determines whether at least one rule
    covers a particular input point.
    """

    maximum_activation = max(
        (
            rule.membership(inputs)
            for rule in rules
        ),
        default=0.0
    )

    return (
        maximum_activation
        > activation_threshold
    )


def calculate_completeness(
    rules,
    variable_ranges,
    resolution=30,
    activation_threshold=0.0
):
    """
    Calculates global rule-base coverage.

    Boundary points are excluded from the
    coverage denominator because triangular
    membership functions naturally evaluate
    to zero at their exact endpoints.
    """

    variables, points = generate_input_grid(
        variable_ranges,
        resolution
    )

    covered_points = 0
    valid_points = 0

    for point in points:

        inputs = {
            variables[i]: point[i]
            for i in range(len(variables))
        }

        # Ignore exact domain boundaries
        # for coverage scoring.
        is_boundary = False

        for variable in variables:

            value = inputs[variable]

            minimum, maximum = (
                variable_ranges[variable]
            )

            if (
                np.isclose(value, minimum)
                or
                np.isclose(value, maximum)
            ):
                is_boundary = True
                break

        if is_boundary:
            continue

        valid_points += 1

        covered = calculate_point_coverage(
            rules,
            inputs,
            activation_threshold
        )

        if covered:
            covered_points += 1

    if valid_points == 0:
        return 0.0

    return (
        covered_points
        / valid_points
        * 100
    )


def find_uncovered_regions(
    rules,
    variable_ranges,
    resolution=30,
    activation_threshold=0.0
):
    """
    Finds genuine interior regions that are
    not covered by any fuzzy rule.
    """

    variables, points = generate_input_grid(
        variable_ranges,
        resolution
    )

    uncovered = []

    for point in points:

        inputs = {
            variables[i]: point[i]
            for i in range(len(variables))
        }

        # Ignore exact boundaries.
        is_boundary = False

        for variable in variables:

            value = inputs[variable]

            minimum, maximum = (
                variable_ranges[variable]
            )

            if (
                np.isclose(value, minimum)
                or
                np.isclose(value, maximum)
            ):
                is_boundary = True
                break

        if is_boundary:
            continue

        covered = calculate_point_coverage(
            rules,
            inputs,
            activation_threshold
        )

        if not covered:
            uncovered.append(inputs)

    return uncovered