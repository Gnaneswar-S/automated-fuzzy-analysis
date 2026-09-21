from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np


@dataclass(frozen=True)
class TriangularMF:
    name: str
    a: float
    b: float
    c: float

    def membership(self, x: float) -> float:
        if x == self.b:
            return 1.0
        if x <= self.a:
            return 0.0
        if x >= self.c:
            return 0.0
        if x < self.b:
            return (x - self.a) / (self.b - self.a)
        return (self.c - x) / (self.c - self.b)


@dataclass(frozen=True)
class TrapezoidalMF:
    name: str
    a: float
    b: float
    c: float
    d: float

    def membership(self, x: float) -> float:
        if self.b <= x <= self.c:
            return 1.0
        if x <= self.a:
            return 0.0
        if x >= self.d:
            return 0.0
        if x < self.b:
            return (x - self.a) / (self.b - self.a)
        return (self.d - x) / (self.d - self.c)


@dataclass(frozen=True)
class ReferenceRule:
    rule_id: str
    angle_terms: Tuple[str, ...]
    change_angle_terms: Tuple[str, ...]
    force_term: str
    connector: str = "or"
    weight: float = 1.0


def min_value(values: List[float]) -> float:
    return min(values)


def max_value(values: List[float]) -> float:
    return max(values)


def build_input_mfs() -> Dict[str, Dict[str, object]]:
    return {
        "Angle": {
            "very negative": TrapezoidalMF(
                "very negative", 0.0, 0.0, 48.0, 88.0
            ),
            "negative": TriangularMF(
                "negative", 48.0, 88.0, 128.0
            ),
            "zero": TriangularMF(
                "zero", 88.0, 128.0, 168.0
            ),
            "positive": TriangularMF(
                "positive", 128.0, 168.0, 208.0
            ),
            "very positive": TrapezoidalMF(
                "very positive", 168.0, 208.0, 255.0, 255.0
            ),
            "very negative or negative": TrapezoidalMF(
                "very negative or negative", 0.0, 0.0, 88.0, 128.0
            ),
            "positive or very positive": TrapezoidalMF(
                "positive or very positive", 128.0, 168.0, 255.0, 255.0
            ),
        },
        "ChangeAngle": {
            "very negative": TrapezoidalMF(
                "very negative", 0.0, 0.0, 48.0, 88.0
            ),
            "negative": TriangularMF(
                "negative", 48.0, 88.0, 128.0
            ),
            "zero": TriangularMF(
                "zero", 88.0, 128.0, 168.0
            ),
            "positive": TriangularMF(
                "positive", 128.0, 168.0, 208.0
            ),
            "very positive": TrapezoidalMF(
                "very positive", 168.0, 208.0, 255.0, 255.0
            ),
            "very negative or negative": TrapezoidalMF(
                "very negative or negative", 0.0, 0.0, 88.0, 128.0
            ),
            "positive or very positive": TrapezoidalMF(
                "positive or very positive", 128.0, 168.0, 255.0, 255.0
            ),
        },
    }


def build_output_mfs() -> Dict[str, object]:
    return {
        "very negative": TrapezoidalMF(
            "very negative", 0.0, 0.0, 48.0, 88.0
        ),
        "negative": TriangularMF(
            "negative", 48.0, 88.0, 128.0
        ),
        "zero": TriangularMF(
            "zero", 88.0, 128.0, 168.0
        ),
        "positive": TriangularMF(
            "positive", 128.0, 168.0, 208.0
        ),
        "very positive": TrapezoidalMF(
            "very positive", 168.0, 208.0, 255.0, 255.0
        ),
    }


