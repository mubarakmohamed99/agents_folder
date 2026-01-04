"""Odoo setup utilities.

This module can either perform a conceptual setup (for demos / cloud
environments) or a more concrete local setup that installs Python
dependencies and starts the Odoo server process.
"""

import os
import subprocess
import sys
from typing import Tuple


def _run_command(args, cwd=None) -> bool:
    """Run a subprocess and report success.

    This is a thin wrapper so that all system calls are logged and
    failures are visible in the agent logs.
    """

    print("Running command:", " ".join(args))
    result = subprocess.run(args, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}.")
        return False
    return True


def setup_odoo(odoo_path: str, real_install: bool = False) -> Tuple[bool, str]:
    """Set up an Odoo environment.

    Args:
        odoo_path: Path to the downloaded/extracted Odoo source.
        real_install: If True, perform real steps (pip install and start
            the Odoo server). If False, only simulate the steps.

    Returns:
        Tuple[bool, str]: (success_flag, path_to_generated_config or "").
    """

    print(f"Starting Odoo setup from {odoo_path}...")

    try:
        # Step 1: Install Python dependencies
        requirements_path = os.path.join(odoo_path, "requirements.txt")
        if real_install:
            print("Installing Python dependencies from requirements.txt...")
            if os.path.exists(requirements_path):
                ok = _run_command(
                    [sys.executable, "-m", "pip", "install", "-r", requirements_path]
                )
                if not ok:
                    return False, ""
            else:
                print(
                    "Warning: requirements.txt not found. Skipping dependency "
                    "installation."
                )
        else:
            print("Installing Python dependencies (conceptual step)...")
        print("Python dependencies step completed.")

        # Step 2: Database setup (still conceptual – Odoo can manage DBs itself)
        if real_install:
            print(
                "Assuming PostgreSQL is installed and accessible. Odoo will "
                "use the connection settings from odoo.conf."
            )
        else:
            print("Setting up PostgreSQL database (conceptual step)...")
        print("Database setup step completed.")

        # Step 3: Create Odoo configuration file
        print("Creating Odoo configuration file...")
        config_path = os.path.join(odoo_path, "odoo.conf")
        with open(config_path, "w", encoding="utf-8") as config_file:
            config_file.write("# Auto-generated Odoo configuration file\n")
            config_file.write(f"addons_path = {os.path.join(odoo_path, 'addons')}\n")
            config_file.write("db_host = localhost\n")
            config_file.write("db_port = 5432\n")
            config_file.write("db_user = odoo\n")
            config_file.write("db_password = odoo\n")
            config_file.write("xmlrpc_port = 8069\n")
        print(f"Odoo configuration file created at {config_path}.")

        # Step 4: Start Odoo server
        if real_install:
            print("Starting real Odoo server process...")
            odoo_bin = os.path.join(odoo_path, "odoo-bin")
            if not os.path.exists(odoo_bin):
                print(
                    f"Error: odoo-bin not found at {odoo_bin}. Make sure the "
                    "Odoo source was downloaded correctly."
                )
                return False, ""

            # Launch Odoo in the background so the installer can exit.
            print("Launching Odoo server in background...")
            subprocess.Popen(
                [sys.executable, odoo_bin, "-c", config_path],
                cwd=odoo_path,
            )
            print(
                "Odoo server process started. You should be able to open "
                "http://localhost:8069 in your browser once it finishes "
                "initializing."
            )
        else:
            print("Initiating Odoo server process (conceptual step)...")
            print("Odoo server initiation command simulated.")

        print("Odoo setup completed successfully.")
        return True, config_path

    except Exception as exc:  # pragma: no cover - generic safety net
        print(f"Error during Odoo setup: {exc}")
        return False, ""
