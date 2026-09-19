from .consistency import detect_inconsistencies
from .completeness import (
    calculate_completeness,
    find_uncovered_regions
)


def verify_rule_base(
    rules,
    variable_ranges,
    consistency_threshold=0.7,
    completeness_resolution=30,
    activation_threshold=0.0
):
    """
    Performs a unified verification of a fuzzy rule base.

    Includes:
    - Consistency analysis
    - Completeness analysis
    """

    # -----------------------------------------
    # CONSISTENCY ANALYSIS
    # -----------------------------------------

    conflicts = detect_inconsistencies(
        rules,
        variable_ranges,
        threshold=consistency_threshold
    )

    # -----------------------------------------
    # COMPLETENESS ANALYSIS
    # -----------------------------------------

    completeness_score = calculate_completeness(
        rules,
        variable_ranges,
        resolution=completeness_resolution,
        activation_threshold=activation_threshold
    )

    uncovered_regions = find_uncovered_regions(
        rules,
        variable_ranges,
        resolution=completeness_resolution,
        activation_threshold=activation_threshold
    )

    # -----------------------------------------
    # STATUS DETERMINATION
    # -----------------------------------------

    if conflicts:
        consistency_status = "WARNING"
    else:
        consistency_status = "PASS"

    if completeness_score < 100.0:
        completeness_status = "INCOMPLETE"
    else:
        completeness_status = "PASS"

    if (
        consistency_status == "PASS"
        and
        completeness_status == "PASS"
    ):
        overall_status = "PASS"

    else:
        overall_status = "REQUIRES REVIEW"

    # -----------------------------------------
    # FINAL RESULT
    # -----------------------------------------

    return {
        "rules_analyzed": len(rules),

        "consistency": {
            "conflict_count": len(conflicts),
            "status": consistency_status,
            "conflicts": conflicts
        },

        "completeness": {
            "score": round(
                completeness_score,
                4
            ),
            "uncovered_count": len(
                uncovered_regions
            ),
            "status": completeness_status,
            "uncovered_regions":
                uncovered_regions
        },

        "overall_status": overall_status
    }