from itertools import combinations

from ..fuzzy.similarity import (
    rule_antecedent_similarity,
    consequent_similarity
)


def calculate_conflict_score(
    rule_a,
    rule_b,
    variable_ranges
):
    """
    Calculates the conflict score between
    two fuzzy rules.

    High antecedent similarity combined with
    different consequents indicates a potential
    inconsistency.
    """

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

    return {
        "antecedent_similarity":
            antecedent_similarity,

        "consequent_similarity":
            consequent_sim,

        "conflict_score":
            conflict_score
    }


def detect_inconsistencies(
    rules,
    variable_ranges,
    threshold=0.7
):
    """
    Checks every pair of rules and identifies
    potentially inconsistent rule pairs.

    threshold:
        Minimum conflict score required for
        a pair to be reported.
    """

    conflicts = []

    for rule_a, rule_b in combinations(
        rules,
        2
    ):

        result = calculate_conflict_score(
            rule_a,
            rule_b,
            variable_ranges
        )

        if result["conflict_score"] >= threshold:

            conflicts.append({

                "rule_1":
                    rule_a.rule_id,

                "rule_2":
                    rule_b.rule_id,

                "antecedent_similarity":
                    round(
                        result[
                            "antecedent_similarity"
                        ],
                        4
                    ),

                "consequent_similarity":
                    round(
                        result[
                            "consequent_similarity"
                        ],
                        4
                    ),

                "conflict_score":
                    round(
                        result[
                            "conflict_score"
                        ],
                        4
                    ),

                "consequent_1":
                    rule_a.consequent,

                "consequent_2":
                    rule_b.consequent
            })

    return conflicts