RULES = [
    ReferenceRule(
    "rule1",
    ("very negative or negative",),
    ("very negative or negative",),
    "very negative",
    connector="and",
),
    ReferenceRule("rule2", ("very negative",),
                   ("zero",), "very negative", connector="and"),
    ReferenceRule("rule3", ("very negative",),
                   ("positive",), "negative", connector="and"),
    ReferenceRule("rule4", ("very negative",),
                   ("very positive",), "zero", connector="and"),
    ReferenceRule("rule5", ("negative",),
                   ("zero",), "negative", connector="and"),
    ReferenceRule("rule6", ("negative",),
                   ("positive",), "zero", connector="and"),
    ReferenceRule("rule7", ("negative",),
                   ("very positive",), "positive", connector="and"),
    ReferenceRule("rule8", ("zero",),
                   ("very negative",), "very negative", connector="and"),
    ReferenceRule("rule9", ("zero",),
                   ("negative",), "negative", connector="and"),
    ReferenceRule("rule10", ("zero",),
                   ("zero",), "zero", connector="and"),
    ReferenceRule("rule11", ("zero",),
                   ("positive",), "positive", connector="and"),
    ReferenceRule("rule12", ("zero",),
                   ("very positive",), "very positive", connector="and"),
    ReferenceRule("rule13", ("positive",),
                   ("very negative",), "negative", connector="and"),
    ReferenceRule("rule14", ("positive",),
                   ("negative",), "zero", connector="and"),
    ReferenceRule("rule15", ("positive",),
                   ("zero",), "positive", connector="and"),
    ReferenceRule("rule16", ("very positive",),
                   ("very negative",), "zero", connector="and"),
    ReferenceRule("rule17", ("very positive",),
                   ("negative",), "positive", connector="and"),
    ReferenceRule("rule18", ("very positive",),
                   ("zero",), "very positive", connector="and"),ReferenceRule(
    "rule19",
    ("positive or very positive",),
    ("positive or very positive",),
    "very positive",
    connector="and",
)]


def regular_output_points() -> List[float]:
    minimum = np.float32(0.0)
    maximum = np.float32(255.0)
    number_of_points = 2000
    step = np.float32((maximum - minimum) / np.float32(number_of_points))

    points = []
    x = np.float32(minimum)

    while x < maximum:
        points.append(float(x))
        x = np.float32(x + step)

    return points

def output_breakpoints() -> List[float]:
    return [
        0.0, 48.0, 88.0, 128.0, 168.0, 208.0, 255.0
    ]


def build_output_grid() -> List[float]:
    return sorted(set(
        regular_output_points() + output_breakpoints()
    ))


def antecedent_membership(
    terms: Tuple[str, ...],
    variable_mfs: Dict[str, object],
    value: float,
    connector: str,
) -> float:
    values = [
        np.float32(variable_mfs[term].membership(np.float32(value)))
        for term in terms
    ]

    if connector == "or":
        return np.float32(max_value(values))

    return np.float32(min_value(values))


def rule_firing(
    rule: ReferenceRule,
    angle: float,
    change_angle: float,
    input_mfs: Dict[str, Dict[str, object]],
) -> float:
    angle_value = antecedent_membership(
        rule.angle_terms,
        input_mfs["Angle"],
        angle,
        rule.connector,
    )

    change_value = antecedent_membership(
        rule.change_angle_terms,
        input_mfs["ChangeAngle"],
        change_angle,
        rule.connector,
    )

    firing = np.float32(min_value([angle_value, change_value]))
    return np.float32(firing * np.float32(rule.weight))


def evaluate(
    angle: float,
    change_angle: float,
) -> float:
    input_mfs = build_input_mfs()
    output_mfs = build_output_mfs()
    grid = build_output_grid()

    aggregated = {x: np.float32(0.0) for x in grid}

    for rule in RULES:
        firing = rule_firing(
            rule,
            np.float32(angle),
            np.float32(change_angle),
            input_mfs,
        )

        if firing <= np.float32(0.0):
            continue

        consequent = output_mfs[rule.force_term]

        for x in grid:
            membership = np.float32(consequent.membership(np.float32(x)))

            # JFML M1: MIN activation / implication.
            activated = np.float32(min_value([firing, membership]))

            # JFML M1: MAX accumulation.
            current = aggregated[x]
            if activated > current:
                aggregated[x] = activated

    numerator = np.float32(0.0)
    denominator = np.float32(0.0)

    for x in grid:
        y = np.float32(aggregated[x])
        numerator = np.float32(numerator + np.float32(np.float32(x) * y))
        denominator = np.float32(denominator + y)

    if denominator <= np.float32(0.0):
        return float("nan")

    return float(np.float32(numerator / denominator))


if __name__ == "__main__":
    print("JFML INDEPENDENT REFERENCE")
    print("--------------------------")

    points = [
        (128.0, 128.0),
        (88.0, 128.0),
        (168.0, 128.0),
        (128.0, 88.0),
        (128.0, 168.0),
        (100.0, 100.0),
        (150.0, 150.0),
        (0.0, 0.0),
        (255.0, 255.0),
    ]

    print(f"Output grid size: {len(build_output_grid())}")

    for angle, change_angle in points:
        result = evaluate(angle, change_angle)
        print(
            f"Angle={angle:7.3f} "
            f"ChangeAngle={change_angle:7.3f} "
            f"Force={result:12.7f}"
        )
