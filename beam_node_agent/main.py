import argparse
import asyncio
import logging

import os
import sys

# Ensure the package root is on sys.path so absolute imports work in both
# normal Python and PyInstaller frozen builds.
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_pkg_dir)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from beam_node_agent.config import load_config
from beam_node_agent.service import NodeAgent


def main():
    parser = argparse.ArgumentParser(description="Beam Node Agent")
    parser.add_argument(
        "--config", default="config.yaml", help="Path to configuration file"
    )
    args = parser.parse_args()

    # Setup Logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Load Config
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return

    # Start Agent
    agent = NodeAgent(config)
    try:
        asyncio.run(agent.start())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
