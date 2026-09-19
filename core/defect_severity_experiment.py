from copy import deepcopy

from .fuzzy_sets import TriangularFuzzySet
from .similarity import fuzzy_set_similarity
from .rules import FuzzyRule
from .verification import verify_rule_base
from .localization import calculate_rule_suspicion_scores
from .repair import generate_repair_candidates
from .repair_engine import evaluate_repair_candidate


def inject_severity_controlled_defect(
    rules,
    target_rule_id,
    variable,
    shift,
    conflicting_consequent
):
    """
    Creates a controlled defective rule base.

    Defect severity is controlled by shifting the target
    rule's antecedent while maintaining a conflicting
    consequent.

    The original rule base is never modified.
    """

    defective_rules = deepcopy(rules)

    target_rule = None

    for rule in defective_rules:
        if rule.rule_id == target_rule_id:
            target_rule = rule
            break

    if target_rule is None:
        raise ValueError(
            f"Rule '{target_rule_id}' not found."
        )

    fuzzy_set = target_rule.antecedent[variable]

    shifted_set = TriangularFuzzySet(
        name=f"{fuzzy_set.name}_severity_{shift}",
        a=fuzzy_set.a + shift,
        b=fuzzy_set.b + shift,
        c=fuzzy_set.c + shift
    )

    target_rule.antecedent[variable] = shifted_set
    target_rule.consequent = conflicting_consequent

    return defective_rules


def evaluate_defect_severity(
    clean_rules,
    variable_ranges,
    target_rule_id,
    variable,
    shifts,
    conflicting_consequent,
    consistency_threshold=0.7,
    completeness_resolution=100
):
    """
    Evaluates the complete analysis-and-repair pipeline
    under controlled defect severity.

    Severity is represented by controlled displacement
    of the target rule's antecedent.

    The actual antecedent similarity is measured
    independently from the detection threshold.
    """

    results = []

    reference_rule = next(
        rule for rule in clean_rules
        if rule.rule_id == "R2"
    )

    target_rule = next(
        rule for rule in clean_rules
        if rule.rule_id == target_rule_id
    )

    reference_set = reference_rule.antecedent[variable]
    target_set = target_rule.antecedent[variable]

    xmin, xmax = variable_ranges[variable]

    for shift in shifts:

        defective_rules = inject_severity_controlled_defect(
            clean_rules,
            target_rule_id,
            variable,
            shift,
            conflicting_consequent
        )

        shifted_rule = next(
            rule for rule in defective_rules
            if rule.rule_id == target_rule_id
        )

        shifted_set = shifted_rule.antecedent[variable]

        actual_similarity = fuzzy_set_similarity(
            reference_set,
            shifted_set,
            xmin,
            xmax
        )

        verification = verify_rule_base(
            defective_rules,
            variable_ranges,
            consistency_threshold=consistency_threshold,
            completeness_resolution=completeness_resolution
        )

        localization = calculate_rule_suspicion_scores(
            defective_rules,
            variable_ranges,
            consistency_threshold=consistency_threshold
        )

        conflicts = verification["consistency"]["conflicts"]

        repair_candidates = generate_repair_candidates(
            defective_rules,
            conflicts
        )

        successful_repairs = 0

        for candidate in repair_candidates:

            evaluation = evaluate_repair_candidate(
                defective_rules,
                candidate,
                variable_ranges,
                consistency_threshold=consistency_threshold,
                completeness_resolution=completeness_resolution
            )

            if evaluation["comparison"]["repair_success"]:
                successful_repairs += 1

        localized_rule = None

        if localization and conflicts:
            localized_rule = localization[0]["rule_id"]

        conflict_score = 0.0

        if conflicts:
            conflict_score = conflicts[0]["conflict_score"]

        results.append({
            "shift": shift,
            "absolute_shift": abs(shift),
            "antecedent_similarity":
                round(actual_similarity, 4),
            "conflict_score":
                round(conflict_score, 4),
            "conflict_count":
                verification["consistency"]["conflict_count"],
            "conflict_detected":
                verification["consistency"]["conflict_count"] > 0,
            "completeness":
                verification["completeness"]["score"],
            "overall_status":
                verification["overall_status"],
            "top_localized_rule":
                localized_rule,
            "repair_candidate_count":
                len(repair_candidates),
            "successful_repair_count":
                successful_repairs
        })

    return results