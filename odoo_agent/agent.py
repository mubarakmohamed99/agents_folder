"""High-level Odoo installer agent.

The `OdooInstallerAgent` coordinates detection, download, setup, and
conceptual Google API integration for an Odoo instance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from .detection import detect_odoo_executable
from .download import download_odoo
from .setup_odoo import setup_odoo
from .google_integration import integrate_google_api


@dataclass
class OdooInstallerAgent:
    """AI-style agent that manages the Odoo installation workflow.

    The methods follow the same logical flow as in the original Colab
    notebook, but the implementation is now split into reusable modules.
    """

    config: Dict = field(default_factory=dict)
    odoo_config_path: Optional[str] = None

    def __post_init__(self) -> None:
        print("OdooInstallerAgent initialized with configuration:", self.config)

    # --- Low-level operations -------------------------------------------------

    def detect_odoo_executable(self):
        """Detect an existing Odoo executable on the system."""

        return detect_odoo_executable()

    def download_odoo(
        self,
        version: str = "16.0",
        target_dir: str = ".",
        download_url: Optional[str] = None,
    ):
        """Download and extract Odoo source code."""

        return download_odoo(version=version, target_dir=target_dir, download_url=download_url)

    def setup_odoo(self, odoo_path: str, real_install: bool = False) -> bool:
        """Run Odoo setup steps and remember the config path.

        If ``real_install`` is True this will attempt to install
        requirements and start a real Odoo server process. Otherwise it
        behaves conceptually (no system changes).
        """

        success, config_path = setup_odoo(odoo_path, real_install=real_install)
        if success:
            self.odoo_config_path = config_path
        return success

    def integrate_google_api(self, odoo_instance_details: Dict) -> bool:
        """Integrate Google APIs (for example Gemini) conceptually."""

        return integrate_google_api(self.config, odoo_instance_details)

    # --- Orchestration --------------------------------------------------------

    def execute_installation_process(
        self,
        odoo_version: str = "16.0",
        target_directory: str = ".",
        real_install: bool = False,
    ) -> bool:
        """Run the full conceptual Odoo installation workflow.

        Steps:
        1. Detect existing Odoo executable.
        2. If not found, download and extract the specified Odoo version.
        3. Run setup steps (conceptual or real, depending on ``real_install``).
        4. Conceptually integrate Google APIs.
        """

        print("Starting Odoo installation process...")

        # Step 1: Detect existing Odoo installation
        found, odoo_exec_path = self.detect_odoo_executable()
        if found:
            print(f"Odoo executable found at: {odoo_exec_path}. Skipping download.")
            # Use the parent directory of the executable as the installation root
            # when possible.
            import os

            current_odoo_path = os.path.dirname(odoo_exec_path) or "."
            print(f"Using detected Odoo path for setup: {current_odoo_path}")
        else:
            # Step 2: Download Odoo
            success, download_path = self.download_odoo(
                version=odoo_version,
                target_dir=target_directory,
            )
            if not success:
                print("Odoo download failed.")
                return False
            current_odoo_path = download_path

        # Step 3: Setup Odoo
        if not self.setup_odoo(current_odoo_path, real_install=real_install):
            print("Odoo setup failed.")
            return False

        # Placeholder for getting actual Odoo instance details after setup
        odoo_instance_details = {"url": "http://localhost:8069", "admin_user": "admin"}

        # Step 4: Integrate Google API
        if not self.integrate_google_api(odoo_instance_details):
            print("Google API integration failed.")
            return False

        print("Odoo installation process completed successfully.")
        return True
