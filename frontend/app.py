from pathlib import Path

import streamlit as st

from core.experiments.external_inverted_pendulum_adapter import (
    load_inverted_pendulum_rule_base,
)
from core.experiments.multi_defect_experiment import (
    create_three_region_independent_experiment_case,
)
from core.verification.verification import verify_rule_base
from core.diagnosis.diagnosis import diagnose_conflicts
from core.repair.repair import generate_repair_candidates
from core.repair.ranking import rank_repair_candidates
from core.repair.repair_engine import apply_repair_candidate
from core.diagnosis.localization import (
    calculate_rule_suspicion_scores,
    locate_conflict_regions,
)


st.set_page_config(
    page_title="Automated Fuzzy Rule-Base Analysis",
    page_icon=chr(0x1F52C),
    layout="wide",
)

st.title("Automated Fuzzy Rule-Base Analysis")
st.caption("Research Analysis Platform")

st.header("Analysis Mode")

analysis_mode = st.selectbox(
    "Select rule-base source",
    [
        "External Inverted Pendulum M1",
        "Controlled Benchmark - MD-5",
    ],
)

if st.session_state.get("_analysis_mode") != analysis_mode:
    analysis_keys = [
        "rules",
        "metadata",
        "variable_ranges",
        "verification",
        "suspicion_scores",
        "conflict_regions",
        "diagnosis",
        "repair_candidates",
        "ranked_repair_candidates",
        "repaired_rules",
        "repaired_verification",
    ]

    for key in analysis_keys:
        st.session_state.pop(key, None)

    st.session_state["_analysis_mode"] = analysis_mode

st.divider()

st.header("Rule Base")

