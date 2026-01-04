"""Entry point for running the Odoo installer agent.

This script demonstrates how to use the `OdooInstallerAgent` in a
standalone way. Adjust configuration values (for example the Gemini API
key) and run this module to execute the conceptual installation flow.
"""

from odoo_agent import OdooInstallerAgent


def main() -> None:
    # Example configuration; replace values with real ones as needed.
    config = {
        # "gemini_api_key": "YOUR_REAL_GEMINI_API_KEY_HERE",
    }

    agent = OdooInstallerAgent(config=config)
    success = agent.execute_installation_process(
        odoo_version="16.0",
        target_directory="odoo_installation",
    )

    print("Result:", "SUCCESS" if success else "FAILED")


if __name__ == "__main__":
    main()
