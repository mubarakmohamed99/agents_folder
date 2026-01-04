"""Entry point for running the Odoo installer agent.

This script demonstrates how to use the `OdooInstallerAgent` in a
standalone way. It expects a Google Gemini API key to be provided via
the `GEMINI_API_KEY` environment variable.
"""

import os

from odoo_agent import OdooInstallerAgent


def main() -> None:
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

    print("Result:", "SUCCESS" if success else "FAILED")


if __name__ == "__main__":
    main()
