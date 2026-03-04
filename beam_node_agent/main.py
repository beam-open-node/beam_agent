import argparse
import asyncio
import logging

try:
    from .config import load_config
    from .service import NodeAgent
except ImportError:
    # Allow running as a script entrypoint in frozen builds (PyInstaller).
    from beam_node_agent.config import load_config
    from beam_node_agent.service import NodeAgent


def main():
    parser = argparse.ArgumentParser(description="Beam Node Agent")
    parser.add_argument(
        "--config", default="config.yaml", help="Path to configuration file"
    )
    parser.add_argument(
        "--tui",
        action="store_true",
        help="Launch the terminal UI (requires textual: pip install beam-node-agent[tui])",
    )
    args = parser.parse_args()

    if args.tui:
        try:
            from beam_node_agent.tui.app import BeamTuiApp
        except ImportError:
            print(
                "The TUI requires the 'textual' package.\n"
                "Install it with:  pip install beam-node-agent[tui]"
            )
            return
        BeamTuiApp(config_path=args.config).run()
        return

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
