from copy import deepcopy


def inject_antecedent_mutation(
    rules,
    target_rule_id,
    donor_rule_id,
    variable,
):
    """
    Create a controlled antecedent mutation.

    The target rule receives the donor rule's fuzzy set
    for exactly one antecedent variable. All other rule
    properties remain unchanged.

    Returns:
        mutated_rules, mutation_metadata
    """

    mutated_rules = deepcopy(rules)

    target_rule = None
    donor_rule = None

    for rule in mutated_rules:

        if rule.rule_id == target_rule_id:
            target_rule = rule

        if rule.rule_id == donor_rule_id:
            donor_rule = rule

    if target_rule is None:
        raise ValueError(
            f"Target rule '{target_rule_id}' not found."
        )

    if donor_rule is None:
        raise ValueError(
            f"Donor rule '{donor_rule_id}' not found."
        )

    if variable not in target_rule.antecedent:
        raise ValueError(
            f"Variable '{variable}' not found in "
            f"target rule '{target_rule_id}'."
        )

    if variable not in donor_rule.antecedent:
        raise ValueError(
            f"Variable '{variable}' not found in "
            f"donor rule '{donor_rule_id}'."
        )

    original_fuzzy_set = target_rule.antecedent[
        variable
    ]

    donor_fuzzy_set = donor_rule.antecedent[
        variable
    ]

    original_term = original_fuzzy_set.name
    injected_term = donor_fuzzy_set.name

    target_rule.antecedent[
        variable
    ] = donor_fuzzy_set

    mutation_metadata = {
        "defect_type": "ANTECEDENT_MUTATION",
        "target_rule": target_rule_id,
        "donor_rule": donor_rule_id,
        "variable": variable,
        "original_term": original_term,
        "injected_term": injected_term,
        "original_consequent": target_rule.consequent,
    }

    return mutated_rules, mutation_metadata