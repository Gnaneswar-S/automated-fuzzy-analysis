from pathlib import Path

import streamlit as st

from core.experiments.external_inverted_pendulum_adapter import (
    load_inverted_pendulum_rule_base,
)
from core.verification.verification import verify_rule_base
from core.diagnosis.diagnosis import diagnose_conflicts
from core.repair.repair import generate_repair_candidates
from core.repair.ranking import rank_repair_candidates
from core.diagnosis.localization import (
    calculate_rule_suspicion_scores,
    locate_conflict_regions,
)


st.set_page_config(
    page_title="Automated Fuzzy Rule-Base Analysis",
    page_icon="🔬",
    layout="wide",
)

st.title("Automated Fuzzy Rule-Base Analysis")
st.caption("Research Analysis Platform")

st.header("Rule Base")

try:
    xml_path = (
        Path.home()
        / "Desktop"
        / "Documents"
        / "fuzzy_external_validation"
        / "JFML"
        / "Examples"
        / "XMLFiles"
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

    st.subheader("Inverted Pendulum Mamdani M1")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rules", len(rules))

    with col2:
        st.metric("Inputs", len(input_variables))

    with col3:
        st.metric("Outputs", len(output_variables))

    domains = [
        f"{variable}: "
        f"{metadata['variables'][variable]['domain_left']} – "
        f"{metadata['variables'][variable]['domain_right']}"
        for variable in input_variables
    ]

    st.write("**Input domains**")
    for domain in domains:
        st.write(domain)

    st.write("**Output variables**")
    st.write(", ".join(output_variables))

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
                else "—"
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
            st.warning("Run Verification before generating Repair Candidates.")
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

            for item in ranked_candidates:
                candidate = item["candidate"]

                repair_rows.append({
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
        else:
            st.info("No repair candidates are available.")

except Exception as exc:
    st.error(
        "Unable to load the Inverted Pendulum M1 rule base: "
        f"{exc}"
    )