try:
    if analysis_mode == "External Inverted Pendulum M1":
        repo_root = Path(__file__).resolve().parents[1]
        xml_path = (
            repo_root
            / "data"
            / "external_validation"
            / "InvertedPendulumMamdani1.xml"
        )

        rules, metadata = load_inverted_pendulum_rule_base(
            str(xml_path)
        )

        variable_ranges = {
            variable: (
                details["domain_left"],
                details["domain_right"],
            )
            for variable, details in metadata["variables"].items()
            if details["type"] == "input"
        }

        input_variables = [
            variable
            for variable, details in metadata["variables"].items()
            if details["type"] == "input"
        ]

        output_variables = [
            variable
            for variable, details in metadata["variables"].items()
            if details["type"] == "output"
        ]

        rule_base_title = "Inverted Pendulum Mamdani M1"

        st.info(
            "External validation rule base loaded from the JFML "
            "Inverted Pendulum Mamdani M1 model."
        )

    else:
        benchmark_case = create_three_region_independent_experiment_case()

        rules = benchmark_case["defective_rules"]

        variable_ranges = {
            "temperature": (0, 100),
            "humidity": (0, 100),
        }

        input_variables = [
            "temperature",
            "humidity",
        ]

        output_variables = ["risk"]

        metadata = {
            "source": "MD-5 controlled three-region independent benchmark",
            "variables": {
                "temperature": {
                    "type": "input",
                    "domain_left": 0,
                    "domain_right": 100,
                },
                "humidity": {
                    "type": "input",
                    "domain_left": 0,
                    "domain_right": 100,
                },
                "risk": {
                    "type": "output",
                },
            },
        }

        rule_base_title = "Controlled Benchmark - MD-5"

        st.info(
            "Controlled benchmark with three independent injected "
            "consequent conflicts. The benchmark ground truth is "
            "preserved separately from the repair-ranking heuristic."
        )

    st.subheader(rule_base_title)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rules", len(rules))

    with col2:
        st.metric("Inputs", len(input_variables))

    with col3:
        st.metric("Outputs", len(output_variables))

    domains = [
        f"{variable}: "
        f"{variable_ranges[variable][0]} - "
        f"{variable_ranges[variable][1]}"
        for variable in input_variables
    ]

    st.write("**Input domains**")
    for domain in domains:
        st.write(domain)

    st.write("**Output variables**")
    st.write(", ".join(output_variables))

    if analysis_mode == "Controlled Benchmark - MD-5":
        ground_truth = benchmark_case["benchmark_case"]["ground_truth"]

        st.write("**Benchmark ground truth**")
        st.dataframe(
            ground_truth,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    st.subheader("Rules")

    rule_rows = []

    for rule in rules:
        row = {
            "Rule": rule.rule_id,
        }

        for variable in input_variables:
            fuzzy_set = rule.antecedent.get(variable)
            row[variable] = (
                fuzzy_set.name
                if fuzzy_set is not None
                else "-"
            )

        row["Consequent"] = rule.consequent
        row["Weight"] = rule.weight

        rule_rows.append(row)

    st.dataframe(
        rule_rows,
        width="stretch",
        hide_index=True,
    )

    st.divider()

    if st.button("Run Verification", type="primary"):
        verification = verify_rule_base(
            rules,
            variable_ranges,
        )

        st.session_state["rules"] = rules
        st.session_state["metadata"] = metadata
        st.session_state["variable_ranges"] = variable_ranges
        st.session_state["verification"] = verification

    if "verification" in st.session_state:
        verification = st.session_state["verification"]

        st.header("Verification")

        completeness = verification["completeness"]
        consistency = verification["consistency"]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rules analyzed",
                verification["rules_analyzed"],
            )

        with col2:
            st.metric(
                "Potential conflicts",
                consistency["conflict_count"],
            )

        with col3:
            st.metric(
                "Completeness",
                f"{completeness['score']:.1f}%",
            )

        with col4:
            st.metric(
                "Overall status",
                verification["overall_status"],
            )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Consistency")
            st.write(consistency["status"])

        with col2:
            st.subheader("Completeness")
            st.write(completeness["status"])

        if consistency["conflicts"]:
            st.subheader("Detected conflicts")
            st.json(consistency["conflicts"])
        else:
            st.info("No potential conflicts were detected.")

        if completeness["uncovered_regions"]:
            st.subheader("Uncovered regions")
            st.json(completeness["uncovered_regions"])
        else:
            st.info("No uncovered regions were detected.")

    st.divider()

    st.header("Localization")

    if st.button("Run Localization"):
        suspicion_scores = calculate_rule_suspicion_scores(
            rules,
            variable_ranges,
        )

        conflict_regions = locate_conflict_regions(
            rules,
            variable_ranges,
        )

        st.session_state["suspicion_scores"] = suspicion_scores
        st.session_state["conflict_regions"] = conflict_regions

    if "suspicion_scores" in st.session_state:
        suspicion_scores = st.session_state["suspicion_scores"]
        conflict_regions = st.session_state["conflict_regions"]

        st.subheader("Rule Suspicion Scores")
        st.dataframe(
            suspicion_scores,
            width="stretch",
            hide_index=True,
        )

        st.subheader("Localized Conflict Regions")
        st.metric("Regions identified", len(conflict_regions))

        if conflict_regions:
            st.json(conflict_regions)
        else:
            st.info("No conflict regions were localized.")

    st.divider()

    st.header("Diagnosis")

    if st.button("Run Diagnosis"):
        if "verification" not in st.session_state:
            st.warning("Run Verification before Diagnosis.")
        elif "conflict_regions" not in st.session_state:
            st.warning("Run Localization before Diagnosis.")
        else:
            conflicts = st.session_state["verification"]["consistency"]["conflicts"]
            conflict_regions = st.session_state["conflict_regions"]

            diagnosis = diagnose_conflicts(
                rules,
                conflicts,
                conflict_regions,
            )

            st.session_state["diagnosis"] = diagnosis

    if "diagnosis" in st.session_state:
        diagnosis = st.session_state["diagnosis"]

        st.subheader("Conflict Diagnosis")

        if diagnosis:
            st.dataframe(
                diagnosis,
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("No conflicts require diagnosis.")

    st.divider()

    st.header("Repair")

    if st.button("Generate Repair Candidates"):
        if "verification" not in st.session_state:
            st.warning(
                "Run Verification before generating Repair Candidates."
            )
        else:
            conflicts = st.session_state["verification"]["consistency"]["conflicts"]

            if not conflicts:
                st.session_state["repair_candidates"] = []
                st.session_state["ranked_repair_candidates"] = []
            else:
                repair_candidates = generate_repair_candidates(
                    rules,
                    conflicts,
                )

                ranked_candidates = rank_repair_candidates(
                    rules,
                    repair_candidates,
                    variable_ranges,
                )

                st.session_state["repair_candidates"] = repair_candidates
                st.session_state["ranked_repair_candidates"] = ranked_candidates

    if "ranked_repair_candidates" in st.session_state:
        ranked_candidates = st.session_state["ranked_repair_candidates"]

        if ranked_candidates:
            st.subheader("Repair Candidates")

            repair_rows = []

            for index, item in enumerate(ranked_candidates):
                candidate = item["candidate"]

                repair_rows.append({
                    "candidate": index + 1,
                    "conflict": candidate["conflict"],
                    "action": candidate["action"],
                    "target_rule": candidate["target_rule"],
                    "new_consequent": candidate.get("new_consequent", ""),
                    "ranking_score": item["score"],
                    "conflicts_before": item["conflicts_before"],
                    "conflicts_after": item["conflicts_after"],
                    "completeness_before": item["completeness_before"],
                    "completeness_after": item["completeness_after"],
                    "repair_success": item["repair_success"],
                })

            st.dataframe(
                repair_rows,
                width="stretch",
                hide_index=True,
            )

            st.info(
                "Repair candidates are proposals only. "
                "No repair is automatically applied."
            )

            selected_index = st.selectbox(
                "Select a repair candidate",
                options=list(range(len(ranked_candidates))),
                format_func=lambda index: (
                    f"Candidate {index + 1}: "
                    f"{ranked_candidates[index]['candidate']['action']} "
                    f"{ranked_candidates[index]['candidate']['target_rule']} "
                    f"({ranked_candidates[index]['candidate']['conflict']})"
                ),
            )

            selected_item = ranked_candidates[selected_index]
            selected_candidate = selected_item["candidate"]

            st.subheader("Selected Repair")

            st.write(selected_candidate["description"])

            if st.button("Apply Selected Repair"):
                repaired_rules = apply_repair_candidate(
                    rules,
                    selected_candidate,
                )

                repaired_verification = verify_rule_base(
                    repaired_rules,
                    variable_ranges,
                )

                st.session_state["repaired_rules"] = repaired_rules
                st.session_state["repaired_verification"] = repaired_verification

        else:
            st.info("No repair candidates are available.")

    if "repaired_verification" in st.session_state:
        repaired_verification = st.session_state["repaired_verification"]

        st.subheader("Re-verification")

        before_verification = st.session_state["verification"]

        before_conflicts = before_verification["consistency"]["conflict_count"]
        after_conflicts = repaired_verification["consistency"]["conflict_count"]

        before_completeness = before_verification["completeness"]["score"]
        after_completeness = repaired_verification["completeness"]["score"]

        st.metric("Conflicts before repair", before_conflicts)
        st.metric("Conflicts after repair", after_conflicts)
        st.metric("Completeness before repair", f"{before_completeness:.1f}%")
        st.metric("Completeness after repair", f"{after_completeness:.1f}%")

        st.write(
            "Repaired rule base status:",
            repaired_verification["overall_status"],
        )

        if (
            after_conflicts < before_conflicts
            and after_completeness >= before_completeness
        ):
            st.success(
                "The selected repair reduced detected conflicts "
                "without reducing completeness."
            )
        else:
            st.warning(
                "The selected repair did not satisfy both "
                "conflict reduction and completeness preservation."
            )

except Exception as exc:
    st.error(
        "Unable to load the selected rule base: "
        f"{exc}"
    )
