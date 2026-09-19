import numpy as np


def fuzzy_set_similarity(
    set_a,
    set_b,
    xmin,
    xmax,
    steps=1000
):
    """
    Calculates Jaccard-style similarity
    between two fuzzy sets using numerical
    integration.
    """

    xs = np.linspace(xmin, xmax, steps)

    a_values = np.array([
        set_a.membership(x)
        for x in xs
    ])

    b_values = np.array([
        set_b.membership(x)
        for x in xs
    ])

    # Fuzzy intersection = minimum
    intersection = np.minimum(
        a_values,
        b_values
    )

    # Fuzzy union = maximum
    union = np.maximum(
        a_values,
        b_values
    )

    # Numerical integration
    intersection_area = np.trapz(
        intersection,
        xs
    )

    union_area = np.trapz(
        union,
        xs
    )

    if union_area == 0:
        return 0.0

    return intersection_area / union_area


def rule_antecedent_similarity(
    rule_a,
    rule_b,
    variable_ranges
):
    """
    Calculates average similarity between
    the antecedent fuzzy sets of two rules.
    """

    variables = (
        set(rule_a.antecedent.keys())
        &
        set(rule_b.antecedent.keys())
    )

    if not variables:
        return 0.0

    similarities = []

    for variable in variables:

        fuzzy_a = rule_a.antecedent[variable]
        fuzzy_b = rule_b.antecedent[variable]

        xmin, xmax = variable_ranges[variable]

        similarity = fuzzy_set_similarity(
            fuzzy_a,
            fuzzy_b,
            xmin,
            xmax
        )

        similarities.append(similarity)

    return float(np.mean(similarities))


def consequent_similarity(
    rule_a,
    rule_b
):
    """
    Returns 1 when consequents are identical
    and 0 when they are different.
    """

    if rule_a.consequent == rule_b.consequent:
        return 1.0

    return 0.0