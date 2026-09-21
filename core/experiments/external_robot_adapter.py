from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

from core.fuzzy.fuzzy_sets import TriangularFuzzySet
from core.rules.rules import FuzzyRule


JFML_NAMESPACE = "http://www.ieee1855.org"
NS = {"f": JFML_NAMESPACE}


def _tag(name: str) -> str:
    return f"{{{JFML_NAMESPACE}}}{name}"


def load_robot_rule_base(xml_path: str) -> Tuple[List[FuzzyRule], Dict]:
    """
    Load RobotMamdani.xml into the existing FuzzyRule representation.

    The source rule base has two consequents (la and av). The existing
    FuzzyRule abstraction supports one consequent string, so the complete
    output vector is preserved as a canonical structural token:

        la=TERM|av=TERM

    Source metadata is retained separately so the projection is explicit.
    """

    path = Path(xml_path)

    if not path.is_file():
        raise FileNotFoundError(f"Robot XML not found: {path}")

    tree = ET.parse(path)
    root = tree.getroot()

    variables = {}
    variable_metadata = {}

    for variable in root.findall(".//f:fuzzyVariable", NS):

        name = variable.get("name")
        domain_left = float(variable.get("domainleft"))
        domain_right = float(variable.get("domainright"))
        variable_type = variable.get("type", "")

        if not name:
            raise ValueError("Encountered fuzzyVariable without a name")

        terms = {}

        for term in variable.findall("./f:fuzzyTerm", NS):

            term_name = term.get("name")

            if not term_name:
                raise ValueError(
                    f"Variable {name} contains a fuzzyTerm without a name"
                )

            shapes = list(term)

            if len(shapes) != 1:
                raise ValueError(
                    f"Variable {name}, term {term_name}: "
                    f"expected exactly one membership shape"
                )

            shape = shapes[0]

            if shape.tag != _tag("triangularShape"):
                raise ValueError(
                    f"Variable {name}, term {term_name}: "
                    f"unsupported membership shape {shape.tag}"
                )

            a = float(shape.get("param1"))
            b = float(shape.get("param2"))
            c = float(shape.get("param3"))

            terms[term_name] = TriangularFuzzySet(
                name=term_name,
                a=a,
                b=b,
                c=c,
            )

        variables[name] = terms

        variable_metadata[name] = {
            "domain_left": domain_left,
            "domain_right": domain_right,
            "type": variable_type,
            "terms": {
                term_name: {
                    "shape": "triangular",
                    "parameters": (
                        fuzzy_set.a,
                        fuzzy_set.b,
                        fuzzy_set.c,
                    ),
                }
                for term_name, fuzzy_set in terms.items()
            },
        }

    rule_nodes = root.findall(".//f:mamdaniRuleBase/f:rule", NS)

    if not rule_nodes:
        raise ValueError("No Mamdani rules found in Robot XML")

    rules = []
    source_rules = []

    for rule_node in rule_nodes:

        rule_id = rule_node.get("name")
        weight = float(rule_node.get("weight", "1.0"))

        if not rule_id:
            raise ValueError("Encountered rule without a name")

        antecedent = {}
        source_antecedents = {}

        antecedent_clauses = rule_node.findall(
            "./f:antecedent/f:clause",
            NS,
        )

        for clause in antecedent_clauses:

            variable = clause.findtext("./f:variable", namespaces=NS)
            term = clause.findtext("./f:term", namespaces=NS)

            if variable not in variables:
                raise ValueError(
                    f"Rule {rule_id}: unknown antecedent variable {variable}"
                )

            if term not in variables[variable]:
                raise ValueError(
                    f"Rule {rule_id}: unknown term "
                    f"{variable}={term}"
                )

            if variable in antecedent:
                raise ValueError(
                    f"Rule {rule_id}: duplicate antecedent variable "
                    f"{variable}"
                )

            antecedent[variable] = variables[variable][term]
            source_antecedents[variable] = term

        consequent_clauses = rule_node.findall(
            "./f:consequent/f:then/f:clause",
            NS,
        )

        source_consequents = {}

        for clause in consequent_clauses:

            variable = clause.findtext("./f:variable", namespaces=NS)
            term = clause.findtext("./f:term", namespaces=NS)

            if variable not in variables:
                raise ValueError(
                    f"Rule {rule_id}: unknown consequent variable {variable}"
                )

            if term not in variables[variable]:
                raise ValueError(
                    f"Rule {rule_id}: unknown term "
                    f"{variable}={term}"
                )

            source_consequents[variable] = term

        required_outputs = ("la", "av")

        if set(source_consequents) != set(required_outputs):
            raise ValueError(
                f"Rule {rule_id}: expected consequents "
                f"{required_outputs}, got "
                f"{tuple(source_consequents)}"
            )

        canonical_consequent = (
            f"la={source_consequents['la']}"
            f"|av={source_consequents['av']}"
        )

        rules.append(
            FuzzyRule(
                rule_id=rule_id,
                antecedent=antecedent,
                consequent=canonical_consequent,
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
        "source": "RobotMamdani.xml",
        "format": "JFML / IEEE 1855 XML",
        "rule_count": len(rules),
        "variables": variable_metadata,
        "source_rules": source_rules,
        "analysis_projection": {
            "representation": "existing FuzzyRule",
            "consequent_encoding": "la=TERM|av=TERM",
            "semantic_scope": "structural",
        },
    }

    return rules, metadata
