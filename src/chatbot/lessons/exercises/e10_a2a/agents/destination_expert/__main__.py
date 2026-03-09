from pathlib import Path
from chatbot.utils.a2a import A2AAgent
from chatbot.utils.logging import configure_logging
from chatbot.utils.telemetry import Telemetry
from .agent import agent


def main():
    configure_logging()

    # Path to agent card YAML file
    agent_card_path = Path(__file__).parent / "agent_card.yaml"

    # Create and start A2A server
    # The agent card YAML defines the agent's metadata and capabilities
    server = A2AAgent(agent=agent, agent_card_path=agent_card_path)

    # Start server with telemetry enabled
    with Telemetry(service_name="destination-expert"):
        server.start()


if __name__ == "__main__":
    main()
