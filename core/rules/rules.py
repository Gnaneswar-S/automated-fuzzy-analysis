from dataclasses import dataclass
from typing import Dict


@dataclass
class FuzzyRule:

    rule_id: str

    antecedent: Dict[str, object]

    consequent: str

    weight: float = 1.0

    def membership(self, inputs):

        values = []

        for variable, fuzzy_set in self.antecedent.items():

            x = inputs[variable]

            values.append(
                fuzzy_set.membership(x)
            )

        if not values:
            return 0.0

        return min(values)