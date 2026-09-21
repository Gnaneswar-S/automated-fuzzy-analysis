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
def create_multi_defect_benchmark_case(
    case_id,
    clean_rules,
    defect_info,
    expected_repairs
):
    """
    Creates a reproducible benchmark case containing
    multiple controlled defects and explicit ground truth.

    Parameters
    ----------
    case_id : str
        Unique benchmark identifier.

    clean_rules : list
        Original clean rule base.

    defect_info : list of dict
        Information returned by multi-defect injection.

    expected_repairs : list of dict
        Ground-truth repair specification for each defect.

    Returns
    -------
    dict
        Multi-defect benchmark case.
    """

    defects = []

    for info in defect_info:

        defects.append({
            "type": info["defect_type"],
            "target_rule": info["target_rule"],
            "original_value": info[
                "original_consequent"
            ],
            "injected_value": info[
                "injected_consequent"
            ]
        })

    return {
        "case_id": case_id,

        "clean_rules": deepcopy(
            clean_rules
        ),

        "defects": defects,

        "ground_truth": {
            "defects": deepcopy(
                expected_repairs
            )
        }
    }
