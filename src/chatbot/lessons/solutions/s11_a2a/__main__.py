import sys
import subprocess
import time
from pathlib import Path
from typing import Dict
from chatbot.utils.console import console
from chatbot.utils.logging import configure_logging
from chatbot.utils.telemetry import Telemetry
from .chatbot import ChatBot


def main():
    configure_logging()

    # Start A2A agents as subprocesses
    agents: Dict[str, subprocess.Popen] = {}
    for agent_name in ["budget_expert", "destination_expert"]:
        agents[agent_name] = subprocess.Popen(
            [
                sys.executable,
                "-m",
                f"chatbot.lessons.{Path(__file__).parent.parent.name}.{Path(__file__).parent.name}.agents.{agent_name}",
            ],
        )
    time.sleep(3)

    try:
        with Telemetry(service_name=Path(__file__).parent.name):
            console(ChatBot)
    finally:
        # Clean up subprocesses
        for agent_process in agents.values():
            agent_process.terminate()
        for agent_process in agents.values():
            agent_process.wait()


if __name__ == "__main__":
    main()
