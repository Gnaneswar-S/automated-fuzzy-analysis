from typing import Any, Dict, List, Tuple

from core.fuzzy.fuzzy_sets import (
    TrapezoidalFuzzySet,
    TriangularFuzzySet,
)
from core.rules.rules import FuzzyRule


def _build_fuzzy_set(
    name: str,
    definition: Dict[str, Any],
):
    set_type = definition.get("type")
    parameters = definition.get("parameters")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Fuzzy-set name must be a non-empty string.")

    if not isinstance(parameters, (list, tuple)):
        raise ValueError(
            f"Fuzzy set '{name}' must provide numeric parameters."
        )

    try:
        parameters = [float(value) for value in parameters]
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Fuzzy set '{name}' parameters must be numeric."
        ) from exc

    if set_type == "triangular":
        if len(parameters) != 3:
            raise ValueError(
                f"Triangular fuzzy set '{name}' requires exactly 3 parameters."
            )

        a, b, c = parameters

        if not a < b < c:
            raise ValueError(
                f"Triangular fuzzy set '{name}' requires a < b < c."
            )

        return TriangularFuzzySet(name, a, b, c)

    if set_type == "trapezoidal":
        if len(parameters) != 4:
            raise ValueError(
                f"Trapezoidal fuzzy set '{name}' requires exactly 4 parameters."
            )

        a, b, c, d = parameters

        if not a < b <= c < d:
            raise ValueError(
                f"Trapezoidal fuzzy set '{name}' requires a < b <= c < d."
            )

        return TrapezoidalFuzzySet(name, a, b, c, d)

    raise ValueError(
        f"Unsupported fuzzy-set type '{set_type}' for '{name}'."
    )


def load_custom_rule_base(
    definition: Dict[str, Any],
) -> Tuple[List[FuzzyRule], Dict[str, Any]]:
    """
    Convert a custom rule-base definition into the project's
    existing FuzzyRule representation.

    The adapter performs source-format translation only.
    Verification, localization, diagnosis, and repair remain
    delegated to the existing research pipeline.
    """

    if not isinstance(definition, dict):
        raise ValueError("Custom rule-base definition must be a dictionary.")

    variables = definition.get("variables")
    rule_definitions = definition.get("rules")

    if not isinstance(variables, dict) or not variables:
        raise ValueError(
            "Custom rule-base definition must contain 'variables'."
        )

    if not isinstance(rule_definitions, list) or not rule_definitions:
        raise ValueError(
            "Custom rule-base definition must contain at least one rule."
        )

    variable_sets: Dict[str, Dict[str, object]] = {}
    metadata_variables: Dict[str, Dict[str, Any]] = {}

    for variable, variable_definition in variables.items():
        if not isinstance(variable, str) or not variable.strip():
            raise ValueError("Variable names must be non-empty strings.")

        if not isinstance(variable_definition, dict):
            raise ValueError(
                f"Definition for variable '{variable}' must be a dictionary."
            )

        variable_type = variable_definition.get("type")

        if variable_type not in {"input", "output"}:
            raise ValueError(
                f"Variable '{variable}' must have type 'input' or 'output'."
            )

        sets = variable_definition.get("sets", {})

        if not isinstance(sets, dict) or not sets:
            raise ValueError(
                f"Variable '{variable}' must define at least one fuzzy set."
            )

        built_sets = {}

        for set_name, set_definition in sets.items():
            if set_name in built_sets:
                raise ValueError(
                    f"Duplicate fuzzy set '{set_name}' "
                    f"for variable '{variable}'."
                )

            built_sets[set_name] = _build_fuzzy_set(
                set_name,
                set_definition,
            )

        variable_sets[variable] = built_sets

        metadata_variable = {
            "type": variable_type,
        }

        if variable_type == "input":
            if "domain_left" not in variable_definition:
                raise ValueError(
                    f"Input variable '{variable}' requires 'domain_left'."
                )

            if "domain_right" not in variable_definition:
                raise ValueError(
                    f"Input variable '{variable}' requires 'domain_right'."
                )

            try:
                domain_left = float(variable_definition["domain_left"])
                domain_right = float(variable_definition["domain_right"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Input variable '{variable}' domain must be numeric."
                ) from exc

            if not domain_left < domain_right:
                raise ValueError(
                    f"Input variable '{variable}' requires "
                    "domain_left < domain_right."
                )

            metadata_variable["domain_left"] = domain_left
            metadata_variable["domain_right"] = domain_right

        metadata_variable["sets"] = sets
        metadata_variables[variable] = metadata_variable

    input_variables = [
        variable
        for variable, details in metadata_variables.items()
        if details["type"] == "input"
    ]

    output_variables = [
        variable
        for variable, details in metadata_variables.items()
        if details["type"] == "output"
    ]

    if not input_variables:
        raise ValueError("At least one input variable is required.")

    if not output_variables:
        raise ValueError("At least one output variable is required.")

    rules: List[FuzzyRule] = []
    rule_ids = set()

    for rule_definition in rule_definitions:
        if not isinstance(rule_definition, dict):
            raise ValueError("Each rule definition must be a dictionary.")

        rule_id = rule_definition.get("rule_id")
        antecedent_definition = rule_definition.get("antecedent")
        consequent = rule_definition.get("consequent")
        weight = rule_definition.get("weight", 1.0)

        if not isinstance(rule_id, str) or not rule_id.strip():
            raise ValueError("Each rule requires a non-empty 'rule_id'.")

        if rule_id in rule_ids:
            raise ValueError(f"Duplicate rule ID '{rule_id}'.")

        if not isinstance(antecedent_definition, dict):
            raise ValueError(
                f"Rule '{rule_id}' must contain an antecedent dictionary."
            )

        if not antecedent_definition:
            raise ValueError(
                f"Rule '{rule_id}' must contain at least one antecedent."
            )

        if not isinstance(consequent, str) or not consequent.strip():
            raise ValueError(
                f"Rule '{rule_id}' requires a non-empty consequent."
            )

        try:
            weight = float(weight)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Rule '{rule_id}' weight must be numeric."
            ) from exc

        antecedent = {}

        for variable, set_name in antecedent_definition.items():
            if variable not in variable_sets:
                raise ValueError(
                    f"Rule '{rule_id}' references unknown variable "
                    f"'{variable}'."
                )

            if metadata_variables[variable]["type"] != "input":
                raise ValueError(
                    f"Rule '{rule_id}' uses non-input variable "
                    f"'{variable}' in its antecedent."
                )

            if set_name not in variable_sets[variable]:
                raise ValueError(
                    f"Rule '{rule_id}' references unknown fuzzy set "
                    f"'{set_name}' for variable '{variable}'."
                )

            antecedent[variable] = variable_sets[variable][set_name]

        rules.append(
            FuzzyRule(
                rule_id=rule_id,
                antecedent=antecedent,
                consequent=consequent,
                weight=weight,
            )
        )

        rule_ids.add(rule_id)

    metadata = {
        "source": "custom rule base",
        "format": "native custom definition",
        "variables": metadata_variables,
        "input_variables": input_variables,
        "output_variables": output_variables,
        "rule_count": len(rules),
    }

    return rules, metadata
