from copy import deepcopy


def create_benchmark_case(
    case_id,
    clean_rules,
    defect_type,
    target_rule,
    original_value,
    injected_value,
    expected_repair_action
):
    """
    Creates a reproducible benchmark case with
    explicit ground truth.
    """

    return {
        "case_id": case_id,

        "clean_rules": deepcopy(
            clean_rules
        ),

        "defect": {
            "type": defect_type,
            "target_rule": target_rule,
            "original_value": original_value,
            "injected_value": injected_value
        },

        "ground_truth": {
            "repair_action":
                expected_repair_action,

            "target_rule":
                target_rule,

            "correct_value":
                original_value
        }
    }