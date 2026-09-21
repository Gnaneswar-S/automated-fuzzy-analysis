from ..fuzzy.fuzzy_sets import TriangularFuzzySet
from ..rules.rules import FuzzyRule
from ..verification.verification import verify_rule_base
from ..diagnosis.activation_overlap import (
    characterize_activation_overlap
)
from .defect_injection import inject_multiple_defects
from .benchmark import create_multi_defect_benchmark_case
from .benchmark_runner import run_multi_defect_benchmark_case
from ..repair.repair_engine import apply_repair_candidate
from ..repair.behavioral_validation import evaluate_repair_behavior

def create_independent_experiment_case():
    """
    Creates a controlled two-variable rule base containing
    two spatially independent defect regions.

    Defect A:
        temperature-low AND humidity-low

    Defect B:
        temperature-high AND humidity-high

    The remaining fuzzy cells provide complete interior
    coverage without introducing additional conflicting
    duplicate rules.
    """

    temperature_low = TriangularFuzzySet(
        "temperature_low",
        0,
        20,
        40
    )

    temperature_medium = TriangularFuzzySet(
        "temperature_medium",
        30,
        50,
        70
    )

    temperature_high = TriangularFuzzySet(
        "temperature_high",
        60,
        80,
        100
    )

    humidity_low = TriangularFuzzySet(
        "humidity_low",
        0,
        20,
        40
    )

    humidity_medium = TriangularFuzzySet(
        "humidity_medium",
        30,
        50,
        70
    )

    humidity_high = TriangularFuzzySet(
        "humidity_high",
        60,
        80,
        100
    )

    clean_rules = [
        FuzzyRule(
            "C2",
            {
                "temperature": temperature_low,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C3",
            {
                "temperature": temperature_low,
                "humidity": humidity_high
            },
            "risk_medium"
        ),

        FuzzyRule(
            "C4",
            {
                "temperature": temperature_medium,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C5",
            {
                "temperature": temperature_medium,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C6",
            {
                "temperature": temperature_medium,
                "humidity": humidity_high
            },
            "risk_medium"
        ),

        FuzzyRule(
            "C7",
            {
                "temperature": temperature_high,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C8",
            {
                "temperature": temperature_high,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "A1",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "A2",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),

        FuzzyRule(
            "B1",
            {
                "temperature": temperature_high,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "B2",
            {
                "temperature": temperature_high,
                "humidity": humidity_high
            },
            "risk_medium"
        )
    ]

    defects = [
        {
            "target_rule": "A2",
            "conflicting_consequent": "risk_high"
        },
        {
            "target_rule": "B2",
            "conflicting_consequent": "risk_low"
        }
    ]

    expected_repairs = [
        {
            "target_rule": "A2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        },
        {
            "target_rule": "B2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        }
    ]

    defective_rules, defect_info = inject_multiple_defects(
        clean_rules,
        defects
    )

    benchmark_case = create_multi_defect_benchmark_case(
        case_id="MD-2-INDEPENDENT",
        clean_rules=clean_rules,
        defect_info=defect_info,
        expected_repairs=expected_repairs
    )

    return {
        "benchmark_case": benchmark_case,
        "clean_rules": clean_rules,
        "defective_rules": defective_rules,
        "defect_info": defect_info,
        "expected_repairs": expected_repairs
    }


def create_overlapping_experiment_case():
    """
    Creates a controlled two-variable rule base containing
    two defects whose activation regions overlap.

    Defect A:
        standard low temperature AND standard low humidity

    Defect B:
        shifted-low temperature AND shifted-low humidity

    The two antecedent regions overlap at the activation
    threshold while remaining below the structural conflict
    similarity threshold when compared with each other.
    """

    temperature_low = TriangularFuzzySet(
        "temperature_low",
        0,
        20,
        40
    )

    temperature_shifted_low = TriangularFuzzySet(
        "temperature_shifted_low",
        5,
        25,
        45
    )

    temperature_medium = TriangularFuzzySet(
        "temperature_medium",
        30,
        50,
        70
    )

    temperature_high = TriangularFuzzySet(
        "temperature_high",
        60,
        80,
        100
    )

    humidity_low = TriangularFuzzySet(
        "humidity_low",
        0,
        20,
        40
    )

    humidity_shifted_low = TriangularFuzzySet(
        "humidity_shifted_low",
        5,
        25,
        45
    )

    humidity_medium = TriangularFuzzySet(
        "humidity_medium",
        30,
        50,
        70
    )

    humidity_high = TriangularFuzzySet(
        "humidity_high",
        60,
        80,
        100
    )

    clean_rules = [
        FuzzyRule(
            "C2",
            {
                "temperature": temperature_low,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C3",
            {
                "temperature": temperature_low,
                "humidity": humidity_high
            },
            "risk_medium"
        ),

        FuzzyRule(
            "C4",
            {
                "temperature": temperature_medium,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C5",
            {
                "temperature": temperature_medium,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C6",
            {
                "temperature": temperature_medium,
                "humidity": humidity_high
            },
            "risk_medium"
        ),

        FuzzyRule(
            "C7",
            {
                "temperature": temperature_high,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C8",
            {
                "temperature": temperature_high,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C9",
            {
                "temperature": temperature_high,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "A1",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "A2",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),

        FuzzyRule(
            "B1",
            {
                "temperature": temperature_shifted_low,
                "humidity": humidity_shifted_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "B2",
            {
                "temperature": temperature_shifted_low,
                "humidity": humidity_shifted_low
            },
            "risk_medium"
        )
    ]

    defects = [
        {
            "target_rule": "A2",
            "conflicting_consequent": "risk_high"
        },
        {
            "target_rule": "B2",
            "conflicting_consequent": "risk_low"
        }
    ]

    expected_repairs = [
        {
            "target_rule": "A2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        },
        {
            "target_rule": "B2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        }
    ]

    defective_rules, defect_info = inject_multiple_defects(
        clean_rules,
        defects
    )

    benchmark_case = create_multi_defect_benchmark_case(
        case_id="MD-3-OVERLAPPING",
        clean_rules=clean_rules,
        defect_info=defect_info,
        expected_repairs=expected_repairs
    )

    return {
        "benchmark_case": benchmark_case,
        "clean_rules": clean_rules,
        "defective_rules": defective_rules,
        "defect_info": defect_info,
        "expected_repairs": expected_repairs
    }


def create_interacting_experiment_case():
    """
    Creates a controlled two-variable rule base designed to test
    behavioral interaction between two nearby defect regions.

    Defect A:
        standard low temperature AND standard low humidity

    Defect B:
        shifted-low temperature AND shifted-low humidity

    The shifted-low fuzzy sets are deliberately close to the
    standard-low sets so that structural similarity and activation
    overlap can be measured before behavioral interaction is tested.

    Behavioral interaction is NOT assumed by construction.
    It must be established empirically through the subsequent
    counterfactual repair experiment.
    """

    temperature_low = TriangularFuzzySet(
        "temperature_low",
        0,
        20,
        40
    )

    temperature_shifted_low = TriangularFuzzySet(
        "temperature_shifted_low",
        2,
        22,
        42
    )

    temperature_medium = TriangularFuzzySet(
        "temperature_medium",
        30,
        50,
        70
    )

    temperature_high = TriangularFuzzySet(
        "temperature_high",
        60,
        80,
        100
    )

    humidity_low = TriangularFuzzySet(
        "humidity_low",
        0,
        20,
        40
    )

    humidity_shifted_low = TriangularFuzzySet(
        "humidity_shifted_low",
        2,
        22,
        42
    )

    humidity_medium = TriangularFuzzySet(
        "humidity_medium",
        30,
        50,
        70
    )

    humidity_high = TriangularFuzzySet(
        "humidity_high",
        60,
        80,
        100
    )

    clean_rules = [
        FuzzyRule(
            "C2",
            {
                "temperature": temperature_low,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C3",
            {
                "temperature": temperature_medium,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C4",
            {
                "temperature": temperature_medium,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C5",
            {
                "temperature": temperature_medium,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C6",
            {
                "temperature": temperature_high,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C7",
            {
                "temperature": temperature_low,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C8",
            {
                "temperature": temperature_high,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C9",
            {
                "temperature": temperature_high,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "A1",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "A2",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "B1",
            {
                "temperature": temperature_shifted_low,
                "humidity": humidity_shifted_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "B2",
            {
                "temperature": temperature_shifted_low,
                "humidity": humidity_shifted_low
            },
            "risk_medium"
        )
    ]

    defects = [
        {
            "target_rule": "A2",
            "conflicting_consequent": "risk_high"
        },
        {
            "target_rule": "B2",
            "conflicting_consequent": "risk_low"
        }
    ]

    expected_repairs = [
        {
            "target_rule": "A2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        },
        {
            "target_rule": "B2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        }
    ]

    defective_rules, defect_info = inject_multiple_defects(
        clean_rules,
        defects
    )

    benchmark_case = create_multi_defect_benchmark_case(
        case_id="MD-4-INTERACTING",
        clean_rules=clean_rules,
        defect_info=defect_info,
        expected_repairs=expected_repairs
    )

    return {
        "benchmark_case": benchmark_case,
        "clean_rules": clean_rules,
        "defective_rules": defective_rules,
        "defect_info": defect_info,
        "expected_repairs": expected_repairs
    }

def classify_defect_region_relationships(overlap_results):
    """
    Classifies spatial relationships between detected defect
    activation regions.

    Two defect regions are considered overlapping when their
    activation-region component bounding boxes intersect
    across every variable.

    This is a descriptive experimental classification, not
    a new repair score or ranking criterion.
    """

    relationships = []

    for i in range(len(overlap_results)):
        for j in range(i + 1, len(overlap_results)):

            defect_a = overlap_results[i]
            defect_b = overlap_results[j]

            components_a = (
                defect_a["overlap"]["components"]
            )
            components_b = (
                defect_b["overlap"]["components"]
            )

            overlapping = False

            for component_a in components_a:
                for component_b in components_b:

                    variables = set(
                        component_a["bounds"].keys()
                    ) & set(
                        component_b["bounds"].keys()
                    )

                    if not variables:
                        continue

                    intersects = True

                    for variable in variables:

                        a_min = component_a[
                            "bounds"
                        ][variable]["minimum"]

                        a_max = component_a[
                            "bounds"
                        ][variable]["maximum"]

                        b_min = component_b[
                            "bounds"
                        ][variable]["minimum"]

                        b_max = component_b[
                            "bounds"
                        ][variable]["maximum"]

                        if (
                            a_max < b_min
                            or
                            b_max < a_min
                        ):
                            intersects = False
                            break

                    if intersects:
                        overlapping = True
                        break

                if overlapping:
                    break

            relationship = (
                "OVERLAPPING"
                if overlapping
                else "INDEPENDENT"
            )

            relationships.append({
                "defect_a": (
                    defect_a["rule_1"],
                    defect_a["rule_2"]
                ),
                "defect_b": (
                    defect_b["rule_1"],
                    defect_b["rule_2"]
                ),
                "relationship": relationship
            })

    return relationships

def analyze_multi_defect_case(
    case,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50,
    consistency_threshold=0.7,
    completeness_resolution=30
):
    """
    Performs structural verification and activation-region
    characterization for one controlled multi-defect case.
    """

    verification = verify_rule_base(
        case["defective_rules"],
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    rule_lookup = {
        rule.rule_id: rule
        for rule in case["defective_rules"]
    }

    overlap_results = []

    for conflict in verification["consistency"]["conflicts"]:

        rule_a = rule_lookup[conflict["rule_1"]]
        rule_b = rule_lookup[conflict["rule_2"]]

        overlap = characterize_activation_overlap(
            rule_a,
            rule_b,
            variable_ranges,
            activation_threshold=activation_threshold,
            resolution=resolution
        )

        overlap_results.append({
            "rule_1": conflict["rule_1"],
            "rule_2": conflict["rule_2"],
            "conflict_score": conflict["conflict_score"],
            "overlap": overlap
        })

    relationships = classify_defect_region_relationships(
        overlap_results
    )

    return {
        "case_id": case["benchmark_case"]["case_id"],
        "verification": verification,
        "overlap_results": overlap_results,
        "relationships": relationships
    }

def _get_rule_lookup(rules):
    """Returns a rule-id lookup for a rule base."""

    return {
        rule.rule_id: rule
        for rule in rules
    }


def _get_related_conflicts(
    conflicts,
    rule_ids
):
    """
    Returns conflicts involving at least one rule from the
    specified defect region.
    """

    rule_ids = set(rule_ids)

    return [
        conflict
        for conflict in conflicts
        if (
            conflict["rule_1"] in rule_ids
            or conflict["rule_2"] in rule_ids
        )
    ]


def _get_primary_conflict_state(
    conflicts,
    rule_a,
    rule_b
):
    """
    Returns the direct conflict state for one controlled defect pair.
    """

    target_ids = {rule_a, rule_b}

    for conflict in conflicts:
        if {
            conflict["rule_1"],
            conflict["rule_2"]
        } == target_ids:
            return {
                "present": True,
                "conflict": conflict
            }

    return {
        "present": False,
        "conflict": None
    }


def _behavior_changes_in_rule_region(
    original_rules,
    behavior_result,
    region_rule_ids,
    activation_threshold=0.7
):
    """
    Determines whether behavioral changes reported by the existing
    behavioral validator occur inside a specified rule region.

    The region is defined by simultaneous activation of all supplied
    rules at or above the activation threshold in the original rule
    base.
    """

    rule_lookup = _get_rule_lookup(original_rules)

    region_rules = [
        rule_lookup[rule_id]
        for rule_id in region_rule_ids
        if rule_id in rule_lookup
    ]

    region_changes = []

    for change in behavior_result["changed_points"]:
        inputs = change["inputs"]

        activations = [
            rule.membership(inputs)
            for rule in region_rules
        ]

        if region_rules and all(
            activation >= activation_threshold
            for activation in activations
        ):
            region_changes.append(change)

    return {
        "changed_point_count": len(region_changes),
        "changed_points": region_changes,
        "behavior_changed": bool(region_changes)
    }


def _build_counterfactual_repair_candidate(
    target_rule,
    correct_value
):
    """
    Builds an explicit counterfactual repair candidate.

    No repair ranking is used because MD-4 tests causal/counterfactual
    interaction under a controlled intervention.
    """

    return {
        "action": "CHANGE_CONSEQUENT",
        "target_rule": target_rule,
        "new_consequent": correct_value
    }


def _run_single_counterfactual(
    case,
    variable_ranges,
    target_rule,
    correct_value,
    remaining_region_rule_ids,
    original_region_rule_ids,
    activation_threshold=0.7,
    resolution=50,
    consistency_threshold=0.7,
    completeness_resolution=30
):
    """
    Applies one controlled repair while leaving the other defect
    unrepaired, then measures structural and behavioral changes
    associated with the remaining defect.
    """

    original_rules = case["defective_rules"]

    original_verification = verify_rule_base(
        original_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    candidate = _build_counterfactual_repair_candidate(
        target_rule,
        correct_value
    )

    repaired_rules = apply_repair_candidate(
        original_rules,
        candidate
    )

    repaired_verification = verify_rule_base(
        repaired_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    behavior_result = evaluate_repair_behavior(
        original_rules,
        repaired_rules,
        variable_ranges,
        original_verification["consistency"]["conflicts"],
        resolution=resolution,
        activation_threshold=activation_threshold
    )

    original_conflicts = original_verification[
        "consistency"
    ]["conflicts"]

    repaired_conflicts = repaired_verification[
        "consistency"
    ]["conflicts"]

    original_related = _get_related_conflicts(
        original_conflicts,
        remaining_region_rule_ids
    )

    repaired_related = _get_related_conflicts(
        repaired_conflicts,
        remaining_region_rule_ids
    )

    original_primary = _get_primary_conflict_state(
        original_conflicts,
        remaining_region_rule_ids[0],
        remaining_region_rule_ids[1]
    )

    repaired_primary = _get_primary_conflict_state(
        repaired_conflicts,
        remaining_region_rule_ids[0],
        remaining_region_rule_ids[1]
    )

    region_behavior = _behavior_changes_in_rule_region(
        original_rules,
        behavior_result,
        original_region_rule_ids,
        activation_threshold=activation_threshold
    )

    diagnosis_changed = (
        original_related != repaired_related
    )

    primary_conflict_changed = (
        original_primary != repaired_primary
    )

    return {
        "intervention": {
            "target_rule": target_rule,
            "action": "CHANGE_CONSEQUENT",
            "correct_value": correct_value
        },
        "verification_before": original_verification,
        "verification_after": repaired_verification,
        "conflict_count_before": (
            original_verification[
                "consistency"
            ]["conflict_count"]
        ),
        "conflict_count_after": (
            repaired_verification[
                "consistency"
            ]["conflict_count"]
        ),
        "remaining_defect": {
            "rule_ids": list(remaining_region_rule_ids),
            "primary_conflict_before": original_primary,
            "primary_conflict_after": repaired_primary,
            "related_conflicts_before": original_related,
            "related_conflicts_after": repaired_related,
            "primary_conflict_changed": primary_conflict_changed,
            "diagnosis_changed": diagnosis_changed
        },
        "behavioral_validation": behavior_result,
        "remaining_region_behavior": region_behavior
    }


def run_interacting_counterfactual_experiment(
    case,
    variable_ranges,
    activation_threshold=0.7,
    resolution=50,
    consistency_threshold=0.7,
    completeness_resolution=30
):
    """
    Runs the MD-4 counterfactual interaction experiment.

    State 0:
        Both controlled defects are present.

    State 1:
        Repair defect A only and observe whether defect B's structural
        diagnosis or behavioral state changes.

    State 2:
        Repair defect B only and observe whether defect A's structural
        diagnosis or behavioral state changes.

    Behavioral interaction is reported empirically as DETECTED or
    NOT DETECTED. No positive interaction is assumed.
    """

    defective_rules = case["defective_rules"]

    state_0 = verify_rule_base(
        defective_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    state_1 = _run_single_counterfactual(
        case=case,
        variable_ranges=variable_ranges,
        target_rule="A2",
        correct_value="risk_medium",
        remaining_region_rule_ids=("B1", "B2"),
        original_region_rule_ids=("B1", "B2"),
        activation_threshold=activation_threshold,
        resolution=resolution,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    state_2 = _run_single_counterfactual(
        case=case,
        variable_ranges=variable_ranges,
        target_rule="B2",
        correct_value="risk_medium",
        remaining_region_rule_ids=("A1", "A2"),
        original_region_rule_ids=("A1", "A2"),
        activation_threshold=activation_threshold,
        resolution=resolution,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    a_to_b = (
        state_1["remaining_defect"]["diagnosis_changed"]
        or
        state_1["remaining_region_behavior"]["behavior_changed"]
    )

    b_to_a = (
        state_2["remaining_defect"]["diagnosis_changed"]
        or
        state_2["remaining_region_behavior"]["behavior_changed"]
    )

    return {
        "case_id": case["benchmark_case"]["case_id"],
        "state_0": {
            "verification": state_0,
            "conflict_count": (
                state_0["consistency"]["conflict_count"]
            )
        },
        "state_1_repair_A": state_1,
        "state_2_repair_B": state_2,
        "dependencies": {
            "A_to_B": (
                "DETECTED"
                if a_to_b
                else "NOT DETECTED"
            ),
            "B_to_A": (
                "DETECTED"
                if b_to_a
                else "NOT DETECTED"
            )
        }
    }

def _run_multi_region_counterfactual(
    case,
    variable_ranges,
    target_region,
    remaining_regions,
    activation_threshold=0.7,
    resolution=50,
    consistency_threshold=0.7,
    completeness_resolution=30
):
    """
    Applies one controlled repair to a target defect region and
    measures its effects on every remaining defect region.
    """

    original_rules = case["defective_rules"]

    original_verification = verify_rule_base(
        original_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    candidate = _build_counterfactual_repair_candidate(
        target_region["target_rule"],
        target_region["correct_value"]
    )

    repaired_rules = apply_repair_candidate(
        original_rules,
        candidate
    )

    repaired_verification = verify_rule_base(
        repaired_rules,
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    behavior_result = evaluate_repair_behavior(
        original_rules,
        repaired_rules,
        variable_ranges,
        original_verification["consistency"]["conflicts"],
        resolution=resolution,
        activation_threshold=activation_threshold
    )

    effects = []

    original_conflicts = (
        original_verification["consistency"]["conflicts"]
    )

    repaired_conflicts = (
        repaired_verification["consistency"]["conflicts"]
    )

    for remaining_region in remaining_regions:

        rule_ids = tuple(remaining_region["rule_ids"])

        original_related = _get_related_conflicts(
            original_conflicts,
            rule_ids
        )

        repaired_related = _get_related_conflicts(
            repaired_conflicts,
            rule_ids
        )

        original_primary = _get_primary_conflict_state(
            original_conflicts,
            rule_ids[0],
            rule_ids[1]
        )

        repaired_primary = _get_primary_conflict_state(
            repaired_conflicts,
            rule_ids[0],
            rule_ids[1]
        )

        region_behavior = _behavior_changes_in_rule_region(
            original_rules,
            behavior_result,
            rule_ids,
            activation_threshold=activation_threshold
        )

        diagnosis_changed = (
            original_related != repaired_related
        )

        primary_conflict_changed = (
            original_primary != repaired_primary
        )

        effects.append({
            "remaining_region": remaining_region["name"],
            "rule_ids": list(rule_ids),
            "primary_conflict_before": original_primary,
            "primary_conflict_after": repaired_primary,
            "primary_conflict_changed": (
                primary_conflict_changed
            ),
            "related_conflicts_before": original_related,
            "related_conflicts_after": repaired_related,
            "diagnosis_changed": diagnosis_changed,
            "behavior_changed": (
                region_behavior["behavior_changed"]
            ),
            "changed_point_count": (
                region_behavior["changed_point_count"]
            ),
            "behavior_details": region_behavior
        })

    return {
        "intervention": {
            "target_region": target_region["name"],
            "target_rule": target_region["target_rule"],
            "action": "CHANGE_CONSEQUENT",
            "correct_value": target_region["correct_value"]
        },
        "verification_before": original_verification,
        "verification_after": repaired_verification,
        "conflict_count_before": (
            original_verification[
                "consistency"
            ]["conflict_count"]
        ),
        "conflict_count_after": (
            repaired_verification[
                "consistency"
            ]["conflict_count"]
        ),
        "effects_on_remaining_regions": effects
    }


def run_multi_region_counterfactual_experiment(
    case,
    variable_ranges,
    defect_regions,
    activation_threshold=0.7,
    resolution=50,
    consistency_threshold=0.7,
    completeness_resolution=30
):
    """
    Runs controlled counterfactual repairs across three or more
    defect regions.

    For each defect region:
        1. Repair that region only.
        2. Keep every other defect unrepaired.
        3. Measure structural, diagnostic, and behavioral effects
           on every remaining defect region.
    """

    if len(defect_regions) < 3:
        raise ValueError(
            "At least three defect regions are required."
        )

    state_0 = verify_rule_base(
        case["defective_rules"],
        variable_ranges,
        consistency_threshold=consistency_threshold,
        completeness_resolution=completeness_resolution
    )

    states = {}

    for target_region in defect_regions:

        remaining_regions = [
            region
            for region in defect_regions
            if region["name"] != target_region["name"]
        ]

        state_key = (
            f"repair_{target_region['name']}"
        )

        states[state_key] = _run_multi_region_counterfactual(
            case=case,
            variable_ranges=variable_ranges,
            target_region=target_region,
            remaining_regions=remaining_regions,
            activation_threshold=activation_threshold,
            resolution=resolution,
            consistency_threshold=consistency_threshold,
            completeness_resolution=completeness_resolution
        )

    dependency_matrix = {}

    for target_region in defect_regions:

        state_key = (
            f"repair_{target_region['name']}"
        )

        effects = states[
            state_key
        ]["effects_on_remaining_regions"]

        dependency_matrix[
            target_region["name"]
        ] = {}

        for effect in effects:

            dependency_matrix[
                target_region["name"]
            ][
                effect["remaining_region"]
            ] = {
                "diagnosis_changed": (
                    effect["diagnosis_changed"]
                ),
                "behavior_changed": (
                    effect["behavior_changed"]
                ),
                "changed_point_count": (
                    effect["changed_point_count"]
                ),
                "dependency_detected": (
                    effect["diagnosis_changed"]
                    or
                    effect["behavior_changed"]
                )
            }

    return {
        "case_id": case["benchmark_case"]["case_id"],
        "state_0": {
            "verification": state_0,
            "conflict_count": (
                state_0["consistency"]["conflict_count"]
            )
        },
        "counterfactual_states": states,
        "dependency_matrix": dependency_matrix
    }

def create_three_region_independent_experiment_case():
    """
    Creates a controlled three-defect configuration with
    three spatially independent defect regions.

    Region A:
        temperature-low AND humidity-low

    Region B:
        temperature-medium AND humidity-medium

    Region C:
        temperature-high AND humidity-high

    The six remaining fuzzy cells provide complete
    interior coverage without introducing additional
    duplicate rules in the defect regions.
    """

    temperature_low = TriangularFuzzySet(
        "temperature_low",
        0,
        20,
        40
    )

    temperature_medium = TriangularFuzzySet(
        "temperature_medium",
        30,
        50,
        70
    )

    temperature_high = TriangularFuzzySet(
        "temperature_high",
        60,
        80,
        100
    )

    humidity_low = TriangularFuzzySet(
        "humidity_low",
        0,
        20,
        40
    )

    humidity_medium = TriangularFuzzySet(
        "humidity_medium",
        30,
        50,
        70
    )

    humidity_high = TriangularFuzzySet(
        "humidity_high",
        60,
        80,
        100
    )

    clean_rules = [
        # Region A: low x low
        FuzzyRule(
            "A1",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "A2",
            {
                "temperature": temperature_low,
                "humidity": humidity_low
            },
            "risk_medium"
        ),

        # Region B: medium x medium
        FuzzyRule(
            "B1",
            {
                "temperature": temperature_medium,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "B2",
            {
                "temperature": temperature_medium,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),

        # Region C: high x high
        FuzzyRule(
            "C1",
            {
                "temperature": temperature_high,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "C2",
            {
                "temperature": temperature_high,
                "humidity": humidity_high
            },
            "risk_medium"
        ),

        # Remaining six cells: complete coverage
        FuzzyRule(
            "D1",
            {
                "temperature": temperature_low,
                "humidity": humidity_medium
            },
            "risk_medium"
        ),
        FuzzyRule(
            "D2",
            {
                "temperature": temperature_low,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "D3",
            {
                "temperature": temperature_medium,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "D4",
            {
                "temperature": temperature_medium,
                "humidity": humidity_high
            },
            "risk_medium"
        ),
        FuzzyRule(
            "D5",
            {
                "temperature": temperature_high,
                "humidity": humidity_low
            },
            "risk_medium"
        ),
        FuzzyRule(
            "D6",
            {
                "temperature": temperature_high,
                "humidity": humidity_medium
            },
            "risk_medium"
        )
    ]

    defects = [
        {
            "target_rule": "A2",
            "conflicting_consequent": "risk_high"
        },
        {
            "target_rule": "B2",
            "conflicting_consequent": "risk_low"
        },
        {
            "target_rule": "C2",
            "conflicting_consequent": "risk_high"
        }
    ]

    expected_repairs = [
        {
            "target_rule": "A2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        },
        {
            "target_rule": "B2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        },
        {
            "target_rule": "C2",
            "repair_action": "CHANGE_CONSEQUENT",
            "correct_value": "risk_medium"
        }
    ]

    return run_multi_defect_benchmark_case(
        case_id="MD-5-THREE-INDEPENDENT",
        clean_rules=clean_rules,
        variable_ranges={
            "temperature": (0, 100),
            "humidity": (0, 100)
        },
        defects=defects,
        expected_repairs=expected_repairs,
        consistency_threshold=0.7,
        completeness_resolution=100
    )
