from pathlib import Path

from ..verification.verification import verify_rule_base
from .external_inverted_pendulum_adapter import (
    load_inverted_pendulum_rule_base
)
from .inverted_pendulum_mutation_experiment import (
    inject_antecedent_mutation
)
from .baseline_localization_experiment import (
    compare_localization_methods
)


def _print_ranking(
    label,
    result,
    score_key,
    top_n=10
):
    print()
    print(label)
    print("-" * len(label))

    print(
        f"Target rank: "
        f"{result['target_rank']}"
    )

    print(
        f"Target in top candidate set: "
        f"{result['target_in_top_set']}"
    )

    print(
        f"Top candidate set: "
        f"{result['top_candidates']}"
    )

    print(
        f"Candidate-set size: "
        f"{len(result['top_candidates'])}"
    )

    print()
    print("Top results:")

    for index, item in enumerate(
        result["ranking"][:top_n],
        start=1
    ):
        print(
            f"{index}. "
            f"{item['rule_id']} | "
            f"{score_key} = "
            f"{item[score_key]}"
        )


def run_experiment():

    xml_path = (
        Path(__file__).resolve().parents[3]
        / "fuzzy_external_validation"
        / "JFML"
        / "Examples"
        / "XMLFiles"
        / "InvertedPendulumMamdani1.xml"
    )

    rules, metadata = (
        load_inverted_pendulum_rule_base(
            xml_path
        )
    )

    variable_ranges = {
        variable: (
            details["domain_left"],
            details["domain_right"]
        )
        for variable, details
        in metadata["variables"].items()
        if details["type"] == "input"
    }

    target_rule = "rule9"
    donor_rule = "rule10"
    mutation_variable = "ChangeAngle"

    defective_rules, mutation_metadata = (
        inject_antecedent_mutation(
            rules,
            target_rule,
            donor_rule,
            mutation_variable
        )
    )

    verification = verify_rule_base(
        defective_rules,
        variable_ranges
    )

    conflicts = verification[
        "consistency"
    ]["conflicts"]

    comparison = compare_localization_methods(
        defective_rules,
        conflicts,
        variable_ranges,
        target_rule
    )

    print(
        "=== STEP 56: INVERTED PENDULUM "
        "BASELINE COMPARISON ==="
    )

    print(
        f"Rules: {len(defective_rules)}"
    )

    print(
        f"Ground-truth target: {target_rule}"
    )

    print(
        f"Mutation: "
        f"{mutation_metadata['variable']} "
        f"{mutation_metadata['original_term']} "
        f"-> "
        f"{mutation_metadata['injected_term']}"
    )

    print()
    print("Defective verification")
    print("----------------------")
    print(
        f"Conflicts: {len(conflicts)}"
    )
    print(
        f"Completeness: "
        f"{verification['completeness']['score']}"
    )
    print(
        f"Overall status: "
        f"{verification['overall_status']}"
    )

    for conflict in conflicts:
        print(
            f"{conflict['rule_1']} <-> "
            f"{conflict['rule_2']} | "
            f"score = "
            f"{conflict['conflict_score']}"
        )

    _print_ranking(
        "Conflict-count baseline",
        comparison[
            "conflict_count_baseline"
        ],
        "conflict_count"
    )

    _print_ranking(
        "Weighted suspicion",
        comparison[
            "weighted_suspicion"
        ],
        "suspicion_score"
    )

    print()
    print("=== COMPARISON SUMMARY ===")
    print(
        "Conflict-count target rank:",
        comparison[
            "conflict_count_baseline"
        ]["target_rank"]
    )
    print(
        "Weighted-suspicion target rank:",
        comparison[
            "weighted_suspicion"
        ]["target_rank"]
    )

    print(
        "Conflict-count candidate set:",
        comparison[
            "conflict_count_baseline"
        ]["top_candidates"]
    )

    print(
        "Weighted-suspicion candidate set:",
        comparison[
            "weighted_suspicion"
        ]["top_candidates"]
    )

    print()
    print(
        "Target localized by conflict-count:",
        comparison[
            "conflict_count_baseline"
        ]["target_in_top_set"]
    )

    print(
        "Target localized by weighted suspicion:",
        comparison[
            "weighted_suspicion"
        ]["target_in_top_set"]
    )


if __name__ == "__main__":
    run_experiment()
