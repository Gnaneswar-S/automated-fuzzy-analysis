from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

from core.fuzzy.fuzzy_sets import (
    TriangularFuzzySet,
    TrapezoidalFuzzySet,
)
from core.rules.rules import FuzzyRule


JFML_NAMESPACE = "http://www.ieee1855.org"
NS = {"f": JFML_NAMESPACE}


def _tag(name: str) -> str:
    return f"{{{JFML_NAMESPACE}}}{name}"


def load_inverted_pendulum_rule_base(
    xml_path: str,
) -> Tuple[List[FuzzyRule], Dict]:
    """
    Load InvertedPendulumMamdani1.xml into the existing
    FuzzyRule representation.

    The source contains one output variable (Force), so
    its consequent term can be represented directly by
    the existing single-consequent FuzzyRule abstraction.

    Supported membership shapes:
        - triangularShape
        - trapezoidShape

    Unsupported JFML constructs are rejected explicitly
    rather than approximated.
    """

    path = Path(xml_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Inverted Pendulum XML not found: {path}"
        )

    tree = ET.parse(path)
    root = tree.getroot()

    variables = {}
    variable_metadata = {}

    circular_definitions = root.findall(
        ".//f:circularDefinition",
        NS,
    )

    if circular_definitions:
        raise ValueError(
            "Circular definitions are not supported by this adapter"
        )

    for variable in root.findall(
        ".//f:fuzzyVariable",
        NS,
    ):

        name = variable.get("name")
        domain_left = float(
            variable.get("domainleft")
        )
        domain_right = float(
            variable.get("domainright")
        )
        variable_type = variable.get("type", "")

        if not name:
            raise ValueError(
                "Encountered fuzzyVariable without a name"
            )

        terms = {}

        for term in variable.findall(
            "./f:fuzzyTerm",
            NS,
        ):

            term_name = term.get("name")

            if not term_name:
                raise ValueError(
                    f"Variable {name} contains a "
                    "fuzzyTerm without a name"
                )

            complement = term.get(
                "complement",
                "false",
            ).lower()

            if complement == "true":
                raise ValueError(
                    f"Variable {name}, term {term_name}: "
                    "complement=true is not supported"
                )

            shapes = list(term)

            if len(shapes) != 1:
                raise ValueError(
                    f"Variable {name}, term {term_name}: "
                    "expected exactly one membership shape"
                )

            shape = shapes[0]

            if shape.tag == _tag("triangularShape"):

                a = float(shape.get("param1"))
                b = float(shape.get("param2"))
                c = float(shape.get("param3"))

                fuzzy_set = TriangularFuzzySet(
                    name=term_name,
                    a=a,
                    b=b,
                    c=c,
                )

                shape_name = "triangular"
                parameters = (a, b, c)

            elif shape.tag == _tag("trapezoidShape"):

                a = float(shape.get("param1"))
                b = float(shape.get("param2"))
                c = float(shape.get("param3"))
                d = float(shape.get("param4"))

                fuzzy_set = TrapezoidalFuzzySet(
                    name=term_name,
                    a=a,
                    b=b,
                    c=c,
                    d=d,
                )

                shape_name = "trapezoidal"
                parameters = (a, b, c, d)

            else:
                raise ValueError(
                    f"Variable {name}, term {term_name}: "
                    f"unsupported membership shape "
                    f"{shape.tag}"
                )

            terms[term_name] = fuzzy_set

            variable_metadata.setdefault(
                name,
                {
                    "domain_left": domain_left,
                    "domain_right": domain_right,
                    "type": variable_type,
                    "terms": {},
                },
            )

            variable_metadata[name]["terms"][
                term_name
            ] = {
                "shape": shape_name,
                "parameters": parameters,
                "complement": False,
            }

        variables[name] = terms

        variable_metadata.setdefault(
            name,
            {
                "domain_left": domain_left,
                "domain_right": domain_right,
                "type": variable_type,
                "terms": {},
            },
        )

    rule_nodes = root.findall(
        ".//f:mamdaniRuleBase/f:rule",
        NS,
    )

    if not rule_nodes:
        raise ValueError(
            "No Mamdani rules found in "
            "Inverted Pendulum XML"
        )

    rules = []
    source_rules = []

    for rule_node in rule_nodes:

        rule_id = rule_node.get("name")
        weight = float(
            rule_node.get("weight", "1.0")
        )

        if not rule_id:
            raise ValueError(
                "Encountered rule without a name"
            )

        antecedent = {}
        source_antecedents = {}

        antecedent_clauses = rule_node.findall(
            "./f:antecedent/f:clause",
            NS,
        )

        for clause in antecedent_clauses:

            variable = clause.findtext(
                "./f:variable",
                namespaces=NS,
            )
            term = clause.findtext(
                "./f:term",
                namespaces=NS,
            )

            if variable not in variables:
                raise ValueError(
                    f"Rule {rule_id}: unknown "
                    f"antecedent variable {variable}"
                )

            if term not in variables[variable]:
                raise ValueError(
                    f"Rule {rule_id}: unknown term "
                    f"{variable}={term}"
                )

            if variable in antecedent:
                raise ValueError(
                    f"Rule {rule_id}: duplicate "
                    f"antecedent variable {variable}"
                )

            antecedent[variable] = variables[
                variable
            ][term]

            source_antecedents[
                variable
            ] = term

        consequent_clauses = rule_node.findall(
            "./f:consequent/f:then/f:clause",
            NS,
        )

        source_consequents = {}

        for clause in consequent_clauses:

            variable = clause.findtext(
                "./f:variable",
                namespaces=NS,
            )
            term = clause.findtext(
                "./f:term",
                namespaces=NS,
            )

            if variable not in variables:
                raise ValueError(
                    f"Rule {rule_id}: unknown "
                    f"consequent variable {variable}"
                )

            if term not in variables[variable]:
                raise ValueError(
                    f"Rule {rule_id}: unknown term "
                    f"{variable}={term}"
                )

            source_consequents[
                variable
            ] = term

        required_outputs = {"Force"}

        if set(source_consequents) != required_outputs:
            raise ValueError(
                f"Rule {rule_id}: expected output "
                f"{required_outputs}, got "
                f"{tuple(source_consequents)}"
            )

        consequent = source_consequents["Force"]

        rules.append(
            FuzzyRule(
                rule_id=rule_id,
                antecedent=antecedent,
                consequent=consequent,
                weight=weight,
            )
        )

        source_rules.append(
            {
                "rule_id": rule_id,
                "antecedents": source_antecedents,
                "consequents": source_consequents,
                "weight": weight,
            }
        )

    metadata = {
        "source": "InvertedPendulumMamdani1.xml",
        "format": "JFML / IEEE 1855 XML",
        "rule_count": len(rules),
        "variables": variable_metadata,
        "source_rules": source_rules,
        "analysis_projection": {
            "representation": "existing FuzzyRule",
            "consequent_encoding": "Force=TERM",
            "semantic_scope": "structural",
        },
    }

    return rules, metadata