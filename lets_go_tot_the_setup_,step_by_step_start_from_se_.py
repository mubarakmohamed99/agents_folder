"""Legacy Colab notebook entrypoint.

The original Colab notebook that explored the Odoo installer agent has been
refactored into a proper Python package structure under the `odoo_agent`
package. This file is kept only as a lightweight entrypoint and reference.

To run the conceptual Odoo installation flow, prefer using `main.py` or
importing `OdooInstallerAgent` directly from `odoo_agent`.
"""

from odoo_agent import OdooInstallerAgent


def main() -> None:
    """Run a simple demo installation flow via the refactored package."""

    config = {
        # "gemini_api_key": "YOUR_REAL_GEMINI_API_KEY_HERE",
    }

    agent = OdooInstallerAgent(config=config)
    success = agent.execute_installation_process(
        odoo_version="16.0",
        target_directory="odoo_installation",
    )

    print("Result (legacy entrypoint):", "SUCCESS" if success else "FAILED")


if __name__ == "__main__":
    main()