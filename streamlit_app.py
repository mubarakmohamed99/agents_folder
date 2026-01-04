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
    "This web app **demonstrates** the Odoo installation workflow in a sandbox "
    "using the `OdooInstallerAgent`. It does not install Odoo on your local "
    "machine, but shows the steps, logs, and Google Gemini integration."
)

st.markdown(
    "**Want a real Windows installer?** "
    "Download the standalone installer EXE and run it on your machine: "
    "[Download Odoo Windows installer]"
    "(https://github.com/mubarakmohamed99/agents_folder/releases/latest/download/installer_main.exe). "
    "After downloading, double-click the file and follow the prompts."
)

st.info(
    "This Streamlit app runs in the cloud only. It **never** installs or "
    "changes software on your computer. To actually install Odoo on Windows, "
    "use the download link above and run the installer on your own machine."
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
            real_install=False,  # Streamlit stays conceptual by default
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
