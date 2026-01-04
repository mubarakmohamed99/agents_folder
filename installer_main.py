"""Interactive local installer entrypoint for Odoo.

This script is meant to be turned into a Windows one-click installer
(EXE) using tools like PyInstaller. When run, it asks for a few
parameters and then runs the OdooInstallerAgent in real-install mode.
"""

from __future__ import annotations

import os

from odoo_agent import OdooInstallerAgent


def main() -> None:
    print("=== Odoo Installer (Interactive) ===")

    version = input("Odoo version to install [16.0]: ") or "16.0"
    target_dir = input("Target directory [odoo_installation]: ") or "odoo_installation"

    # Ask once for Gemini key (optional)
    existing_key = os.environ.get("GEMINI_API_KEY")
    default_hint = " (leave blank to skip / use existing)" if existing_key else " (leave blank to skip)"
    gemini = input(f"Google Gemini API key{default_hint}: ")

    config: dict = {}
    if gemini:
        config["gemini_api_key"] = gemini
    elif existing_key:
        config["gemini_api_key"] = existing_key

    agent = OdooInstallerAgent(config=config)
    success = agent.execute_installation_process(
        odoo_version=version,
        target_directory=target_dir,
        real_install=True,
    )

    print("Result:", "SUCCESS" if success else "FAILED")
    if success:
        print("You can now open http://localhost:8069 in your browser.")


if __name__ == "__main__":
    main()
