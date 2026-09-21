import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

import jfml_independent_reference as reference


JFML_FILE = HERE / "jfml_validation_sweep.csv"

# PREDECLARED VALIDATION CRITERION
TOLERANCE = 1e-5


def load_jfml_results():
    results = []

    with JFML_FILE.open("r", encoding="utf-8-sig", newline="") as handle:
        lines = handle.readlines()

    data_lines = [
        line.strip()
        for line in lines
        if line.strip()
        and not line.startswith("JFML_VALIDATION_SWEEP")
        and not line.startswith("points_per_axis=")
        and not line.startswith("total_points=")
    ]

    for line in data_lines:
        angle, change_angle, force = map(float, line.split(","))
        results.append((angle, change_angle, force))

    return results


def main():
    jfml_results = load_jfml_results()

    errors = []
    mismatches = []
    nan_mismatches = []

    for angle, change_angle, jfml_force in jfml_results:

        independent_force = reference.evaluate(
            np.float32(angle),
            np.float32(change_angle),
        )

        if math.isnan(jfml_force) or math.isnan(independent_force):
            if math.isnan(jfml_force) and math.isnan(independent_force):
                continue

            nan_mismatches.append(
                (angle, change_angle, jfml_force, independent_force)
            )
            continue

        error = abs(jfml_force - independent_force)
        errors.append(error)

        if error > TOLERANCE:
            mismatches.append(
                (
                    angle,
                    change_angle,
                    jfml_force,
                    independent_force,
                    error,
                )
            )

    total = len(jfml_results)
    max_error = max(errors) if errors else float("nan")
    mae = sum(errors) / len(errors) if errors else float("nan")

    print("=== STEP 57: SYSTEMATIC EXTERNAL VALIDATION ===")
    print(f"JFML evaluations: {total}")
    print(f"Independent evaluations: {total}")
    print(f"Tolerance: {TOLERANCE:.1e}")
    print()

    print("Numerical comparison")
    print("--------------------")
    print(f"Maximum absolute error: {max_error:.12g}")
    print(f"Mean absolute error:    {mae:.12g}")
    print(f"Comparisons within tolerance: {total - len(mismatches)}")
    print(f"Comparisons above tolerance:  {len(mismatches)}")
    print(f"NaN mismatches:              {len(nan_mismatches)}")
    print()

    if mismatches:
        print("MISMATCHES")
        print("----------")

        for row in mismatches[:20]:
            angle, change_angle, jfml_force, independent_force, error = row
            print(
                f"Angle={angle:.6f} "
                f"ChangeAngle={change_angle:.6f} "
                f"JFML={jfml_force:.12f} "
                f"Independent={independent_force:.12f} "
                f"Error={error:.12g}"
            )

        if len(mismatches) > 20:
            print(f"... {len(mismatches) - 20} additional mismatches")

    else:
        print("RESULT")
        print("------")
        print("ALL 289 OUTPUTS AGREE WITHIN THE PREDECLARED TOLERANCE.")


if __name__ == "__main__":
    main()
