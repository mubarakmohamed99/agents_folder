"""Streamlit UI for the Odoo installer agent.

Run with:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import io
import os
import contextlib

import streamlit as st

from odoo_agent import OdooInstallerAgent


st.set_page_config(page_title="Odoo Installer Agent", page_icon="🛠", layout="centered")

st.title("Odoo Installer Agent")
st.write(
    "This app runs a conceptual Odoo installation workflow using the "
    "`OdooInstallerAgent`. It will try to detect an existing Odoo installation, "
    "optionally download Odoo, create a basic configuration file, and perform "
    "a conceptual Google Gemini integration."
)

st.info(
    "Note: This is a **conceptual** installer. It does not fully configure your "
    "system (PostgreSQL, services, etc.) but outlines and simulates the steps."
)

with st.form("odoo_install_form"):
    odoo_version = st.text_input("Odoo version", value="16.0")
    target_directory = st.text_input(
        "Target directory for installation",
        value="odoo_installation",
        help="Odoo source and configuration will be placed here.",
    )
    gemini_api_key = st.text_input(
        "Google Gemini API key (optional)",
        type="password",
        help=(
            "Provide this if you want the conceptual Google Gemini integration "
            "step to succeed. If left empty, the app will try to use the "
            "`GEMINI_API_KEY` Streamlit secret or environment variable."
        ),
    )

    submitted = st.form_submit_button("Run installation workflow")

if submitted:
    st.write("### Running agent...")

    config = {}
    key_to_use = gemini_api_key

    # If the user did not type a key, fall back to Streamlit secrets or
    # environment variables so it works on Streamlit Cloud with configured
    # secrets.
    if not key_to_use:
        if "GEMINI_API_KEY" in st.secrets:
            key_to_use = st.secrets["GEMINI_API_KEY"]
        else:
            key_to_use = os.environ.get("GEMINI_API_KEY")

    if key_to_use:
        config["gemini_api_key"] = key_to_use
    else:
        st.warning(
            "No Gemini API key provided and `GEMINI_API_KEY` secret/env is not "
            "set. Google API integration will fail.",
            icon="⚠️",
        )

    agent = OdooInstallerAgent(config=config)

    # Capture the agent's printed output so we can show it in the UI.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        success = agent.execute_installation_process(
            odoo_version=odoo_version,
            target_directory=target_directory,
        )

    logs = buffer.getvalue()

    st.subheader("Agent logs")
    if logs.strip():
        st.code(logs, language="text")
    else:
        st.write("(No logs captured.)")

    if success:
        st.success("Odoo installation workflow completed successfully.")
    else:
        st.error("Odoo installation workflow failed. Check the logs above for details.")
