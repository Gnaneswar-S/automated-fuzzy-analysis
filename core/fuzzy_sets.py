from dataclasses import dataclass


@dataclass
class TriangularFuzzySet:
    name: str
    a: float
    b: float
    c: float

    def membership(self, x: float) -> float:

        if x <= self.a or x >= self.c:
            return 0.0

        if x == self.b:
            return 1.0

        if x < self.b:
            return (x - self.a) / (self.b - self.a)

        return (self.c - x) / (self.c - self.b)


@dataclass
class TrapezoidalFuzzySet:
    name: str
    a: float
    b: float
    c: float
    d: float

    def membership(self, x: float) -> float:

        if x <= self.a or x >= self.d:
            return 0.0

        if self.b <= x <= self.c:
            return 1.0

        if x < self.b:
            return (x - self.a) / (self.b - self.a)

        return (self.d - x) / (self.d - self.c)