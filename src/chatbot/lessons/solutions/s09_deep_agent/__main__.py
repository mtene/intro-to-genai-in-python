from pathlib import Path
from chatbot.utils.console import console
from chatbot.utils.logging import configure_logging
from chatbot.utils.telemetry import Telemetry
from .chatbot import ChatBot


def main():
    configure_logging()
    with Telemetry(service_name=Path(__file__).parent.name):
        console(ChatBot)


if __name__ == "__main__":
    main()
