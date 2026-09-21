from pathlib import Path

import streamlit as st

from core.experiments.external_inverted_pendulum_adapter import (
    load_inverted_pendulum_rule_base,
)
from core.verification.verification import verify_rule_base


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

except Exception as exc:
    st.error(
        "Unable to load the Inverted Pendulum M1 rule base: "
        f"{exc}"
    )
