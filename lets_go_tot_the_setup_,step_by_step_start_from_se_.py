"""Legacy Colab notebook entrypoint.

The original Colab notebook that explored the Odoo installer agent has been
refactored into a proper Python package structure under the `odoo_agent`
package. This file is kept only as a lightweight entrypoint and reference.

To run the conceptual Odoo installation flow, prefer using `main.py` or
importing `OdooInstallerAgent` directly from `odoo_agent`.
"""

import os

from odoo_agent import OdooInstallerAgent


def main() -> None:
    """Run a simple demo installation flow via the refactored package."""

    # Read the Gemini API key from an environment variable instead of
    # hardcoding it in the repository.
    api_key = os.environ.get("GEMINI_API_KEY")
    config = {}
    if api_key:
        config["gemini_api_key"] = api_key
    else:
        print(
            "Warning: GEMINI_API_KEY environment variable is not set. "
            "Google API integration will fail."
        )

    agent = OdooInstallerAgent(config=config)
    success = agent.execute_installation_process(
        odoo_version="16.0",
        target_directory="odoo_installation",
    )

    print("Result (legacy entrypoint):", "SUCCESS" if success else "FAILED")


if __name__ == "__main__":
    main()