import numpy as np
from collections import defaultdict

from .similarity import (
    rule_antecedent_similarity,
    consequent_similarity
)


def calculate_rule_suspicion_scores(
    rules,
    variable_ranges,
    consistency_threshold=0.7
):
    """
    Calculates a suspicion score for each rule.

    A rule receives a higher score when it participates
    in potentially conflicting rule pairs.

    The score is based on:
        - antecedent similarity
        - consequent disagreement
        - number of conflicts involving the rule
    """

    suspicion_scores = defaultdict(float)
    conflict_counts = defaultdict(int)

    for i in range(len(rules)):

        for j in range(i + 1, len(rules)):

            rule_a = rules[i]
            rule_b = rules[j]

            antecedent_similarity = (
                rule_antecedent_similarity(
                    rule_a,
                    rule_b,
                    variable_ranges
                )
            )

            consequent_sim = consequent_similarity(
                rule_a,
                rule_b
            )

            conflict_score = (
                antecedent_similarity
                * (1.0 - consequent_sim)
            )

            if conflict_score >= consistency_threshold:

                suspicion_scores[
                    rule_a.rule_id
                ] += conflict_score

                suspicion_scores[
                    rule_b.rule_id
                ] += conflict_score

                conflict_counts[
                    rule_a.rule_id
                ] += 1

                conflict_counts[
                    rule_b.rule_id
                ] += 1

    # -----------------------------------------
    # BUILD RESULT
    # -----------------------------------------

    results = []

    for rule in rules:

        rule_id = rule.rule_id

        score = suspicion_scores.get(
            rule_id,
            0.0
        )

        count = conflict_counts.get(
            rule_id,
            0
        )

        results.append({

            "rule_id":
                rule_id,

            "suspicion_score":
                round(score, 4),

            "conflict_count":
                count
        })

    # Highest suspicion first
    results.sort(
        key=lambda x:
            x["suspicion_score"],
        reverse=True
    )

    return results
def locate_conflict_regions(
    rules,
    variable_ranges,
    threshold=0.7,
    resolution=50
):
    """
    Identifies input points where two rules
    simultaneously activate strongly but have
    different consequents.
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

    points = np.stack(
        [axis.flatten() for axis in mesh],
        axis=-1
    )

    conflict_regions = []

    for point in points:

        inputs = {
            variables[i]: point[i]
            for i in range(len(variables))
        }

        for i in range(len(rules)):

            for j in range(i + 1, len(rules)):

                rule_a = rules[i]
                rule_b = rules[j]

                activation_a = rule_a.membership(
                    inputs
                )

                activation_b = rule_b.membership(
                    inputs
                )

                # Rules must both activate
                # and produce different outputs.
                if (
                    activation_a > 0
                    and
                    activation_b > 0
                    and
                    rule_a.consequent
                    !=
                    rule_b.consequent
                ):

                    conflict_strength = min(
                        activation_a,
                        activation_b
                    )

                    if conflict_strength >= threshold:

                        conflict_regions.append({

                            "inputs":
                                inputs.copy(),

                            "rule_1":
                                rule_a.rule_id,

                            "rule_2":
                                rule_b.rule_id,

                            "activation_1":
                                round(
                                    activation_a,
                                    4
                                ),

                            "activation_2":
                                round(
                                    activation_b,
                                    4
                                ),

                            "conflict_strength":
                                round(
                                    conflict_strength,
                                    4
                                )
                        })

    return conflict_regions