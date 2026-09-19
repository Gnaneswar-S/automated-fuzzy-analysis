from ..fuzzy.fuzzy_sets import TriangularFuzzySet
from ..fuzzy.similarity import fuzzy_set_similarity
from ..rules.rules import FuzzyRule
from ..verification.consistency import calculate_conflict_score

def generate_shifted_fuzzy_sets(
    base_set,
    shifts
):
    """
    Generates triangular fuzzy sets by shifting
    a base triangular fuzzy set along the input axis.
    """

    generated_sets = []

    for index, shift in enumerate(shifts):
        generated_sets.append(
            TriangularFuzzySet(
                name=f"shift_{index}",
                a=base_set.a + shift,
                b=base_set.b + shift,
                c=base_set.c + shift
            )
        )

    return generated_sets


def calculate_similarity_experiment(
    base_set,
    shifted_sets,
    xmin,
    xmax
):
    """
    Measures actual fuzzy-set similarity for each
    shifted set against the base set.
    """

    results = []

    for fuzzy_set in shifted_sets:
        similarity = fuzzy_set_similarity(
            base_set,
            fuzzy_set,
            xmin,
            xmax
        )

        results.append({
            "set": fuzzy_set.name,
            "a": fuzzy_set.a,
            "b": fuzzy_set.b,
            "c": fuzzy_set.c,
            "similarity": round(similarity, 4)
        })

    return results


def evaluate_thresholds(
    similarity_results,
    thresholds
):
    """
    Determines whether each measured similarity would
    be classified as a conflict at each threshold.

    Because consequents are different, conflict score
    equals antecedent similarity.
    """

    evaluations = []

    for threshold in thresholds:
        for result in similarity_results:
            evaluations.append({
                "threshold": threshold,
                "set": result["set"],
                "similarity": result["similarity"],
                "detected": (
                    result["similarity"] >= threshold
                )
            })

    return evaluations
def evaluate_generated_rule_pairs(
    base_set,
    shifted_sets,
    xmin,
    xmax,
    thresholds
):
    """
    Evaluates generated fuzzy-set pairs as actual
    fuzzy rules using the project's conflict metric.
    """

    results = []

    for shifted_set in shifted_sets:

        rule_a = FuzzyRule(
            rule_id="BASE",
            antecedent={"temperature": base_set},
            consequent="risk_low"
        )

        rule_b = FuzzyRule(
            rule_id=shifted_set.name,
            antecedent={"temperature": shifted_set},
            consequent="risk_high"
        )

        similarity = fuzzy_set_similarity(
            base_set,
            shifted_set,
            xmin,
            xmax
        )

        for threshold in thresholds:

            conflict = calculate_conflict_score(
                rule_a,
                rule_b,
                {"temperature": (xmin, xmax)}
            )

            results.append({
                "set": shifted_set.name,
                "shift": round(
                    shifted_set.a - base_set.a,
                    4
                ),
                "similarity": round(
                    similarity,
                    4
                ),
                "conflict_score": round(
                    conflict["conflict_score"],
                    4
                ),
                "threshold": threshold,
                "detected": (
                    conflict["conflict_score"] >= threshold
                )
            })

    return results